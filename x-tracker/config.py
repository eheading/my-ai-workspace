"""
Configuration management for X Tracker.
Loads settings from environment variables (or .env file).
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            f"Please copy .env.example to .env and fill in the values."
        )
    return value


# ---------- Telegram ----------
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

# ---------- OpenAI ----------
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ---------- Scheduling ----------
# 24-hour HH:MM format (UTC) for daily digest dispatch
DAILY_SUMMARY_TIME: str = os.getenv("DAILY_SUMMARY_TIME", "09:00")

# ---------- Database ----------
DB_PATH: str = os.getenv("DB_PATH", "x_tracker.db")

# ---------- X / twscrape accounts ----------
# Provide a JSON array of objects:
# [{"username":"...", "password":"...", "email":"...", "email_password":"..."}]
TWITTER_ACCOUNTS_JSON: str = os.getenv("TWITTER_ACCOUNTS", "[]")

# How many recent tweets to fetch per user per run
TWEETS_PER_USER: int = int(os.getenv("TWEETS_PER_USER", "20"))

# How many days back to look (posts older than this are ignored)
LOOKBACK_DAYS: int = int(os.getenv("LOOKBACK_DAYS", "1"))


def validate():
    """Raise EnvironmentError if any required variable is missing."""
    missing = []
    for key in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "OPENAI_API_KEY"):
        if not os.getenv(key):
            missing.append(key)
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please copy .env.example to .env and fill in the values."
        )
