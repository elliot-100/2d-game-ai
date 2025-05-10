"""Set up logging for examples."""

import sys

from loguru import logger


def configure_logger() -> None:
    """Set up the logger."""
    logger.remove()
    logger.add(sys.stderr, level="INFO")
