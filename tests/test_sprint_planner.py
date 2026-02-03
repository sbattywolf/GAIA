import json
import sys
import types
from types import SimpleNamespace

import pytest

from agents import sprint_planner


def test_build_task_from_story_minimal():
    story = {'id': 's1', 'title': 'Do thing'}
    t = sprint_planner.build_task_from_story(story, 'S1')
    assert t['story_id'] == 's1'
    assert t['sprint'] == 'S1'


def test_plan_sprint_emits_and_enqueue(tmp_path, monkeypatch):
    events = tmp_path / 'events.ndjson'
    monkeypatch.setattr(sprint_planner, 'EVENTS_PATH', str(events))

    stories = [{'id': 's2', 'title': 'Do other'}]
    sf = tmp_path / 'stories.json'
    sf.write_text(json.dumps(stories), encoding='utf-8')

    mod = types.ModuleType('orchestrator')
    mod.calls = []

    def enqueue_task(task_type, payload):
        mod.calls.append((task_type, payload))
        return 123

    mod.enqueue_task = enqueue_task
    monkeypatch.setitem(sys.modules, 'orchestrator', mod)

    args = SimpleNamespace(name='Sprint1', start='2026-02-02', end='2026-02-16', stories_file=str(sf), enqueue=True)
    rc = sprint_planner.cmd_plan_sprint(args)
    assert rc == 0
    assert len(mod.calls) == 1
    text = events.read_text(encoding='utf-8').strip()
    lines = text.splitlines() if text else []
    assert len(lines) == 1
    ev = json.loads(lines[0])
    assert ev['type'] == 'sprint.task.created'
