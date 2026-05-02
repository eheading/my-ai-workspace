"""
Telegram notification layer.

Sends the daily digest (and optionally on-demand messages) via the
python-telegram-bot library using the Bot.send_message() helper.
Long messages are automatically split to respect Telegram's 4096-char limit.
"""

import asyncio
import logging
from datetime import date

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

import config
import db

logger = logging.getLogger(__name__)

_MAX_LEN = 4000  # Telegram hard cap is 4096; 96-char buffer for Markdown formatting overhead


def _split_message(text: str) -> list[str]:
    """Split a long message into chunks that Telegram can handle."""
    if len(text) <= _MAX_LEN:
        return [text]
    chunks: list[str] = []
    while text:
        if len(text) <= _MAX_LEN:
            chunks.append(text)
            break
        # Try to split at a paragraph boundary
        split_at = text.rfind("\n\n", 0, _MAX_LEN)
        if split_at == -1:
            split_at = text.rfind("\n", 0, _MAX_LEN)
        if split_at == -1:
            split_at = _MAX_LEN
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    return chunks


async def _send_async(text: str, chat_id: str, token: str) -> None:
    bot = Bot(token=token)
    async with bot:
        for chunk in _split_message(text):
            await bot.send_message(
                chat_id=chat_id,
                text=chunk,
                parse_mode=ParseMode.MARKDOWN,
            )


def send_message(text: str) -> None:
    """Send *text* to the configured Telegram chat (blocking)."""
    asyncio.run(_send_async(text, config.TELEGRAM_CHAT_ID, config.TELEGRAM_BOT_TOKEN))


def send_daily_summary(summary_date: date | None = None) -> None:
    """
    Retrieve the stored summary for *summary_date* and send it via Telegram.
    Marks the summary as sent on success.
    """
    if summary_date is None:
        summary_date = date.today()

    record = db.get_summary(summary_date)
    if not record:
        logger.warning("No summary found for %s – nothing to send.", summary_date)
        return

    if record["sent"]:
        logger.info("Summary for %s already sent – skipping.", summary_date)
        return

    try:
        send_message(record["summary"])
        db.mark_summary_sent(summary_date)
        logger.info("Daily summary for %s sent successfully.", summary_date)
    except TelegramError as exc:
        logger.error("Failed to send Telegram message: %s", exc)
        raise
