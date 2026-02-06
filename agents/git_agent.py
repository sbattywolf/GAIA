#!/usr/bin/env python3
"""Simple Git agent CLI for GAIA.

Features (lightweight):
- create a session-scoped branch
- scaffold a task directory from a template
- open a PR using `gh` (if available)
- delete a branch (remote + local)
- append trace events to `events.ndjson`

This is intentionally minimal and safe. Use `--dry-run` to preview commands.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVENT_LOG = ROOT / 'events.ndjson'


def run(cmd, dry_run=False, check=True):
    print('>>>', ' '.join(cmd))
    if dry_run:
        return None
    return subprocess.run(cmd, check=check)


def append_event(ev: dict):
    ev.setdefault('timestamp', datetime.utcnow().isoformat() + 'Z')
    with open(EVENT_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(ev) + '\n')


def branch_name(session_date, agent, desc):
    safe = desc.replace(' ', '-').lower()
    return f"session/{session_date}-{agent}/{safe}"[:200]


def cmd_create_branch(args):
    session_date = args.date or datetime.utcnow().strftime('%Y%m%d')
    agent = args.agent or os.environ.get('AGENT_NAME', 'copilot')
    name = branch_name(session_date, agent, args.desc)
    run(['git', 'checkout', '-b', name], dry_run=args.dry_run)
    run(['git', 'push', '-u', 'origin', name], dry_run=args.dry_run)
    append_event({
        'type': 'git.action',
        'action': 'create_branch',
        'branch': name,
        'agent': agent,
        'session': session_date,
    })
    print('Created branch', name)


def cmd_scaffold(args):
    # create a simple task scaffold under tasks/<name>
    name = args.name.replace(' ', '_')
    tasks_dir = ROOT / 'tasks'
    tasks_dir.mkdir(exist_ok=True)
    target = tasks_dir / name
    if target.exists():
        print('Target exists:', target)
        return 1
    target.mkdir()
    # copy template
    tpl = ROOT / 'doc' / 'templates' / 'git_agent_task_template.md'
    if tpl.exists():
        content = tpl.read_text(encoding='utf-8')
    else:
        content = f"# Task: {args.name}\n\nDescribe the task here."
    (target / 'README.md').write_text(content, encoding='utf-8')
    append_event({
        'type': 'git.action',
        'action': 'scaffold_task',
        'task': name,
        'agent': args.agent or os.environ.get('AGENT_NAME', 'copilot'),
    })
    print('Scaffolded task at', target)


def cmd_pr(args):
    # create PR via gh
    title = args.title or f"[session] {args.branch}"
    body = args.body or f"Automated PR from git_agent for {args.branch}"
    cmd = ['gh', 'pr', 'create', '--title', title, '--body', body]
    if args.base:
        cmd += ['--base', args.base]
    if args.draft:
        cmd += ['--draft']
    run(cmd, dry_run=args.dry_run)
    append_event({
        'type': 'git.action',
        'action': 'create_pr',
        'branch': args.branch,
        'title': title,
    })


def cmd_delete_branch(args):
    name = args.branch
    # delete remote
    run(['git', 'push', 'origin', '--delete', name], dry_run=args.dry_run, check=False)
    # delete local
    run(['git', 'branch', '-D', name], dry_run=args.dry_run, check=False)
    append_event({'type': 'git.action', 'action': 'delete_branch', 'branch': name})
    print('Deleted branch', name)


def main(argv=None):
    p = argparse.ArgumentParser(prog='git_agent')
    sub = p.add_subparsers(dest='cmd')

    b = sub.add_parser('branch', help='create and push a session branch')
    b.add_argument('desc')
    b.add_argument('--agent')
    b.add_argument('--date')
    b.add_argument('--dry-run', action='store_true')
    b.set_defaults(func=cmd_create_branch)

    s = sub.add_parser('scaffold', help='scaffold a new task')
    s.add_argument('name')
    s.add_argument('--agent')
    s.set_defaults(func=cmd_scaffold)

    pr = sub.add_parser('pr', help='create a GitHub PR using gh')
    pr.add_argument('--branch', required=True)
    pr.add_argument('--title')
    pr.add_argument('--body')
    pr.add_argument('--base')
    pr.add_argument('--draft', action='store_true')
    pr.add_argument('--dry-run', action='store_true')
    pr.set_defaults(func=cmd_pr)

    d = sub.add_parser('delete-branch', help='delete branch remote+local')
    d.add_argument('branch')
    d.add_argument('--dry-run', action='store_true')
    d.set_defaults(func=cmd_delete_branch)

    args = p.parse_args(argv)
    if not hasattr(args, 'func'):
        p.print_help()
        return 2
    return args.func(args)


if __name__ == '__main__':
    rc = main()
    if isinstance(rc, int):
        sys.exit(rc)