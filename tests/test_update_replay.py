import json
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
    import scripts.telegram_queue as tq

    monkeypatch.setattr(tcm, 'ROOT', tmp_path)
    monkeypatch.setattr(tcm, 'TMP', tmp_path / '.tmp')
    monkeypatch.setattr(tcm, 'PENDING', tmp_path / '.tmp' / 'pending_commands.json')
    monkeypatch.setattr(tcm, 'ENV_FILE', tmp_path / '.tmp' / 'telegram.env')
    monkeypatch.setattr(tcm, 'EVENTS', tmp_path / 'events.ndjson')
    monkeypatch.setattr(tcm, 'DB_PATH', tmp_path / 'gaia.db')

    # queue paths
    monkeypatch.setattr(tq, 'ROOT', tmp_path)
    monkeypatch.setattr(tq, 'Q_PATH', tmp_path / '.tmp' / 'telegram_queue.json')
    monkeypatch.setattr(tq, 'SEEN_PATH', tmp_path / '.tmp' / 'telegram_queue_seen.json')

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


def test_update_replay_skips_duplicate_callback(tmp_path):
    import scripts.tg_command_manager as tcm
    import scripts.telegram_idempotency as tid
    import scripts.telegram_queue as tq
    from gaia import events, db

    # prepare pending item
    item = make_item('cb-replay', tcm.now)
    tcm.safe_save(tcm.PENDING, [item])

    # two updates that represent the same callback_query but different update_ids (a replay)
    upd1 = {'update_id': 100, 'callback_query': {'id': 'cq-1', 'data': 'approve:cb-replay', 'from': {'id': 123}}}
    upd2 = {'update_id': 101, 'callback_query': {'id': 'cq-1', 'data': 'approve:cb-replay', 'from': {'id': 123}}}

    assert tq.append_dedup(upd1) is True
    assert tq.append_dedup(upd2) is True

    # drain the queue similar to approval_listener behavior
    while True:
        queued = tq.pop_next()
        if not queued:
            break
        callback = queued.get('callback_query')
        if callback:
            cqid = callback.get('id')
            # skip already-processed callback queries
            if cqid and tid.seen_callback(cqid):
                continue
            data = callback.get('data')
            from_id = (callback.get('from') or {}).get('id')
            if isinstance(data, str) and ':' in data:
                cmd, arg = data.split(':', 1)
                try:
                    if cmd == 'approve':
                        tcm.approve(arg, actor=from_id)
                        events.make_event('command.approved', {'id': arg, 'via': 'callback', 'by': from_id})
                        db.write_trace(action='command.approved', status='ok', details={'id': arg, 'by': from_id})
                except Exception:
                    pass
            # mark callback idempotent only after successful processing
            try:
                if cqid:
                    tid.mark_callback(cqid)
            except Exception:
                pass

    evs = read_events(tcm.EVENTS)
    matched = [e for e in evs if e.get('type') == 'command.approved' and e.get('payload', {}).get('id') == 'cb-replay']
    assert len(matched) == 1

    rows = read_audit_rows(tcm.DB_PATH, 'cb-replay')
    approved_rows = [r for r in rows if r[1] == 'approved']
    assert len(approved_rows) == 1
