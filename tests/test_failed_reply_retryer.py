import json
import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolate_fs(tmp_path, monkeypatch):
    # Redirect gaia events to tmp_path and process module paths
    import gaia.events as ge
    import scripts.process_telegram_queue as prq
    import scripts.telegram_client as tc

    monkeypatch.setattr(ge, 'EVENTS_FILE', tmp_path / 'events.ndjson')
    # adjust file locations used by the retry worker
    monkeypatch.setattr(prq, 'FAILED_FILE', tmp_path / '.tmp' / 'telegram_queue_failed.json')
    monkeypatch.setattr(prq, 'PERM_FAILED_FILE', tmp_path / '.tmp' / 'telegram_queue_failed_permanent.json')
    monkeypatch.setattr(prq, 'ENV_FILE', tmp_path / '.tmp' / 'telegram.env')
    # ensure token in env
    envf = prq.ENV_FILE
    envf.parent.mkdir(parents=True, exist_ok=True)
    envf.write_text('TELEGRAM_BOT_TOKEN=token-test\n', encoding='utf-8')

    yield


def test_retry_worker_succeeds_on_transient(monkeypatch, tmp_path):
    import scripts.process_telegram_queue as prq
    import scripts.telegram_client as tc

    # prepare failed file with one answer_callback item
    failed_item = {'action': 'answer_callback', 'callback_query_id': 'cb-1', 'update': {'update_id': 101}, '_retries': 0}
    prq.FAILED_FILE.parent.mkdir(parents=True, exist_ok=True)
    prq.FAILED_FILE.write_text(json.dumps([failed_item], indent=2), encoding='utf-8')

    # monkeypatch answer_callback to fail twice then succeed
    calls = {'n': 0}

    def fake_answer(token, cqid, text=None, show_alert=False, timeout=6):
        calls['n'] += 1
        if calls['n'] < 3:
            raise Exception('simulated transient error')
        return {'ok': True}

    monkeypatch.setattr(tc, 'answer_callback', fake_answer)

    out = prq.process_failed_items_once()
    assert out['processed'] == 1
    # succeeded should be 1 because worker will retry up to default attempts (3)
    assert out['succeeded'] == 1
    # permanent moved should be 0
    assert out['moved_permanent'] == 0

    # failed file should be empty now
    assert prq.FAILED_FILE.exists()
    data = json.loads(prq.FAILED_FILE.read_text(encoding='utf-8') or '[]')
    assert data == []

    # perm file should be empty
    assert prq.PERM_FAILED_FILE.exists()
    perm = json.loads(prq.PERM_FAILED_FILE.read_text(encoding='utf-8') or '[]')
    assert perm == []


def test_retry_worker_moves_permanent_on_bad_request(monkeypatch, tmp_path):
    import scripts.process_telegram_queue as prq
    import scripts.telegram_client as tc

    # prepare failed file with one answer_callback item
    failed_item = {'action': 'answer_callback', 'callback_query_id': 'cb-2', 'update': {'update_id': 102}, '_retries': 0}
    prq.FAILED_FILE.parent.mkdir(parents=True, exist_ok=True)
    prq.FAILED_FILE.write_text(json.dumps([failed_item], indent=2), encoding='utf-8')

    class FakeHTTPError(Exception):
        pass

    def fake_answer_bad(token, cqid, text=None, show_alert=False, timeout=6):
        # simulate a permanent bad request
        raise Exception('400 Bad Request')

    monkeypatch.setattr(tc, 'answer_callback', fake_answer_bad)

    out = prq.process_failed_items_once()
    assert out['processed'] == 1
    assert out['succeeded'] == 0
    assert out['moved_permanent'] == 1

    perm = json.loads(prq.PERM_FAILED_FILE.read_text(encoding='utf-8') or '[]')
    assert len(perm) == 1
    assert perm[0].get('callback_query_id') == 'cb-2'
