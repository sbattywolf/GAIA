import json
from pathlib import Path
import os
import time
from datetime import datetime, timedelta


def test_auto_requeue_dry_run(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    perm = root / '.tmp' / 'telegram_queue_failed_permanent.json'
    failed = root / '.tmp' / 'telegram_queue_failed.json'
    perm.parent.mkdir(parents=True, exist_ok=True)

    item = {'action': 'send_message', '_retries': 0, '_failed_at': (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'}
    perm.write_text(json.dumps([item], indent=2), encoding='utf-8')
    if failed.exists():
        failed.unlink()

    from scripts.auto_requeue import run
    out = run(dry_run=True)
    assert out['considered'] == 1
    assert out['requeued'] == 1
    # ensure files unchanged
    perm_data = json.loads(perm.read_text(encoding='utf-8'))
    assert len(perm_data) == 1


def test_auto_requeue_exec(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    perm = root / '.tmp' / 'telegram_queue_failed_permanent.json'
    failed = root / '.tmp' / 'telegram_queue_failed.json'
    perm.parent.mkdir(parents=True, exist_ok=True)

    item = {'action': 'send_message', '_retries': 0, '_failed_at': (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'}
    perm.write_text(json.dumps([item], indent=2), encoding='utf-8')
    if failed.exists():
        failed.unlink()

    from scripts.auto_requeue import run
    out = run(dry_run=False)
    assert out['requeued'] == 1
    # failed file should now contain the requeued item
    failed_data = json.loads(failed.read_text(encoding='utf-8'))
    assert len(failed_data) >= 1
    # perm should be empty
    perm_data = json.loads(perm.read_text(encoding='utf-8') or '[]')
    assert len(perm_data) == 0
