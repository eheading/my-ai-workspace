"""
SQLite database layer for X Tracker.

Tables:
  tracked_users   – accounts to follow, with optional description
  posts           – cached tweets (de-duplicated by tweet ID)
  daily_summaries – AI-generated summaries with send status
"""

import sqlite3
from datetime import date, datetime
from typing import Optional
import config


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create tables if they do not exist yet."""
    with _conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tracked_users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT    UNIQUE NOT NULL COLLATE NOCASE,
                description TEXT    DEFAULT '',
                active      INTEGER DEFAULT 1,
                created_at  TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS posts (
                tweet_id   TEXT PRIMARY KEY,
                username   TEXT NOT NULL COLLATE NOCASE,
                content    TEXT NOT NULL,
                created_at TEXT NOT NULL,
                fetched_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS daily_summaries (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                date       TEXT    UNIQUE NOT NULL,
                summary    TEXT    NOT NULL,
                sent       INTEGER DEFAULT 0,
                sent_at    TEXT
            );
            """
        )


# ── Tracked users ──────────────────────────────────────────────────────────────

def add_user(username: str, description: str = "") -> bool:
    """Add a user to track. Returns True if inserted, False if already exists."""
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO tracked_users (username, description) VALUES (?, ?)",
                (username.lstrip("@"), description),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def update_user_description(username: str, description: str) -> bool:
    """Update description for an existing user. Returns True if found."""
    with _conn() as conn:
        cur = conn.execute(
            "UPDATE tracked_users SET description = ? WHERE username = ? COLLATE NOCASE",
            (description, username.lstrip("@")),
        )
    return cur.rowcount > 0


def remove_user(username: str) -> bool:
    """Deactivate (soft-delete) a tracked user. Returns True if found."""
    with _conn() as conn:
        cur = conn.execute(
            "UPDATE tracked_users SET active = 0 WHERE username = ? COLLATE NOCASE",
            (username.lstrip("@"),),
        )
    return cur.rowcount > 0


def list_users(active_only: bool = True) -> list[dict]:
    with _conn() as conn:
        query = "SELECT * FROM tracked_users"
        if active_only:
            query += " WHERE active = 1"
        query += " ORDER BY username"
        return [dict(row) for row in conn.execute(query).fetchall()]


# ── Posts ──────────────────────────────────────────────────────────────────────

def save_posts(posts: list[dict]) -> int:
    """Bulk-insert posts; skip duplicates. Returns number of new rows."""
    inserted = 0
    with _conn() as conn:
        for p in posts:
            try:
                conn.execute(
                    "INSERT INTO posts (tweet_id, username, content, created_at) VALUES (?, ?, ?, ?)",
                    (p["tweet_id"], p["username"], p["content"], p["created_at"]),
                )
                inserted += 1
            except sqlite3.IntegrityError:
                pass  # already cached
    return inserted


def get_posts_since(since: datetime) -> list[dict]:
    """Return all posts created on or after *since* (UTC)."""
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM posts WHERE created_at >= ? ORDER BY created_at DESC",
            (since.isoformat(),),
        ).fetchall()
    return [dict(r) for r in rows]


# ── Daily summaries ────────────────────────────────────────────────────────────

def save_summary(summary_date: date, summary: str) -> None:
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO daily_summaries (date, summary)
            VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET summary = excluded.summary, sent = 0
            """,
            (summary_date.isoformat(), summary),
        )


def mark_summary_sent(summary_date: date) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE daily_summaries SET sent = 1, sent_at = datetime('now') WHERE date = ?",
            (summary_date.isoformat(),),
        )


def get_summary(summary_date: date) -> Optional[dict]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM daily_summaries WHERE date = ?",
            (summary_date.isoformat(),),
        ).fetchone()
    return dict(row) if row else None
