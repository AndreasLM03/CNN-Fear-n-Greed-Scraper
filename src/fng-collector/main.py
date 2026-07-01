"""Entry point: fetch Fear & Greed Index and persist it, then exit."""

import logging
import logging.handlers
import os
import sys

from config import LOG_BACKUP_COUNT, LOG_DIR, LOG_FILE, LOG_MAX_BYTES
from scraper import fetch_fear_and_greed
from storage import save


def _setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])


def main() -> None:
    _setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("fng-collector starting …")

    try:
        value = fetch_fear_and_greed()
        save(value)
        logger.info("fng-collector finished successfully.")
    except Exception:
        logger.exception("Unhandled error — exiting with code 1.")
        sys.exit(1)


if __name__ == "__main__":
    main()
