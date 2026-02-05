import os
import tempfile
import json
from pathlib import Path
import orchestrator


def test_write_approval_creates_row(tmp_path: Path):
    # use temp DB path
    dbpath = tmp_path / 'gaia.db'
    # monkeypatch DB_PATH by setting environment variable for test run
    # orchestrator uses relative path; copy module and adjust DB_PATH
    orchestrator.DB_PATH = str(dbpath)
    # ensure DB initialized
    orchestrator.init_db()

    ev = {
        'type': 'approval.request',
        'task_id': 'task-xyz',
        'request_id': 'r-123',
        'trace_id': 't-abc',
        'payload': {'foo': 'bar'},
        'timestamp': '2026-02-05T10:00:00Z'
    }

    orchestrator.write_approval(ev)

    # verify row exists
    conn = orchestrator._connect()
    cur = conn.cursor()
    cur.execute('SELECT event_type, task_id, request_id, trace_id, payload FROM approvals')
    rows = cur.fetchall()
    conn.close()
    assert len(rows) == 1
    et, task_id, request_id, trace_id, payload = rows[0]
    assert et == 'approval.request'
    assert task_id == 'task-xyz'
    assert request_id == 'r-123'
    assert trace_id == 't-abc'
    payload_obj = json.loads(payload)
    assert payload_obj.get('foo') == 'bar'
