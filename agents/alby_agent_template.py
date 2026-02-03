#!/usr/bin/env python3
"""Minimal Alby-based Scrum agent template.

Commands:
  create-story --title "..." --desc "..."
  split-story --story-id ID --parts N
  plan-sprint --name NAME --start YYYY-MM-DD --end YYYY-MM-DD
  assign-task --task-id ID --assignee NAME

This template emits NDJSON events to `events.ndjson` (or path from env GAIA_EVENTS_PATH).
It uses `agents.agent_utils.build_event` and `append_event_atomic`.

Copy or extend this file when implementing concrete agents.
"""

import argparse
import json
import os
from datetime import datetime
from agents import agent_utils

EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', 'events.ndjson')
SOURCE = os.path.basename(os.getcwd())


def write_event(ev_type, payload, task_id=None):
    ev = agent_utils.build_event(ev_type, SOURCE, payload, task_id=task_id)
    agent_utils.append_event_atomic(EVENTS_PATH, ev)
    return ev


def cmd_create_story(args):
    payload = {
        'title': args.title,
        'description': args.desc,
        'created_at': datetime.utcnow().isoformat() + 'Z',
        'meta': {'source': SOURCE},
    }
    ev = write_event('story.created', payload)
    print('emitted', ev['type'], ev['trace_id'])


def cmd_split_story(args):
    payload = {'story_id': args.story_id, 'parts': args.parts}
    ev = write_event('story.split', payload)
    print('emitted', ev['type'], ev['trace_id'])


def cmd_plan_sprint(args):
    payload = {
        'name': args.name,
        'start': args.start,
        'end': args.end,
        'created_at': datetime.utcnow().isoformat() + 'Z',
    }
    ev = write_event('sprint.planned', payload)
    print('emitted', ev['type'], ev['trace_id'])


def cmd_assign_task(args):
    payload = {'task_id': args.task_id, 'assignee': args.assignee}
    ev = write_event('task.assigned', payload)
    print('emitted', ev['type'], ev['trace_id'])


def main(argv=None):
    p = argparse.ArgumentParser(prog='alby-agent-template')
    sp = p.add_subparsers(dest='cmd')

    p_create = sp.add_parser('create-story')
    p_create.add_argument('--title', required=True)
    p_create.add_argument('--desc', default='')
    p_create.set_defaults(func=cmd_create_story)

    p_split = sp.add_parser('split-story')
    p_split.add_argument('--story-id', required=True)
    p_split.add_argument('--parts', type=int, default=2)
    p_split.set_defaults(func=cmd_split_story)

    p_plan = sp.add_parser('plan-sprint')
    p_plan.add_argument('--name', required=True)
    p_plan.add_argument('--start', required=True)
    p_plan.add_argument('--end', required=True)
    p_plan.set_defaults(func=cmd_plan_sprint)

    p_assign = sp.add_parser('assign-task')
    p_assign.add_argument('--task-id', required=True)
    p_assign.add_argument('--assignee', required=True)
    p_assign.set_defaults(func=cmd_assign_task)

    args = p.parse_args(argv)
    if not hasattr(args, 'func'):
        p.print_help()
        return 2
    args.func(args)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
