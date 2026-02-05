#!/usr/bin/env python3
"""Telegram + Backlog agent (prototype scaffold).

Safe-by-default: runs in `--dry-run` mode and will not make network calls.

Features:
- parse backlog docs under `doc/` (simple heuristics)
- emit NDJSON events into `events.ndjson` (dry-run appends shown)
- when `--send` is used, write an audit row into `gaia.db` via `orchestrator.write_audit()`

Usage:
  python agents/telegram_backlog_agent.py --dry-run
  python agents/telegram_backlog_agent.py --send

This is a lightweight scaffold to iterate quickly; extend with real Telegram
integration and GH issue creation in subsequent stories.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from uuid import uuid4
from typing import List, Dict

ROOT = os.path.dirname(os.path.dirname(__file__))
DOC_DIR = os.path.join(ROOT, 'doc')
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')


def find_doc_files() -> List[str]:
    # prefer consolidated backlog and STR_TODO files
    files = []
    cb = os.path.join(DOC_DIR, 'BACKLOG_CONSOLIDATED.md')
    if os.path.exists(cb):
        files.append(cb)
    # add STR_TODO_* files
    for name in sorted(os.listdir(DOC_DIR)):
        if name.startswith('STR_TODO') or name.startswith('STR_Telegram'):
            path = os.path.join(DOC_DIR, name)
            if os.path.isfile(path):
                files.append(path)
    return files


def extract_tasks_from_markdown(path: str) -> List[Dict]:
    tasks = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return tasks

    for i, raw in enumerate(lines):
        line = raw.strip()
        # heuristic: lines starting with '- ' denote backlog items in many docs
        if line.startswith('- '):
            title = line[2:].strip()
            task = {
                'id': f"doc:{os.path.basename(path)}#{i+1}",
                'source': os.path.basename(path),
                'title': title,
                'line': i+1,
            }
            tasks.append(task)
    return tasks


def build_event(task: Dict) -> Dict:
    now = datetime.utcnow().isoformat() + 'Z'
    trace_id = str(uuid4())
    return {
        'type': 'backlog.task.discovered',
        'source': task.get('source', 'doc'),
        'target': os.path.basename(os.getcwd()),
        'task_id': task['id'],
        'timestamp': now,
        'trace_id': trace_id,
        'payload': {
            'title': task.get('title'),
            'line': task.get('line'),
        }
    }


def append_event(event: Dict, dry_run: bool = True) -> None:
    line = json.dumps(event, ensure_ascii=False)
    if dry_run:
        print('DRY RUN event:', line)
        return
    # append to events.ndjson
    with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def write_audit(actor: str, action: str, details: str) -> None:
    try:
        from orchestrator import write_audit as _write_audit
    except Exception:
        print('orchestrator not available; skipping audit write')
        return
    try:
        _write_audit(actor, action, details)
    except Exception as e:
        print('audit write failed:', e)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='telegram_backlog_agent')
    parser.add_argument('--dry-run', action='store_true', help='Do not persist events; print them')
    parser.add_argument('--send', action='store_true', help='Persist events and write audit (no network calls)')
    parser.add_argument('--limit', type=int, default=100, help='Limit tasks discovered')
    args = parser.parse_args(argv)

    dry = not args.send

    files = find_doc_files()
    if not files:
        print('No doc files found under', DOC_DIR)
        return 1

    discovered = []
    for p in files:
        tasks = extract_tasks_from_markdown(p)
        for t in tasks:
            discovered.append(t)
            if len(discovered) >= args.limit:
                break
        if len(discovered) >= args.limit:
            break

    print(f'Found {len(discovered)} tasks across {len(files)} files (limit={args.limit})')

    events = [build_event(t) for t in discovered]

    for ev in events:
        append_event(ev, dry_run=dry)

    if args.send:
        # commit audit row summarizing the run
        details = json.dumps({'discovered': len(events)}, ensure_ascii=False)
        write_audit('telegram_backlog_agent', 'discover_and_record', details)
        print('Events persisted to', EVENTS_FILE)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
