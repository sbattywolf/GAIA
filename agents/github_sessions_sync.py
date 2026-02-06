#!/usr/bin/env python3
"""Prototype: sync `gaia.db` backlog -> GitHub issues (or dry-run).

Usage:
  python agents/github_sessions_sync.py --dry-run
  python agents/github_sessions_sync.py        # requires GITHUB_TOKEN and GITHUB_REPO

Behavior:
- By default runs in dry-run mode and prints intended actions.
- When not dry-run, uses `GITHUB_TOKEN` and `GITHUB_REPO` (owner/repo) to create/update issues.

This is a lightweight prototype for `TASK-009` and `MINI-002-2`.
"""
import argparse
import os
import sqlite3
import json
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / 'gaia.db'
CONFIG = ROOT / 'agents' / 'config' / 'github_sessions.yml'

def load_backlog(dbpath):
    conn = sqlite3.connect(str(dbpath))
    cur = conn.cursor()
    cur.execute('SELECT id, title, status, priority, est_hours FROM backlog')
    rows = [ {'id': r[0], 'title': r[1], 'status': r[2], 'priority': r[3], 'est_hours': r[4]} for r in cur.fetchall() ]
    conn.close()
    return rows

def find_issue(session, repo, gaia_id):
    # search issues with the GAIA marker
    q = f'repo:{repo} in:body "GAIA_ID: {gaia_id}"'
    resp = session.get('https://api.github.com/search/issues', params={'q': q})
    resp.raise_for_status()
    data = resp.json()
    items = data.get('items', [])
    return items[0] if items else None

def create_issue(session, repo, title, body, labels=None):
    url = f'https://api.github.com/repos/{repo}/issues'
    payload = {'title': title, 'body': body}
    if labels:
        payload['labels'] = labels
    resp = session.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def update_issue(session, repo, number, title=None, body=None, state=None, labels=None):
    url = f'https://api.github.com/repos/{repo}/issues/{number}'
    payload = {}
    if title is not None:
        payload['title'] = title
    if body is not None:
        payload['body'] = body
    if state is not None:
        payload['state'] = state
    if labels is not None:
        payload['labels'] = labels
    resp = session.patch(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', default=True, dest='dry')
    args = p.parse_args()

    if not DB.exists():
        print('Missing gaia.db; please run sync_backlog_to_db.py first')
        return 1

    rows = load_backlog(DB)
    if args.dry:
        print('DRY RUN: will prepare', len(rows), 'items for GitHub')
        for r in rows[:50]:
            title = f"[{r['id']}] {r['title']}"
            body = f"GAIA_ID: {r['id']}\nStatus: {r['status']}\nPriority: {r['priority']}\nEst: {r['est_hours']}"
            print('-', title)
            print('  ', body)
        return 0

    # Prefer automation-specific tokens to allow rotating scoped automation tokens
    token = (
        os.environ.get('AUTOMATION_GITHUB_TOKEN_PAI') or
        os.environ.get('AUTOMATION_GITHUB_TOKEN') or
        os.environ.get('AUTOMATION_GITHUB_TOKEN_ORG') or
        os.environ.get('GITHUB_TOKEN')
    )
    repo = os.environ.get('GITHUB_REPO') or os.environ.get('GITHUB_REPOSITORY')
    if not token or not repo:
        print('GITHUB_TOKEN and GITHUB_REPO required when not in --dry-run')
        return 1

    s = requests.Session()
    s.headers.update({'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'})

    for r in rows:
        gaia_id = r['id']
        title = f"[{gaia_id}] {r['title']}"
        body = f"GAIA_ID: {gaia_id}\nStatus: {r['status']}\nPriority: {r['priority']}\nEst: {r['est_hours']}"

        existing = find_issue(s, repo, gaia_id)
        if existing:
            num = existing['number']
            print('Updating issue', num, 'for GAIA_ID', gaia_id)
            update_issue(s, repo, num, title=title, body=body, state='open' if r['status'] != 'closed' else 'closed')
        else:
            print('Creating issue for GAIA_ID', gaia_id)
            create_issue(s, repo, title, body, labels=[f'gaia:{r["priority"]}'])

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
