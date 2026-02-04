import os
import sqlite3
import tempfile
from pathlib import Path

import pytest

from scripts.online_agent import main


def read_events(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def test_dry_run_appends_event_and_audit(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # ensure prototype default
    monkeypatch.setenv("PROTOTYPE_USE_LOCAL_EVENTS", "1")
    monkeypatch.delenv("ALLOW_COMMAND_EXECUTION", raising=False)

    rc = main(["--command", "dry_run"])  # returns 0
    assert rc == 0

    events = read_events(tmp_path / "events.ndjson")
    assert any("received" in e for e in events)

    # check audit DB
    conn = sqlite3.connect(tmp_path / "gaia.db")
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name IN ('audit','audit_v2')")
    assert cur.fetchone()[0] >= 1
    conn.close()


def test_prototype_skip_on_send_telegram(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PROTOTYPE_USE_LOCAL_EVENTS", "1")
    monkeypatch.setenv("ALLOW_COMMAND_EXECUTION", "0")

    rc = main(["--command", "send_telegram", "--body", "hello"])
    # In prototype mode without ALLOW_COMMAND_EXECUTION, script exits 0 and records prototype_skipped
    assert rc == 0
    events = read_events(tmp_path / "events.ndjson")
    assert any("prototype_skipped" in e for e in events)
