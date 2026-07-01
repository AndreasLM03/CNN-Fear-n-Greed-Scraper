"""Fetches the current CNN Fear & Greed Index value via plain HTTP — no browser needed."""

import logging

import requests

from config import CNN_HEADERS, CNN_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def _fetch_cnn() -> int:
    """Fetches current FnG score from CNN's data endpoint."""
    response = requests.get(CNN_URL, headers=CNN_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    score = int(data["fear_and_greed"]["score"])
    logger.debug("CNN endpoint returned score=%d", score)
    return score


def fetch_fear_and_greed() -> int:
    """Returns the current Fear & Greed Index value (0–100)."""
    try:
        score = _fetch_cnn()
        logger.info("Fetched FnG from CNN: %d", score)
        return score
    except Exception as exc:
        logger.warning("CNN endpoint failed (%s), trying fallback …", exc)

    return score
