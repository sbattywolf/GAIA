import json
import sys
import types
from types import SimpleNamespace

import pytest

from agents import scrum_backlog


def test_normalize_story_minimal():
    raw = {}
    s = scrum_backlog.normalize_story(raw)
    assert 'id' in s
    assert s['title'] == 'Untitled'
    assert s['priority'] == 'medium'
    assert isinstance(s['tags'], list)


def test_import_file_emits_events(tmp_path, monkeypatch):
    events = tmp_path / 'events.ndjson'
    monkeypatch.setattr(scrum_backlog, 'EVENTS_PATH', str(events))

    data = [
        {'title': 'A', 'description': 'd1'},
        {'title': 'B', 'desc': 'd2'},
    ]
    f = tmp_path / 'in.json'
    f.write_text(json.dumps(data), encoding='utf-8')

    args = SimpleNamespace(file=str(f), enqueue=False)
    rc = scrum_backlog.cmd_import_file(args)
    assert rc == 0

    text = events.read_text(encoding='utf-8').strip()
    lines = text.splitlines() if text else []
    assert len(lines) == 2
    ev0 = json.loads(lines[0])
    assert ev0['type'] == 'story.normalized'
    assert ev0['payload']['story']['title'] == 'A'


def test_import_with_enqueue_calls_orchestrator(tmp_path, monkeypatch):
    events = tmp_path / 'events.ndjson'
    monkeypatch.setattr(scrum_backlog, 'EVENTS_PATH', str(events))

    data = [{'title': 'X'}]
    f = tmp_path / 'in2.json'
    f.write_text(json.dumps(data), encoding='utf-8')

    mod = types.ModuleType('orchestrator')
    mod.calls = []

    def enqueue_task(task_type, payload):
        mod.calls.append((task_type, payload))
        return 999

    mod.enqueue_task = enqueue_task
    monkeypatch.setitem(sys.modules, 'orchestrator', mod)

    args = SimpleNamespace(file=str(f), enqueue=True)
    rc = scrum_backlog.cmd_import_file(args)
    assert rc == 0
    assert len(mod.calls) == 1
    task_type, payload = mod.calls[0]
    assert task_type == 'create-ticket'
    assert 'story' in payload
