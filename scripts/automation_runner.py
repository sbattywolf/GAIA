#!/usr/bin/env python3
"""Simple automation runner that processes tasks and requests file-based approvals.

Usage: python scripts/automation_runner.py

This is intentionally minimal: it reads `tasks.json` (creates a sample if missing),
writes approval request files to `.tmp/approval_required_{task_id}.json` when needed,
and waits for `.tmp/approval_ack_{task_id}.json` to continue.
Events are appended to `events.ndjson` for audit.
"""
import json
import os
import time
import signal
from datetime import datetime
import importlib.util
from pathlib import Path
import uuid

ROOT = os.path.dirname(os.path.dirname(__file__))
TASKS_FILE = os.path.join(ROOT, 'tasks.json')
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')
TMP_DIR = os.path.join(ROOT, '.tmp')

os.makedirs(TMP_DIR, exist_ok=True)

running = True


def append_event(ev: dict):
    ev['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    # also append to a simple log for quick tailing
    try:
        log_path = os.path.join(TMP_DIR, 'automation.log')
        with open(log_path, 'a', encoding='utf-8') as lf:
            lf.write(f"{ev['timestamp']} {ev.get('type','event')} {ev.get('task_id','')}\n")
    except Exception:
        pass


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        sample = [
            {"id": "task-1", "action": "create_issue", "requires_approval": True, "payload": {"title": "Sample task"}, "status": "pending"}
        ]
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample, f, indent=2)
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)


def handle_task(task):
    task_id = task['id']
    if task.get('requires_approval'):
        req_path = os.path.join(TMP_DIR, f'approval_required_{task_id}.json')
        ack_path = os.path.join(TMP_DIR, f'approval_ack_{task_id}.json')
        # write request with request_id and trace_id for correlation
        request_id = uuid.uuid4().hex
        trace_id = uuid.uuid4().hex
        req_obj = {"task_id": task_id, "payload": task.get('payload'), "request_id": request_id, "trace_id": trace_id}
        with open(req_path, 'w', encoding='utf-8') as f:
            json.dump(req_obj, f)
        append_event({"type": "approval.request", "task_id": task_id, "request_id": request_id, "trace_id": trace_id, "source": "automation_runner"})
        print(f"Approval required for {task_id}; waiting for ack file {ack_path}")
        # wait for ack — accept either task-specific ack or a global approval file
        global_appr = os.path.join(TMP_DIR, 'approval.json')
        while running and not os.path.exists(ack_path):
            # if a global approval file exists, convert it into a task-specific ack
            if os.path.exists(global_appr):
                try:
                    # create the ack file for this task so runner proceeds
                    with open(ack_path, 'w', encoding='utf-8') as f:
                        json.dump({"task_id": task_id, "approved_at": datetime.utcnow().isoformat() + 'Z'}, f)
                    # remove the global approval file to avoid reusing it
                    try:
                        os.remove(global_appr)
                    except Exception:
                        pass
                    break
                except Exception:
                    pass
            time.sleep(1)
        if not running:
            return False
        # proceed
        append_event({"type": "approval.received", "task_id": task_id, "source": "automation_runner"})

    # Simulate work
    append_event({"type": "task.start", "task_id": task_id, "action": task.get('action')})
    print(f"Processing {task_id} ...")
    time.sleep(2)
    append_event({"type": "task.complete", "task_id": task_id, "action": task.get('action')})
    task['status'] = 'done'
    return True


def sigterm_handler(signum, frame):
    global running
    running = False


def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    # load .private/.env early so child processes inherit secrets
    try:
        env_mod = Path(__file__).resolve().parent / 'env_loader.py'
        if env_mod.exists():
            spec_e = importlib.util.spec_from_file_location('env_loader', str(env_mod))
            em = importlib.util.module_from_spec(spec_e)
            spec_e.loader.exec_module(em)
            priv = Path(__file__).resolve().parent.parent / '.private' / '.env'
            if priv.exists():
                em.load_env(str(priv))
    except Exception:
        print('Warning: failed to load .private/.env via env_loader; continuing safely')

    # enforce autonomy guard early to avoid accidental external side-effects
    try:
        mod_path = Path(__file__).resolve().parent / 'autonomy_guard.py'
        if mod_path.exists():
            spec = importlib.util.spec_from_file_location('autonomy_guard', str(mod_path))
            ag = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ag)
            ag.require_autonomy_or_exit('automation runner actions')
    except SystemExit:
        raise
    except Exception:
        print('Failed to load autonomy guard — aborting for safety')
        raise SystemExit(0)
    tasks = load_tasks()
    changed = False
    for task in tasks:
        if task.get('status') == 'done':
            continue
        ok = handle_task(task)
        changed = changed or ok
        if not running:
            break
    if changed:
        save_tasks(tasks)
    print('Runner exiting')


if __name__ == '__main__':
    main()
