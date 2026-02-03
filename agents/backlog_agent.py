#!/usr/bin/env python3
"""GAIA BacklogAgent (prototype).

Usage:
  python agents/backlog_agent.py --title "Issue title" --body "Issue body" [--dry-run]

Pattern: build an event, optionally call `gh`, then append event to `events.ndjson`.
"""
import subprocess
import argparse
import os
import uuid
from datetime import datetime

from .agent_utils import build_event, append_event_atomic, is_dry_run

ROOT = os.path.dirname(os.path.dirname(__file__))
EVENTS_PATH = os.path.join(ROOT, 'events.ndjson')


def gh_create_issue(title, body):
    """Attempt to create an issue with `gh`. Returns the issue URL or None."""
    try:
        cmd = ['gh', 'issue', 'create', '--title', title, '--body', body]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = proc.stdout.strip()
        return output
    except Exception as e:
        print('gh issue create failed:', e)
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--body', default='')
    p.add_argument('--dry-run', action='store_true', help='Do not call external CLIs')
    args = p.parse_args()

    dry = args.dry_run or is_dry_run()

    issue_url = None
    if not dry:
        issue_url = gh_create_issue(args.title, args.body)
    else:
        print('dry run: skipping gh issue creation')

    payload = {
        'title': args.title,
        'body': args.body,
        'issue_url': issue_url,
    }

    event = build_event('issue.create', 'backlog_agent', payload)

    append_event_atomic(EVENTS_PATH, event)
    print('event appended to', EVENTS_PATH)


if __name__ == '__main__':
    main()
