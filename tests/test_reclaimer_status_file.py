import os
import json
from pathlib import Path
import orchestrator
from agents import reclaimer


def test_reclaimer_writes_status_file(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_reclaim_status.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    orchestrator.DB_PATH = str(db)
    orchestrator.init_db()

    tid = orchestrator.enqueue_task('job', {'cmd': 'echo x'})
    task = orchestrator.claim_task('workerS')
    assert task and task['id'] == tid

    # backdate to make it stale
    from datetime import datetime, timedelta
    old = (datetime.utcnow() - timedelta(seconds=3600)).isoformat() + 'Z'
    conn = orchestrator._connect()
    cur = conn.cursor()
    cur.execute('UPDATE queue SET started_at = ? WHERE id = ?', (old, tid))
    conn.commit()
    conn.close()

    status = tmp_path / 'reclaim_status.json'
    rc = reclaimer.main(['--ttl', '60', '--once', '--reclaim-max-attempts', '2', '--status-file', str(status)])
    assert rc == 0
    assert status.exists()
    data = json.loads(status.read_text(encoding='utf-8'))
    assert 'reclaimed' in data and 'pending' in data
