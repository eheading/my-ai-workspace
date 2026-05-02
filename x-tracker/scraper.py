"""
X.com scraper using twscrape.

twscrape authenticates with real X.com accounts stored in an account pool.
Accounts are loaded from the TWITTER_ACCOUNTS environment variable (JSON array).

Each account object:
  {"username": "...", "password": "...", "email": "...", "email_password": "..."}

At a minimum one account is required.  Use multiple accounts to reduce rate-limit risk.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import AsyncIterator

import twscrape
from twscrape import API as TwAPI

import config
import db

logger = logging.getLogger(__name__)


async def _build_api() -> TwAPI:
    """Create a twscrape API instance and populate the account pool."""
    api = TwAPI()
    accounts = json.loads(config.TWITTER_ACCOUNTS_JSON)
    if not accounts:
        raise RuntimeError(
            "No X.com accounts configured.  "
            "Set TWITTER_ACCOUNTS in your .env file."
        )
    for acc in accounts:
        await api.pool.add_account(
            username=acc["username"],
            password=acc["password"],
            email=acc["email"],
            email_password=acc["email_password"],
        )
    await api.pool.login_all()
    return api


def _tweet_to_dict(tweet) -> dict:
    return {
        "tweet_id": str(tweet.id),
        "username": tweet.user.username,
        "content": tweet.rawContent,
        "created_at": tweet.date.isoformat(),
    }


async def _fetch_user_tweets(api: TwAPI, username: str, since: datetime) -> list[dict]:
    """Fetch up to TWEETS_PER_USER tweets for *username* posted after *since*."""
    results: list[dict] = []
    try:
        user = await api.user_by_login(username)
        if user is None:
            logger.warning("User not found on X.com: @%s", username)
            return []
        async for tweet in api.user_tweets(user.id, limit=config.TWEETS_PER_USER):
            if tweet.date.replace(tzinfo=timezone.utc) < since.replace(tzinfo=timezone.utc):
                break  # timeline is reverse-chronological; stop once we're past the window
            results.append(_tweet_to_dict(tweet))
    except Exception as exc:
        logger.error("Error fetching tweets for @%s: %s", username, exc)
    return results


async def scrape_all() -> int:
    """
    Fetch recent tweets for all active tracked users and persist them.
    Returns the total number of *new* posts saved.
    """
    users = db.list_users(active_only=True)
    if not users:
        logger.info("No tracked users found.  Use 'python cli.py add <username>' to add one.")
        return 0

    since = datetime.now(timezone.utc) - timedelta(days=config.LOOKBACK_DAYS)

    api = await _build_api()
    all_posts: list[dict] = []
    for user in users:
        username = user["username"]
        logger.info("Fetching tweets for @%s …", username)
        posts = await _fetch_user_tweets(api, username, since)
        logger.info("  → %d tweets found", len(posts))
        all_posts.extend(posts)

    new_count = db.save_posts(all_posts)
    logger.info("Scraping complete.  %d new posts saved.", new_count)
    return new_count


def run_scrape() -> int:
    """Synchronous wrapper around scrape_all() for use in non-async code."""
    return asyncio.run(scrape_all())
