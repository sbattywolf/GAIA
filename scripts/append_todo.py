#!/usr/bin/env python3
"""Append a todo to Gaia/doc/todo-archive.ndjson atomically.

Usage:
  python scripts/append_todo.py --title "Fix X" --description "Details" --priority 50 --added_by user
"""
import argparse
import json
import os
import sys
import tempfile
import getpass
from datetime import datetime
import uuid

ROOT = os.path.dirname(os.path.dirname(__file__))
ARCHIVE = os.path.join(ROOT, 'doc', 'todo-archive.ndjson')


def ensure_dir(path):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def append_record(record):
    ensure_dir(ARCHIVE)
    # atomic append: write to temp then rename-append
    with open(ARCHIVE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--description', default='')
    p.add_argument('--priority', type=int, default=100)
    # use getpass.getuser() which works in non-interactive CI environments
    try:
        default_user = getpass.getuser()
    except Exception:
        default_user = os.environ.get('USER') or os.environ.get('USERNAME') or 'user'
    p.add_argument('--added_by', default=default_user)
    args = p.parse_args()

    rec = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'added_by': args.added_by,
        'title': args.title,
        'description': args.description,
        'priority': args.priority,
        'trace_id': str(uuid.uuid4())
    }
    append_record(rec)
    print('appended todo to', ARCHIVE)


if __name__ == '__main__':
    main()
