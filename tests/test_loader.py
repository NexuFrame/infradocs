from pathlib import Path

import pytest

from infradocs.loader import load_csv, load_yaml

SAMPLE = Path(__file__).parent.parent / "sample-data"


def test_load_yaml_devices():
    devices = load_yaml(SAMPLE / "devices.yaml").get("devices", [])
    assert len(devices) >= 1
    assert "hostname" in devices[0]
    assert "ip" in devices[0]


def test_load_yaml_sites():
    sites = load_yaml(SAMPLE / "sites.yaml").get("sites", [])
    assert len(sites) >= 1
    assert "id" in sites[0]


def test_load_csv_changelog():
    rows = load_csv(SAMPLE / "change-log.csv")
    assert len(rows) >= 1
    assert "date" in rows[0]
    assert "engineer" in rows[0]


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_yaml(SAMPLE / "nonexistent.yaml")
