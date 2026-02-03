#!/usr/bin/env python3
"""CI Issue Collector

Scans CI failure reports (or injected failures) and creates GitHub issues
for failing jobs. Emits NDJSON events and records audits via `orchestrator`.

Usage:
  python agents/ci_issue_collector.py --repo owner/repo --since 2026-01-01 --dry-run
"""
import argparse
import os
import subprocess
import uuid
from datetime import datetime
from typing import List, Dict

from .agent_utils import build_event, append_event_atomic, is_dry_run
import orchestrator


def get_events_path():
    return os.environ.get('GAIA_EVENTS_PATH') or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'events.ndjson')


def gh_create_issue(title: str, body: str) -> str:
    try:
        cmd = ['gh', 'issue', 'create', '--repo', os.environ.get('CI_REPO', ''), '--title', title, '--body', body]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return proc.stdout.strip()
    except Exception as e:
        print('gh issue create failed:', e)
        return None


def write_audit(actor: str, action: str, details: str):
    orchestrator.init_db()
    conn = orchestrator.sqlite3.connect(orchestrator.DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO audit (timestamp, actor, action, details) VALUES (?, ?, ?, ?)', (datetime.utcnow().isoformat() + 'Z', actor, action, details))
    conn.commit()
    conn.close()


def find_failures(repo: str, since: str) -> List[Dict]:
    """Discover failures. Default implementation reads from FILE_CI_REPORT env (JSON array).
    Returns list of dicts with keys: `id`, `title`, `body`.
    """
    import json
    path = os.environ.get('FILE_CI_REPORT')
    if path and os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data
            except Exception:
                return []
    # fallback: no failures
    return []


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--since', default='')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    dry = args.dry_run or is_dry_run()
    events_path = get_events_path()

    failures = find_failures(args.repo, args.since)
    if not failures:
        print('no failures found')
        return 0

    for f in failures:
        title = f.get('title') or f.get('id')
        body = f.get('body', '')
        issue_url = None
        if not dry:
            # set CI_REPO env so gh command knows which repo
            os.environ['CI_REPO'] = args.repo
            issue_url = gh_create_issue(title, body)
        else:
            print('dry-run: would create issue for', title)

        event = build_event('ci.issue', 'ci_issue_collector', {'failure': f, 'issue_url': issue_url})
        append_event_atomic(events_path, event)
        # write audit row (concise)
        try:
            write_audit('ci_issue_collector', 'issue.create' if issue_url else 'issue.dry_run', title)
        except Exception:
            pass

    print('processed', len(failures), 'failures')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
