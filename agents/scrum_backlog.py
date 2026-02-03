#!/usr/bin/env python3
"""Scrum backlog importer/normalizer agent.

Usage:
  python -m agents.scrum_backlog import-file --file path/to/backlog.json [--enqueue]

Behavior:
- Reads a JSON file containing either a single story or a list of stories.
- Normalizes fields to a standard shape: id, title, description, priority, tags, created_at.
- Emits `story.normalized` events to `events.ndjson` for each normalized story.
- If `--enqueue` is provided and `orchestrator` is importable, creates an orchestrator task for follow-up work.

This is intentionally minimal; extend with validation, schema checks, and debouncing as needed.
"""

import argparse
import json
import os
import uuid
from datetime import datetime

from agents import agent_utils

EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', 'events.ndjson')
SOURCE = os.path.basename(os.getcwd())


def normalize_story(raw: dict) -> dict:
    s = {}
    s['id'] = raw.get('id') or raw.get('story_id') or str(uuid.uuid4())
    s['title'] = raw.get('title') or raw.get('name') or 'Untitled'
    s['description'] = raw.get('description') or raw.get('desc') or raw.get('body') or ''
    s['priority'] = raw.get('priority') or raw.get('prio') or 'medium'
    tags = raw.get('tags') or raw.get('labels') or []
    s['tags'] = tags if isinstance(tags, list) else [t.strip() for t in str(tags).split(',') if t.strip()]
    s['created_at'] = raw.get('created_at') or datetime.utcnow().isoformat() + 'Z'
    s['source'] = raw.get('source') or SOURCE
    return s


def emit_normalized(story: dict):
    ev = agent_utils.build_event('story.normalized', SOURCE, {'story': story})
    agent_utils.append_event_atomic(EVENTS_PATH, ev)
    return ev


def maybe_enqueue(story: dict):
    try:
        import orchestrator
    except Exception:
        return None
    try:
        tid = orchestrator.enqueue_task('create-ticket', {'story': story})
        return tid
    except Exception:
        return None


def cmd_import_file(args):
    p = args.file
    if not os.path.exists(p):
        print('file not found', p)
        return 2
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items = data if isinstance(data, list) else [data]
    results = []
    for raw in items:
        story = normalize_story(raw)
        ev = emit_normalized(story)
        rec = {'story_id': story['id'], 'event': ev['trace_id']}
        if args.enqueue:
            tid = maybe_enqueue(story)
            rec['task_id'] = tid
        results.append(rec)
        print('normalized', story['id'])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='scrum-backlog')
    sp = p.add_subparsers(dest='cmd')

    p_import = sp.add_parser('import-file')
    p_import.add_argument('--file', required=True)
    p_import.add_argument('--enqueue', action='store_true', help='Create orchestrator tasks for follow-up')
    p_import.set_defaults(func=cmd_import_file)

    args = p.parse_args(argv)
    if not hasattr(args, 'func'):
        p.print_help()
        return 2
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
