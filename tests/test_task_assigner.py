import json
import sys
import types
from types import SimpleNamespace

import pytest

from agents import task_assigner


def test_build_assignment():
    a = task_assigner.build_assignment('t1', 'alice', estimate='2d')
    assert a['task_id'] == 't1'
    assert a['assignee'] == 'alice'
    assert a['estimate'] == '2d'


def test_assign_task_emits_and_enqueue(tmp_path, monkeypatch):
    events = tmp_path / 'events.ndjson'
    monkeypatch.setattr(task_assigner, 'EVENTS_PATH', str(events))

    mod = types.ModuleType('orchestrator')
    mod.calls = []

    def enqueue_task(task_type, payload):
        mod.calls.append((task_type, payload))
        return 555

    mod.enqueue_task = enqueue_task
    monkeypatch.setitem(sys.modules, 'orchestrator', mod)

    args = SimpleNamespace(task_id='task-1', assignee='bob', estimate='1d', note=None, enqueue=True)
    rc = task_assigner.cmd_assign_task(args)
    assert rc == 0
    assert len(mod.calls) == 1
    text = events.read_text(encoding='utf-8').strip()
    lines = text.splitlines() if text else []
    assert len(lines) == 1
    ev = json.loads(lines[0])
    assert ev['type'] == 'task.assigned'
