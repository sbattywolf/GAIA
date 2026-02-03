import os
from pathlib import Path
from datetime import datetime, timedelta
import orchestrator
from agents import reclaimer


def test_reclaimer_cli_once(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_reclaim_cli.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    orchestrator.DB_PATH = str(db)
    orchestrator.init_db()

    tid = orchestrator.enqueue_task('job', {'cmd': 'echo x'})
    task = orchestrator.claim_task('wx')
    assert task and task['id'] == tid

    # backdate started_at
    old = (datetime.utcnow() - timedelta(seconds=3600)).isoformat() + 'Z'
    conn = orchestrator._connect()
    cur = conn.cursor()
    cur.execute('UPDATE queue SET started_at = ? WHERE id = ?', (old, tid))
    conn.commit()
    conn.close()

    # run reclaimer once
    rc = reclaimer.main(['--ttl', '60', '--once'])
    assert rc == 0

    pend = orchestrator.list_tasks('pending')
    assert any(t['id'] == tid for t in pend)
