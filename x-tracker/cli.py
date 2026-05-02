"""
CLI entry point for X Tracker.

Usage:
  python cli.py add <username> [--desc "description"]
  python cli.py remove <username>
  python cli.py list
  python cli.py run         # scrape + analyse + send right now
  python cli.py scrape      # scrape only
  python cli.py analyse     # analyse only (uses cached posts)
  python cli.py send        # send today's stored summary
  python cli.py daemon      # start the daily scheduler
"""

import logging
import sys

import click

import config
import db
import scraper
import analyzer
import telegram_bot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@click.group()
def cli():
    """X Tracker – follow X.com users and receive daily investment digests via Telegram."""
    db.init_db()


# ── User management ────────────────────────────────────────────────────────────

@cli.command("add")
@click.argument("username")
@click.option("--desc", "-d", default="", help="Description / notes about this account.")
def cmd_add(username: str, desc: str):
    """Add a username to the tracked list."""
    username = username.lstrip("@")
    if db.add_user(username, desc):
        click.echo(f"✅  Added @{username}" + (f" — {desc}" if desc else ""))
    else:
        # Update description if user already exists
        db.update_user_description(username, desc)
        click.echo(f"ℹ️  @{username} already tracked.  Description updated.")


@cli.command("remove")
@click.argument("username")
def cmd_remove(username: str):
    """Stop tracking a username (soft delete)."""
    username = username.lstrip("@")
    if db.remove_user(username):
        click.echo(f"🗑️  Removed @{username} from tracked list.")
    else:
        click.echo(f"⚠️  @{username} not found.", err=True)
        sys.exit(1)


@cli.command("list")
def cmd_list():
    """Show all actively tracked usernames."""
    users = db.list_users(active_only=True)
    if not users:
        click.echo("No users tracked yet.  Use 'add' to add one.")
        return
    click.echo(f"{'#':<4} {'Username':<25} {'Description'}")
    click.echo("─" * 70)
    for i, u in enumerate(users, 1):
        click.echo(f"{i:<4} @{u['username']:<24} {u['description'] or '—'}")


# ── Pipeline commands ──────────────────────────────────────────────────────────

@cli.command("scrape")
def cmd_scrape():
    """Fetch recent X.com posts for all tracked users."""
    config.validate()
    n = scraper.run_scrape()
    click.echo(f"✅  Scraping done.  {n} new posts saved.")


@cli.command("analyse")
def cmd_analyse():
    """Analyse cached posts and generate today's digest."""
    config.validate()
    summary = analyzer.run_analysis()
    click.echo("\n" + summary)


@cli.command("send")
def cmd_send():
    """Send today's stored digest to Telegram."""
    config.validate()
    telegram_bot.send_daily_summary()
    click.echo("✅  Summary sent to Telegram.")


@cli.command("run")
def cmd_run():
    """Full pipeline: scrape → analyse → send (run once now)."""
    config.validate()
    click.echo("🔄  Scraping posts …")
    scraper.run_scrape()
    click.echo("🤖  Analysing posts …")
    analyzer.run_analysis()
    click.echo("📨  Sending digest …")
    telegram_bot.send_daily_summary()
    click.echo("✅  Done.")


# ── Scheduler daemon ──────────────────────────────────────────────────────────

@cli.command("daemon")
def cmd_daemon():
    """
    Start the daily scheduler.  Runs the full pipeline once a day at the
    time configured in DAILY_SUMMARY_TIME (default: 09:00 UTC).
    """
    from apscheduler.schedulers.blocking import BlockingScheduler
    from apscheduler.triggers.cron import CronTrigger

    config.validate()
    db.init_db()

    hour, minute = config.DAILY_SUMMARY_TIME.split(":")

    def daily_job():
        import logging as _log
        log = _log.getLogger("scheduler")
        log.info("Daily job started.")
        try:
            scraper.run_scrape()
            analyzer.run_analysis()
            telegram_bot.send_daily_summary()
            log.info("Daily job completed successfully.")
        except Exception as exc:
            log.error("Daily job failed: %s", exc)

    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(
        daily_job,
        trigger=CronTrigger(hour=int(hour), minute=int(minute), timezone="UTC"),
        id="daily_digest",
        name="Daily investment digest",
        replace_existing=True,
    )

    click.echo(
        f"⏰  Scheduler started.  Daily digest will fire at {config.DAILY_SUMMARY_TIME} UTC.\n"
        "Press Ctrl+C to stop."
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        click.echo("\nScheduler stopped.")


if __name__ == "__main__":
    cli()
