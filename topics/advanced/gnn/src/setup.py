import logging
from logging import getLogger

from rich.logging import RichHandler

from src.paths import LOG_DIR

logger = getLogger(__name__)


def setup_logger(level: str = "NOTSET") -> None:
    """Configure Rich console logging and a file handler under LOG_DIR."""
    if LOG_DIR.exists():
        logger.info("Loading logs from %s", LOG_DIR.resolve())
    else:
        logger.info("Creating logs directory at %s", LOG_DIR.resolve())
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level="NOTSET",  # level is set on RichHandler
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                level=level,
            ),
            logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8", mode="w"),
        ],
    )
    logger.info("Logger setup complete.")
