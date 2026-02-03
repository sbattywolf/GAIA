import os
import json
import time
import threading
import socket
from pathlib import Path

import orchestrator
from agents import worker


def _find_free_port():
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    p = s.getsockname()[1]
    s.close()
    return p


def test_worker_max_jobs_and_health(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_worker2.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    orchestrator.DB_PATH = str(db)
    orchestrator.init_db()

    # enqueue 3 short jobs that sleep briefly
    orchestrator.enqueue_task('job', {'cmd': 'python -c "import time; time.sleep(0.2); print(1)"'})
    orchestrator.enqueue_task('job', {'cmd': 'python -c "import time; time.sleep(0.2); print(2)"'})
    orchestrator.enqueue_task('job', {'cmd': 'python -c "import time; time.sleep(0.2); print(3)"'})

    port = _find_free_port()

    # run worker in a thread for a short duration with max-jobs=2 and health port
    def run_worker():
        worker.main(['--worker-id', 'w2', '--max-jobs', '2', '--health-port', str(port), '--run-duration', '2'])

    t = threading.Thread(target=run_worker)
    t.start()

    # allow worker to start and then query health
    time.sleep(0.5)
    import urllib.request
    with urllib.request.urlopen(f'http://127.0.0.1:{port}/health') as r:
        data = json.loads(r.read().decode('utf-8'))
        assert data['worker_id'] == 'w2'
        assert 'uptime' in data

    t.join(timeout=5)

    # ensure all tasks completed
    completed = orchestrator.list_tasks('completed')
    assert len(completed) == 3
