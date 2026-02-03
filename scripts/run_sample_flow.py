#!/usr/bin/env python3
"""Run a sample flow: backlog -> sprint planning -> task assignment.

Reads `examples/sample_backlog.json`, runs `agents.scrum_backlog` import,
then runs `agents.sprint_planner` to create tasks, then assigns tasks via
`agents.task_assigner`. Emits/reads events from `events.ndjson` in repo root.
"""
import json
import os
from types import SimpleNamespace

import importlib.util
import sys


def load_agent(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


REPO_ROOT = os.path.abspath(os.path.dirname(__file__) + os.sep + '..')
sys.path.insert(0, REPO_ROOT)
EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', os.path.join(REPO_ROOT, 'events.ndjson'))
EXAMPLE = os.path.join(REPO_ROOT, 'examples', 'sample_backlog.json')
STORIES_FILE = os.path.join(REPO_ROOT, 'examples', 'stories.json')

AGENTS_DIR = os.path.join(REPO_ROOT, 'agents')
scrum_backlog = load_agent(os.path.join(AGENTS_DIR, 'scrum_backlog.py'), 'scrum_backlog')
sprint_planner = load_agent(os.path.join(AGENTS_DIR, 'sprint_planner.py'), 'sprint_planner')
task_assigner = load_agent(os.path.join(AGENTS_DIR, 'task_assigner.py'), 'task_assigner')

# Ensure agents write/read the same events file
scrum_backlog.EVENTS_PATH = EVENTS_PATH
sprint_planner.EVENTS_PATH = EVENTS_PATH
task_assigner.EVENTS_PATH = EVENTS_PATH

ASSIGNEES = ['alice', 'bob', 'carol']


def read_events_of_type(ev_type):
    if not os.path.exists(EVENTS_PATH):
        return []
    outs = []
    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get('type') == ev_type:
                outs.append(ev)
    return outs


def main():
    print('running sample backlog import -> sprint -> assign flow')

    # 1) import backlog
    print('importing', EXAMPLE)
    args = SimpleNamespace(file=EXAMPLE, enqueue=False)
    rc = scrum_backlog.cmd_import_file(args)
    if rc != 0:
        print('import failed', rc)
        return rc

    # 2) collect normalized stories from events and write stories.json
    stories_ev = read_events_of_type('story.normalized')
    stories = [ev['payload']['story'] for ev in stories_ev]
    with open(STORIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(stories, f, indent=2)
    print('collected', len(stories), 'normalized stories')

    # 3) plan sprint
    plan_args = SimpleNamespace(name='sprint-1', start='2026-02-02', end='2026-02-16', stories_file=STORIES_FILE, enqueue=False)
    rc = sprint_planner.cmd_plan_sprint(plan_args)
    if rc != 0:
        print('planning failed', rc)
        return rc

    tasks_ev = read_events_of_type('sprint.task.created')
    tasks = [ev['payload']['task'] for ev in tasks_ev]
    print('created', len(tasks), 'sprint tasks')

    # 4) assign tasks round-robin
    for i, t in enumerate(tasks):
        assignee = ASSIGNEES[i % len(ASSIGNEES)]
        aargs = SimpleNamespace(task_id=t['task_id'], assignee=assignee, estimate=t.get('estimate'), note=None, enqueue=False)
        task_assigner.cmd_assign_task(aargs)
    assigned_ev = read_events_of_type('task.assigned')
    print('assigned', len(assigned_ev), 'tasks')

    print('\nsummary:')
    print('- stories imported:', len(stories))
    print('- tasks created:', len(tasks))
    print('- tasks assigned:', len(assigned_ev))
    print('events path:', EVENTS_PATH)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
