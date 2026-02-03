import json
import os
import sqlite3
from pathlib import Path

import pytest


def make_item(id_, now_fn, command='echo hi', exec_request=True, status='pending'):
    return {
        'id': id_,
        'chat_id': 'test_chat',
        'message_id': 'm1',
        'command': command,
        'from': {'first_name': 'tester'},
        'status': status,
        'created': now_fn(),
        'options': {'exec_request': exec_request},
    }


@pytest.fixture(autouse=True)
def isolate_fs(tmp_path, monkeypatch):
    # import modules then redirect their paths to tmp_path
    import scripts.tg_command_manager as tcm
    import scripts.telegram_idempotency as tid

    monkeypatch.setattr(tcm, 'ROOT', tmp_path)
    monkeypatch.setattr(tcm, 'TMP', tmp_path / '.tmp')
    monkeypatch.setattr(tcm, 'PENDING', tmp_path / '.tmp' / 'pending_commands.json')
    monkeypatch.setattr(tcm, 'ENV_FILE', tmp_path / '.tmp' / 'telegram.env')
    monkeypatch.setattr(tcm, 'EVENTS', tmp_path / 'events.ndjson')
    monkeypatch.setattr(tcm, 'DB_PATH', tmp_path / 'gaia.db')

    # idempotency path
    monkeypatch.setattr(tid, 'SEEN_PATH', tmp_path / '.tmp' / 'telegram_idempotency.json')

    # re-init DB at the new location
    try:
        tcm._init_db()
    except Exception:
        pass
    yield


def read_events(path: Path):
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


def read_audit_rows(dbpath: Path, command_id: str):
    conn = sqlite3.connect(str(dbpath))
    cur = conn.cursor()
    cur.execute('SELECT command_id, action, details FROM command_audit WHERE command_id = ?', (command_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def test_callback_approve_emits_event_and_audit(tmp_path):
    import scripts.tg_command_manager as tcm
    import scripts.telegram_idempotency as tid

    # prepare pending item
    item = make_item('cb-1', tcm.now)
    tcm.safe_save(tcm.PENDING, [item])

    # process as if callback approve pressed
    res = tcm.approve('cb-1', actor='user-42')
    assert res is not None
    assert res['status'] == 'approved'

    evs = read_events(tcm.EVENTS)
    assert any(e.get('type') == 'command.approved' and e.get('payload', {}).get('id') == 'cb-1' for e in evs)

    rows = read_audit_rows(tcm.DB_PATH, 'cb-1')
    assert any(r[1] == 'approved' for r in rows)


def test_double_callback_is_idempotent(tmp_path):
    import scripts.tg_command_manager as tcm
    import scripts.telegram_idempotency as tid

    # prepare pending item
    item = make_item('cb-dup', tcm.now)
    tcm.safe_save(tcm.PENDING, [item])

    # simulate first callback processing
    res1 = tcm.approve('cb-dup', actor='user-1')
    assert res1 is not None

    # second callback (duplicate) should not create new event/audit
    res2 = tcm.approve('cb-dup', actor='user-1')
    assert res2 is not None

    evs = read_events(tcm.EVENTS)
    matched = [e for e in evs if e.get('type') == 'command.approved' and e.get('payload', {}).get('id') == 'cb-dup']
    assert len(matched) == 1

    rows = read_audit_rows(tcm.DB_PATH, 'cb-dup')
    approved_rows = [r for r in rows if r[1] == 'approved']
    assert len(approved_rows) == 1
