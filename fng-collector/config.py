"""Central configuration for fng-collector."""

import os

# Data directory — mounted as Docker volume
DATA_DIR: str = os.getenv("DATA_DIR", "/data")
CSV_FILE: str = os.path.join(DATA_DIR, "fng.csv")
LOG_DIR: str = os.path.join(DATA_DIR, "logs")
LOG_FILE: str = os.path.join(LOG_DIR, "fng.log")

# Logging
LOG_MAX_BYTES: int = 1 * 1024 * 1024  # 1 MB
LOG_BACKUP_COUNT: int = 3

# HTTP
REQUEST_TIMEOUT: int = 15  # seconds

# Primary: CNN data endpoint (no browser needed, User-Agent required)
CNN_URL: str = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
CNN_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://edition.cnn.com/markets/fear-and-greed",
}
