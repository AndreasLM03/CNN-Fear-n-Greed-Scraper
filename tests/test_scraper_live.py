"""Live integration tests — require internet access.

Run with: pytest tests/test_scraper_live.py -v -s -m integration
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "fng-collector"))


@pytest.mark.integration
def test_cnn_endpoint_returns_valid_score():
    from scraper import _fetch_cnn

    score = _fetch_cnn()
    assert isinstance(score, int)
    assert 0 <= score <= 100, f"Score out of range: {score}"
    print(f"\nCNN score: {score}")


@pytest.mark.integration
def test_fetch_fear_and_greed_returns_valid_score():
    from scraper import fetch_fear_and_greed

    score = fetch_fear_and_greed()
    assert isinstance(score, int)
    assert 0 <= score <= 100
    print(f"\nFinal score: {score}")
