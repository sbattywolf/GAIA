import os
import tempfile
import json
from pathlib import Path
import importlib.util
import sys


def load_orchestrator_module(tmp_path: Path):
    spec = importlib.util.spec_from_file_location('orchestrator', str(Path('orchestrator.py').resolve()))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # set DB path to a temp file for isolation
    mod.DB_PATH = str(tmp_path / 'gaia.db')
    return mod


def test_write_approval_creates_row(tmp_path: Path):
    orchestrator = load_orchestrator_module(tmp_path)
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
