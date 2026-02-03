import os
import json
from pathlib import Path

import sqlite3

import orchestrator


def test_enqueue_claim_complete(tmp_path, monkeypatch):
    db = tmp_path / 'gaia_test.db'
    monkeypatch.setenv('GAIA_DB_PATH', str(db))
    # point orchestrator DB_PATH to our test DB file
    orchestrator.DB_PATH = str(db)
    # initialize
    orchestrator.init_db()

    # enqueue two tasks
    t1 = orchestrator.enqueue_task('job', {'cmd': 'echo 1'})
    t2 = orchestrator.enqueue_task('job', {'cmd': 'echo 2'})
    assert t1 and t2 and t2 > t1

    # claim with worker A
    task = orchestrator.claim_task('workerA')
    assert task is not None
    assert task['task_type'] == 'job'

    # claim with worker B should get the next task
    task2 = orchestrator.claim_task('workerB')
    assert task2 is not None
    assert task2['id'] != task['id']

    # no more tasks
    none = orchestrator.claim_task('workerC')
    assert none is None

    # complete first task
    orchestrator.complete_task(task['id'], {'rc': 0})
    # fail second task
    orchestrator.fail_task(task2['id'], 'error')

    # list tasks by status
    completed = orchestrator.list_tasks('completed')
    failed = orchestrator.list_tasks('failed')
    assert any(t['id'] == task['id'] for t in completed)
    assert any(t['id'] == task2['id'] for t in failed)
