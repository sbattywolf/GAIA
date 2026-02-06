#!/usr/bin/env python3
"""Simple worker CLI for GAIA orchestrator.

Claims tasks from `orchestrator.queue` and invokes registered handlers.

Usage: python agents/worker.py --worker-id W1 [--once] [--poll-interval 2]
"""
import argparse
import os
import time
import subprocess
import json
from typing import Callable
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import orchestrator


# Handlers registry: task_type -> Callable[[dict], dict]
HANDLERS = {}


def register_handler(task_type: str):
    def _wrap(fn: Callable[[dict], dict]):
        HANDLERS[task_type] = fn
        return fn
    return _wrap


@register_handler('job')
def handle_job(payload: dict) -> dict:
    """Run a shell command from payload['cmd'] and return result dict."""
    cmd = payload.get('cmd')
    if not cmd:
        return {'error': 'no-cmd'}
    try:
        # Prefer the standardized script runner to avoid REPL/shell confusion
        from agents.agent_utils import run_script
        # If cmd refers to an existing script file, use the runner; otherwise fall back
        # to shell execution for arbitrary commands.
        if os.path.exists(cmd.split(' ')[0]):
            res = run_script(cmd.split(' ')[0], args=cmd.split(' ')[1:], timeout=300)
            return {'rc': res.get('rc'), 'stdout': res.get('stdout', ''), 'stderr': res.get('stderr', '')}
        else:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
            return {'rc': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}
    except Exception as e:
        return {'error': str(e)}


@register_handler('noop')
def handle_noop(payload: dict) -> dict:
    return {'ok': True}


def _process_task(task, worker_id):
    task_id = task['id']
    ttype = task['task_type']
    payload = task.get('payload') or {}
    handler = HANDLERS.get(ttype)
    if not handler:
        orchestrator.fail_task(task_id, f'no handler for {ttype}')
        return {'id': task_id, 'status': 'failed', 'reason': 'no handler'}

    try:
        result = handler(payload)
        orchestrator.complete_task(task_id, result if isinstance(result, dict) else {'result': result})
        return {'id': task_id, 'status': 'completed'}
    except Exception as e:
        orchestrator.fail_task(task_id, str(e))
        return {'id': task_id, 'status': 'failed', 'reason': str(e)}


def run_once(worker_id: str, max_jobs: int = 1):
    # claim up to max_jobs tasks then process them concurrently
    tasks = []
    for _ in range(max_jobs):
        t = orchestrator.claim_task(worker_id)
        if not t:
            break
        tasks.append(t)

    if not tasks:
        return 2

    results = []
    with ThreadPoolExecutor(max_workers=max_jobs) as ex:
        futures = {ex.submit(_process_task, t, worker_id): t for t in tasks}
        for fut in as_completed(futures):
            results.append(fut.result())

    return 0


def _make_health_handler(status_provider):
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != '/health':
                self.send_response(404)
                self.end_headers()
                return
            st = status_provider()
            data = json.dumps(st).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format, *args):
            return

    return HealthHandler


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--worker-id', required=True)
    p.add_argument('--once', action='store_true')
    p.add_argument('--poll-interval', type=float, default=2.0)
    p.add_argument('--max-jobs', type=int, default=1, help='Maximum concurrent jobs to run')
    p.add_argument('--health-port', type=int, default=0, help='Start HTTP health server on this port (0 = disabled)')
    p.add_argument('--run-duration', type=float, default=0, help='If >0, run main loop for this many seconds then exit')
    args = p.parse_args(argv)

    worker_id = args.worker_id
    max_jobs = max(1, args.max_jobs)
    start_time = time.time()

    # health server
    health_server = None
    if args.health_port and args.health_port > 0:
        def status():
            uptime = time.time() - start_time
            pending = len(orchestrator.list_tasks('pending'))
            inprog = len(orchestrator.list_tasks('in_progress'))
            return {'worker_id': worker_id, 'uptime': uptime, 'pending': pending, 'in_progress': inprog}

        handler = _make_health_handler(status)
        health_server = HTTPServer(('127.0.0.1', args.health_port), handler)
        t = threading.Thread(target=health_server.serve_forever, daemon=True)
        t.start()

    if args.once:
        return run_once(worker_id, max_jobs=max_jobs)

    try:
        with ThreadPoolExecutor(max_workers=max_jobs) as ex:
            futures = set()
            while True:
                # optional run-duration exit
                if args.run_duration and (time.time() - start_time) > args.run_duration:
                    break

                # clean up finished futures
                done = {f for f in futures if f.done()}
                futures -= done

                # if we have capacity, claim tasks
                capacity = max_jobs - len(futures)
                for _ in range(capacity):
                    t = orchestrator.claim_task(worker_id)
                    if not t:
                        break
                    futures.add(ex.submit(_process_task, t, worker_id))

                if not futures:
                    time.sleep(args.poll_interval)
                else:
                    time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        if health_server:
            health_server.shutdown()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
