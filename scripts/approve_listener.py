#!/usr/bin/env python3
"""File-based approval listener.

Place an approval file at `.tmp/approval.json` with content:
  {"task_id": "task-1", "approve": true}

This script will move the approval into an ack file `.tmp/approval_ack_{task_id}.json`
and append an event to `events.ndjson`.
"""
import json
import os
import time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
TMP_DIR = os.path.join(ROOT, '.tmp')
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')

os.makedirs(TMP_DIR, exist_ok=True)


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


def main(poll_interval=1):
    print('Approval listener started, watching .tmp/approval.json')
    while True:
        path = os.path.join(TMP_DIR, 'approval.json')
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                task_id = obj.get('task_id')
                approve = bool(obj.get('approve'))
                if task_id and approve:
                    ack_path = os.path.join(TMP_DIR, f'approval_ack_{task_id}.json')
                    with open(ack_path, 'w', encoding='utf-8') as f:
                        json.dump({"task_id": task_id, "approved_at": datetime.utcnow().isoformat() + 'Z'}, f)
                    append_event({"type": "approval.ack", "task_id": task_id, "source": "approve_listener"})
                    print(f'Approved {task_id}, wrote ack to {ack_path}')
                else:
                    print('Approval file missing required fields or approve=false; ignoring')
            except Exception as e:
                print('Failed to process approval.json:', e)
            try:
                os.remove(path)
            except Exception:
                pass
        time.sleep(poll_interval)


if __name__ == '__main__':
    import json
    from datetime import datetime
    main()
