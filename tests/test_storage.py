"""Tests for storage.py — run with: pytest tests/"""

import csv
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "fng-collector"))


@pytest.fixture()
def tmp_data(tmp_path, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(tmp_path))
    for mod in ["config", "storage"]:
        if mod in sys.modules:
            del sys.modules[mod]
    return tmp_path


def test_first_write_creates_csv(tmp_data):
    import storage

    storage.CSV_FILE = str(tmp_data / "fng.csv")
    storage.DATA_DIR = str(tmp_data)

    written = storage.save(55)

    assert written is True
    with open(storage.CSV_FILE) as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1
    assert int(rows[0]["value"]) == 55


def test_duplicate_within_same_minute_is_skipped(tmp_data):
    import storage

    storage.CSV_FILE = str(tmp_data / "fng.csv")
    storage.DATA_DIR = str(tmp_data)

    storage.save(55)
    written = storage.save(60)

    assert written is False
    with open(storage.CSV_FILE) as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1
