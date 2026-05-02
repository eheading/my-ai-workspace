"""
AI analyser: filters investment-related posts and generates a daily stock summary.

Uses the OpenAI Chat Completions API (model configured in config.OPENAI_MODEL).
"""

import json
import logging
from datetime import date, datetime, timedelta, timezone

from openai import OpenAI

import config
import db

logger = logging.getLogger(__name__)

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.OPENAI_API_KEY)
    return _client


# ── Step 1: filter investment-related posts ────────────────────────────────────

_FILTER_SYSTEM = """\
You are a financial research assistant.
Given a list of social-media posts (from X.com), identify which ones are
investment-related.  A post is investment-related if it discusses:
  • individual stocks, ETFs, or crypto assets (cashtags like $AAPL, $BTC, #ticker)
  • earnings reports, guidance, or analyst upgrades/downgrades
  • macro events with clear market implications (Fed decisions, CPI, etc.)
  • investment recommendations, buy/sell/hold opinions
  • sector trends or market outlooks

Respond with ONLY a JSON array of the original post objects that are investment-related.
Keep the original fields: tweet_id, username, content, created_at.
If none qualify, return an empty array [].
"""


def filter_investment_posts(posts: list[dict]) -> list[dict]:
    """Return only investment-related posts from the provided list."""
    if not posts:
        return []

    # Send in batches of 50 to stay within context limits
    relevant: list[dict] = []
    batch_size = 50
    for i in range(0, len(posts), batch_size):
        batch = posts[i : i + batch_size]
        payload = json.dumps(batch, ensure_ascii=False)
        try:
            response = _get_client().chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": _FILTER_SYSTEM},
                    {"role": "user", "content": payload},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content or "[]"
            # model returns {"posts": [...]} or just [...]
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                relevant.extend(parsed)
            elif isinstance(parsed, dict):
                for v in parsed.values():
                    if isinstance(v, list):
                        relevant.extend(v)
                        break
        except Exception as exc:
            logger.error("OpenAI filter error (batch %d): %s", i, exc)

    return relevant


# ── Step 2: generate daily digest ─────────────────────────────────────────────

_SUMMARY_SYSTEM = """\
You are a senior equity analyst assistant.  You receive a collection of
investment-related social-media posts sourced from X.com.

Your task is to produce a concise, actionable *Daily Investment Digest* in
Traditional Chinese (繁體中文) for a private investor.

Structure your response as follows:

## 📊 每日投資重點摘要 — {date}

### 🔥 值得關注的股票 / 資產
List each mentioned ticker with:
  - Ticker symbol and company/asset name
  - Why it was mentioned (sentiment, catalyst, key point)
  - Overall sentiment: 📈 看漲 / 📉 看跌 / 🔄 中性

### 💡 主要市場觀點
Bullet-point summary of the key macro or sector themes.

### ⚠️ 風險提示
Any notable concerns, cautionary signals, or conflicting opinions.

### 📝 資料來源
List the X.com usernames whose posts informed this digest.

---
Keep the digest tight (under 600 words).  Do NOT give explicit buy/sell advice.
"""


def generate_summary(investment_posts: list[dict], for_date: date) -> str:
    """Generate a Telegram-ready daily digest from filtered investment posts."""
    if not investment_posts:
        return (
            f"## 📊 每日投資重點摘要 — {for_date}\n\n"
            "今日追蹤的帳號未發現值得關注的投資相關貼文。\n"
        )

    formatted = "\n\n".join(
        f"[@{p['username']}] {p['created_at'][:16]}\n{p['content']}"
        for p in investment_posts
    )

    prompt = f"以下是今日收集到的投資相關貼文：\n\n{formatted}"

    try:
        response = _get_client().chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": _SUMMARY_SYSTEM.format(date=for_date.strftime("%Y-%m-%d")),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        return response.choices[0].message.content or "（AI 未能生成摘要）"
    except Exception as exc:
        logger.error("OpenAI summary error: %s", exc)
        return f"（AI 摘要生成失敗：{exc}）"


# ── Top-level pipeline ─────────────────────────────────────────────────────────

def run_analysis(for_date: date | None = None) -> str:
    """
    Full pipeline:
      1. Load posts from the past LOOKBACK_DAYS days
      2. Filter to investment-related ones
      3. Generate and persist the daily summary
    Returns the summary text.
    """
    if for_date is None:
        for_date = date.today()

    since = datetime.combine(for_date, datetime.min.time()) - timedelta(
        days=config.LOOKBACK_DAYS - 1
    )
    posts = db.get_posts_since(since)
    logger.info("Loaded %d cached posts for analysis.", len(posts))

    investment_posts = filter_investment_posts(posts)
    logger.info("Identified %d investment-related posts.", len(investment_posts))

    summary = generate_summary(investment_posts, for_date)
    db.save_summary(for_date, summary)
    logger.info("Summary saved to database.")
    return summary
