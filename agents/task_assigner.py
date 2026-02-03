#!/usr/bin/env python3
"""Task assigner agent.

Responsibilities:
- Assign a task to a person or team member.
- Emit `task.assigned` events to the event stream.
- Optionally create an orchestrator work item to execute the task.

Usage:
  python -m agents.task_assigner assign-task --task-id ID --assignee NAME [--estimate 1d] [--enqueue]
  python -m agents.task_assigner assign-from-file --file tasks.json [--enqueue]
"""

import argparse
import json
import os
from datetime import datetime
from typing import Optional

from agents import agent_utils

EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', 'events.ndjson')
SOURCE = os.path.basename(os.getcwd())


def build_assignment(task_id: str, assignee: str, estimate: Optional[str] = None, note: Optional[str] = None) -> dict:
    return {
        'assignment_id': f"asgn-{task_id}-{assignee}" if task_id and assignee else task_id,
        'task_id': task_id,
        'assignee': assignee,
        'estimate': estimate,
        'note': note,
        'assigned_at': datetime.utcnow().isoformat() + 'Z',
        'source': SOURCE,
    }


def emit_assignment_event(assignment: dict):
    ev = agent_utils.build_event('task.assigned', SOURCE, {'assignment': assignment})
    agent_utils.append_event_atomic(EVENTS_PATH, ev)
    return ev


def maybe_enqueue_orchestrator(assignment: dict):
    try:
        import orchestrator
    except Exception:
        return None
    try:
        tid = orchestrator.enqueue_task('execute-task', {'assignment': assignment})
        return tid
    except Exception:
        return None


def cmd_assign_task(args):
    assignment = build_assignment(args.task_id, args.assignee, estimate=args.estimate, note=args.note)
    ev = emit_assignment_event(assignment)
    print('emitted', ev['type'], ev['trace_id'])
    result = {'event_trace': ev['trace_id']}
    if args.enqueue:
        tid = maybe_enqueue_orchestrator(assignment)
        result['orchestrator_task_id'] = tid
        print('enqueued', tid)
    return 0


def cmd_assign_from_file(args):
    p = args.file
    if not os.path.exists(p):
        print('file not found', p)
        return 2
    with open(p, 'r', encoding='utf-8') as f:
        data = json.load(f)
    items = data if isinstance(data, list) else [data]
    for it in items:
        task_id = it.get('task_id') or it.get('id')
        assignee = it.get('assignee')
        estimate = it.get('estimate')
        note = it.get('note')
        aargs = argparse.Namespace(task_id=task_id, assignee=assignee, estimate=estimate, note=note, enqueue=args.enqueue)
        rc = cmd_assign_task(aargs)
        if rc != 0:
            return rc
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='task-assigner')
    sp = p.add_subparsers(dest='cmd')

    p_assign = sp.add_parser('assign-task')
    p_assign.add_argument('--task-id', required=True)
    p_assign.add_argument('--assignee', required=True)
    p_assign.add_argument('--estimate', default=None)
    p_assign.add_argument('--note', default=None)
    p_assign.add_argument('--enqueue', action='store_true')
    p_assign.set_defaults(func=cmd_assign_task)

    p_file = sp.add_parser('assign-from-file')
    p_file.add_argument('--file', required=True)
    p_file.add_argument('--enqueue', action='store_true')
    p_file.set_defaults(func=cmd_assign_from_file)

    args = p.parse_args(argv)
    if not hasattr(args, 'func'):
        p.print_help()
        return 2
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
