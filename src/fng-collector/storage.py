"""Reads and writes Fear & Greed data to a CSV file on the mounted volume."""

import csv
import logging
import os
from datetime import datetime, timezone

from config import CSV_FILE, DATA_DIR

logger = logging.getLogger(__name__)

CSV_HEADER = ["timestamp", "value"]


def _ensure_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _last_timestamp() -> str | None:
    """Returns the timestamp of the most recent CSV row, or None if the file is empty."""
    if not os.path.exists(CSV_FILE):
        return None
    with open(CSV_FILE, newline="") as fh:
        rows = list(csv.DictReader(fh))
    return rows[-1]["timestamp"] if rows else None


def save(value: int) -> bool:
    """Appends a new row to the CSV.

    Returns True if the row was written, False if the timestamp already exists
    (duplicate guard — same minute).
    """
    _ensure_dirs()

    now_iso = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S")

    last = _last_timestamp()
    if last and last[:16] == now_iso[:16]:  # same HH:MM → skip
        logger.info("Duplicate entry for %s — skipping.", now_iso[:16])
        return False

    write_header = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_HEADER)
        if write_header:
            writer.writeheader()
        writer.writerow({"timestamp": now_iso, "value": value})

    logger.info("Saved FnG=%d at %s", value, now_iso)
    return True
