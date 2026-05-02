"""
Main entry point – also exposes a convenience `main()` function
that other scripts (e.g. cron, Docker CMD) can call directly.
"""

import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from cli import cli

if __name__ == "__main__":
    cli()
