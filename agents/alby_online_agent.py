#!/usr/bin/env python3
"""Alby Online Agent (prototype)

Scaffold for an online-capable agent that can create remote tasks/issues
in a Git-backed workflow (GitHub via `gh`) or emit local NDJSON events when
remote access isn't available or `--dry-run` is used.

Commands:
  create-issue --repo owner/repo --title "..." [--body "..."] [--labels a,b] [--dry-run]
  create-issue-local --title --body    # forces local-only event

Behavior:
- Attempts to run `gh issue create --repo <repo> --title <title> --body <body> --label ...`.
- On success, emits `issue.created.remote` with payload including the URL.
- On failure or dry-run, emits `issue.created.local` with payload recording intended remote target.

Note: This is a prototype scaffold; callers should treat this as the "online" agent
for Alby 0.3 nextagent prototyping. Keep operations idempotent and emit traceable events.
"""

import argparse
import os
import shlex
import subprocess
import time
import json
import sys
from datetime import datetime
from agents import agent_utils

EVENTS_PATH = os.environ.get('GAIA_EVENTS_PATH', 'events.ndjson')
SOURCE = os.path.basename(os.getcwd())


def run_gh_create(repo, title, body=None, labels=None, dry_run=False):
    cmd = ['gh', 'issue', 'create', '--repo', repo, '--title', title]
    if body:
        cmd += ['--body', body]
    if labels:
        # gh accepts multiple --label flags or comma-separated list depending on version
        # we'll pass a comma-joined labels value as a single --label
        cmd += ['--label', ','.join(labels)]

    if dry_run:
        return {'dry_run': True, 'cmd': ' '.join(shlex.quote(c) for c in cmd)}

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, encoding='utf-8')
        return {'dry_run': False, 'stdout': out}
    except FileNotFoundError:
        raise RuntimeError('gh CLI not found')
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'gh failed: {e.output}')


def emit_event(ev_type, payload, task_id=None):
    ev = agent_utils.build_event(ev_type, SOURCE, payload, task_id=task_id)
    agent_utils.append_event_atomic(EVENTS_PATH, ev)
    return ev


def cmd_create_issue(args):
    payload = {'repo': args.repo, 'title': args.title, 'body': args.body, 'labels': args.labels}
    try:
        result = run_gh_create(args.repo, args.title, body=args.body, labels=args.labels, dry_run=args.dry_run)
    except Exception as e:
        # remote failed; emit local fallback
        payload['error'] = str(e)
        payload['fallback'] = True
        payload['attempted_at'] = datetime.utcnow().isoformat() + 'Z'
        ev = emit_event('issue.created.local', payload)
        print('emitted local fallback event', ev['trace_id'])
        return 0

    # success or dry-run
    if result.get('dry_run'):
        payload['dry_run_cmd'] = result['cmd']
        ev = emit_event('issue.created.dryrun', payload)
        print('dry-run event emitted', ev['trace_id'])
        return 0

    # parse stdout for URL heuristically
    stdout = result.get('stdout', '')
    url = None
    for line in stdout.splitlines():
        if line.startswith('https://') or line.startswith('http://'):
            url = line.strip()
            break
    payload['remote_stdout'] = stdout
    payload['url'] = url
    ev = emit_event('issue.created.remote', payload)
    print('remote issue event emitted', ev['trace_id'])
    return 0


def cmd_create_issue_local(args):
    payload = {'title': args.title, 'body': args.body, 'created_at': datetime.utcnow().isoformat() + 'Z'}
    ev = emit_event('issue.created.local', payload)
    print('emitted local event', ev['trace_id'])
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog='alby-online-agent')
    sp = p.add_subparsers(dest='cmd')
    p.add_argument('--serve', action='store_true', help='Run as a long-lived service (health endpoint)')
    p.add_argument('--health-port', type=int, default=0, help='Port for health HTTP server (0 = disabled)')

    p_create = sp.add_parser('create-issue')
    p_create.add_argument('--repo', required=True, help='owner/repo')
    p_create.add_argument('--title', required=True)
    p_create.add_argument('--body', default=None)
    p_create.add_argument('--labels', nargs='*', default=None)
    p_create.add_argument('--dry-run', action='store_true')
    p_create.set_defaults(func=cmd_create_issue)

    p_local = sp.add_parser('create-issue-local')
    p_local.add_argument('--title', required=True)
    p_local.add_argument('--body', default=None)
    p_local.set_defaults(func=cmd_create_issue_local)

    args = p.parse_args(argv)
    # If serve flag provided, run a simple long-lived service with a health endpoint
    if getattr(args, 'serve', False):
        # minimal health server
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import threading

        start_time = datetime.utcnow()

        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/health':
                    self.send_response(404)
                    self.end_headers()
                    return
                uptime = (datetime.utcnow() - start_time).total_seconds()
                payload = {'name': 'alby-online', 'version': '0.3', 'uptime': uptime}
                body = json.dumps(payload).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                return

        httpd = None
        if getattr(args, 'health_port', 0):
            try:
                httpd = HTTPServer(('127.0.0.1', args.health_port), HealthHandler)
                t = threading.Thread(target=httpd.serve_forever, daemon=True)
                t.start()
                print(f'alby-online: health endpoint running on 127.0.0.1:{args.health_port}', flush=True)
            except Exception as e:
                print(f'alby-online: failed to start health server: {e}', file=sys.stderr, flush=True)

        print('alby-online: entering service loop', flush=True)
        try:
            # keep alive until interrupted
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            pass
        finally:
            if httpd:
                httpd.shutdown()
        return 0

    if not hasattr(args, 'func'):
        p.print_help()
        return 2
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
