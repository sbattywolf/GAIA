import os
import json
from pathlib import Path

import orchestrator
from agents import worker


def test_worker_claims_and_runs_job(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_worker.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    orchestrator.DB_PATH = str(db)
    orchestrator.init_db()

    # enqueue a job task
    tid = orchestrator.enqueue_task('job', {'cmd': 'echo test_worker'})

    # run worker once
    rc = worker.main(['--worker-id', 'w1', '--once'])
    assert rc == 0

    # ensure task is completed
    completed = orchestrator.list_tasks('completed')
    assert any(t['id'] == tid for t in completed)
