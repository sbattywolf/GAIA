import json
import sqlite3
import sys
from pathlib import Path

print('PYTHONPATH at start:', sys.path)

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

# Ensure absolute path for clarity
sys.path.insert(0, 'E:/Workspaces/Git/GAIA/scripts')

sys.path.append(str(Path(__file__).resolve().parents[2] / 'scripts'))

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
    import scripts.tg_command_manager as tcm
    import scripts.telegram_queue as tq

    monkeypatch.setattr(tcm, 'ROOT', tmp_path)
    monkeypatch.setattr(tcm, 'TMP', tmp_path / '.tmp')
    monkeypatch.setattr(tcm, 'PENDING', tmp_path / '.tmp' / 'pending_commands.json')
    monkeypatch.setattr(tcm, 'ENV_FILE', tmp_path / '.tmp' / 'telegram.env')
    monkeypatch.setattr(tcm, 'EVENTS', tmp_path / 'events.ndjson')
    monkeypatch.setattr(tcm, 'DB_PATH', tmp_path / 'gaia.db')

    monkeypatch.setattr(tq, 'ROOT', tmp_path)
    monkeypatch.setattr(tq, 'Q_PATH', tmp_path / '.tmp' / 'telegram_queue.json')
    monkeypatch.setattr(tq, 'SEEN_PATH', tmp_path / '.tmp' / 'telegram_queue_seen.json')

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


def test_text_approve_replay_skips_duplicate(tmp_path):
    import scripts.tg_command_manager as tcm
    import scripts.telegram_queue as tq
    from gaia import events, db

    # prepare pending item (use hex-like id so listener regex matches)
    item = make_item('abc123', tcm.now)
    tcm.safe_save(tcm.PENDING, [item])

    # load fixture (message body) and create two updates with different update_ids
    fx = Path(__file__).parent / 'fixtures' / 'text_approve.json'
    base = json.loads(fx.read_text(encoding='utf-8'))
    upd1 = {'update_id': 210, **base}
    upd2 = {'update_id': 211, **base}

    assert tq.append_dedup(upd1) is True
    assert tq.append_dedup(upd2) is True

    # drain and process like approval_listener: textual approve
    while True:
        queued = tq.pop_next()
        if not queued:
            break
        msg = queued.get('message') or queued.get('channel_post')
        if not msg:
            continue
        text = msg.get('text', '') or ''
        from_id = (msg.get('from') or {}).get('id') or (msg.get('chat') or {}).get('id')
        # simple regex as in listener
        import re

        explicit = re.search(r'\b(?:/)?(approve|deny)\s+([0-9a-fA-F\-]{6,})\b', text, re.IGNORECASE)
        if explicit:
            verb = explicit.group(1).lower()
            cmd_id = explicit.group(2)
            try:
                if verb == 'approve':
                    tcm.approve(cmd_id, actor=from_id)
                    events.make_event('command.approved', {'id': cmd_id, 'via': 'text', 'by': from_id})
                    db.write_trace(action='command.approved', status='ok', details={'id': cmd_id, 'by': from_id})
            except Exception:
                pass

    evs = read_events(tcm.EVENTS)
    matched = [e for e in evs if e.get('type') == 'command.approved' and e.get('payload', {}).get('id') == 'abc123']
    assert len(matched) == 1

    rows = read_audit_rows(tcm.DB_PATH, 'abc123')
    approved_rows = [r for r in rows if r[1] == 'approved']
    assert len(approved_rows) == 1
