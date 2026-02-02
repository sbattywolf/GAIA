#!/usr/bin/env python3
"""GAIA BacklogAgent (prototype).

Usage:
  python agents/backlog_agent.py --title "Issue title" --body "Issue body"

This script calls the `gh` (GitHub CLI) if available to create an issue, and
appends an NDJSON event to `events.ndjson` in the repo root.
"""
import subprocess
import json
import argparse
import os
import uuid
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
EVENTS_PATH = os.path.join(ROOT, 'events.ndjson')


def gh_create_issue(title, body):
    """Attempt to create an issue with `gh`. Returns the issue URL or None."""
    try:
        cmd = ['gh', 'issue', 'create', '--title', title, '--body', body]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # gh prints URL on success
        output = proc.stdout.strip()
        return output
    except Exception as e:
        print('gh issue create failed:', e)
        return None


def append_event(event):
    with open(EVENTS_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--body', default='')
    args = p.parse_args()

    issue_url = gh_create_issue(args.title, args.body)

    event = {
        'type': 'issue.create',
        'source': 'backlog_agent',
        'target': os.path.basename(os.getcwd()),
        'task_id': None,
        'payload': {
            'title': args.title,
            'body': args.body,
            'issue_url': issue_url,
        },
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'trace_id': str(uuid.uuid4()),
    }

    append_event(event)
    print('event appended to', EVENTS_PATH)


if __name__ == '__main__':
    main()
