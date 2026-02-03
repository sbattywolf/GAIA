#!/usr/bin/env python3
"""Sprint planner agent.

Usage:
  python -m agents.sprint_planner plan-sprint --name NAME --start YYYY-MM-DD --end YYYY-MM-DD --stories-file stories.json [--enqueue]

Behavior:
- Reads a JSON file of normalized stories (list of story dicts).
- For each story, creates a sprint task payload and emits `sprint.task.created` events.
- Optionally enqueues work in `orchestrator.enqueue_task('sprint-task', payload)` when `--enqueue` is set.
"""

import argparse
import json
import os
import uuid
from datetime import datetime

from agents import agent_utils

EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', 'events.ndjson')
SOURCE = os.path.basename(os.getcwd())


def build_task_from_story(story, sprint_name):
    task = {
        'task_id': str(uuid.uuid4()),
        'story_id': story.get('id'),
        'title': f"{story.get('title')}",
        'description': story.get('description', ''),
        'sprint': sprint_name,
        'estimate': story.get('estimate', '1d'),
        'assignee': None,
        'created_at': datetime.utcnow().isoformat() + 'Z',
    }
    return task


def emit_task_event(task):
    ev = agent_utils.build_event('sprint.task.created', SOURCE, {'task': task})
    agent_utils.append_event_atomic(EVENTS_PATH, ev)
    return ev


def maybe_enqueue(task):
    try:
        import orchestrator
    except Exception:
        return None
    try:
        tid = orchestrator.enqueue_task('sprint-task', {'task': task})
        return tid
    except Exception:
        return None


def cmd_plan_sprint(args):
    sf = args.stories_file
    if not os.path.exists(sf):
        print('stories file not found', sf)
        return 2
    with open(sf, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    results = []
    for s in stories:
        task = build_task_from_story(s, args.name)
        ev = emit_task_event(task)
        rec = {'task_id': task['task_id'], 'event': ev['trace_id']}
        if args.enqueue:
            tid = maybe_enqueue(task)
            rec['orchestrator_task_id'] = tid
        results.append(rec)
        print('created task', task['task_id'])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='sprint-planner')
    sp = p.add_subparsers(dest='cmd')

    p_plan = sp.add_parser('plan-sprint')
    p_plan.add_argument('--name', required=True)
    p_plan.add_argument('--start', required=True)
    p_plan.add_argument('--end', required=True)
    p_plan.add_argument('--stories-file', required=True)
    p_plan.add_argument('--enqueue', action='store_true')
    p_plan.set_defaults(func=cmd_plan_sprint)

    args = p.parse_args(argv)
    if not hasattr(args, 'func'):
        p.print_help()
        return 2
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
