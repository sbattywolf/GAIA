import os
import json
from pathlib import Path
from datetime import datetime, timedelta

import orchestrator


def test_reclaim_stale_tasks(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_reclaim.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    orchestrator.DB_PATH = str(db)
    orchestrator.init_db()

    # enqueue and claim a task
    tid = orchestrator.enqueue_task('job', {'cmd': 'echo x'})
    task = orchestrator.claim_task('workerX')
    assert task and task['id'] == tid

    # mark started_at as far in the past
    old = (datetime.utcnow() - timedelta(seconds=3600)).isoformat() + 'Z'
    conn = orchestrator._connect()
    cur = conn.cursor()
    cur.execute('UPDATE queue SET started_at = ? WHERE id = ?', (old, tid))
    conn.commit()
    conn.close()

    # reclaim tasks older than 60s
    reclaimed = orchestrator.reclaim_stale_tasks(60)
    assert reclaimed >= 1

    # ensure task is pending again
    pendings = orchestrator.list_tasks('pending')
    assert any(t['id'] == tid for t in pendings)


def test_reclaim_backoff_exceeds(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_reclaim2.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    orchestrator.DB_PATH = str(db)
    orchestrator.init_db()

    # enqueue and claim a task
    tid = orchestrator.enqueue_task('job', {'cmd': 'echo x'})
    task = orchestrator.claim_task('workerB')
    assert task and task['id'] == tid

    # backdate started_at and set reclaim_attempts high
    old = (datetime.utcnow() - timedelta(seconds=3600)).isoformat() + 'Z'
    conn = orchestrator._connect()
    cur = conn.cursor()
    cur.execute('UPDATE queue SET started_at = ?, reclaim_attempts = ? WHERE id = ?', (old, 3, tid))
    conn.commit()
    conn.close()

    reclaimed = orchestrator.reclaim_stale_tasks(60)
    # should not be reclaimed (moved to failed instead)
    assert reclaimed == 0

    failed = orchestrator.list_tasks('failed')
    assert any(t['id'] == tid for t in failed)

    # ensure audit contains reclaim_failed entry
    conn = orchestrator._connect()
    cur = conn.cursor()
    cur.execute("SELECT action, details FROM audit WHERE action IN ('reclaim', 'reclaim_failed')")
    rows = cur.fetchall()
    conn.close()
    assert any(r[0] == 'reclaim_failed' for r in rows)
