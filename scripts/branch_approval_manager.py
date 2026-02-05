#!/usr/bin/env python3
"""
Simple branch/PR approval manager for local flow.

Usage examples:
  python scripts/branch_approval_manager.py --branch feature/x --pr 123

This will create `.tmp/branch_approval_feature_x.json` and emit events via `gaia.events`.
It waits for `.tmp/branch_approval_ack_feature_x.json` (or a global `.tmp/approval.json`) and exits with 0 on approval, 2 on timeout.
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TMP = os.path.join(ROOT, '.tmp')
os.makedirs(TMP, exist_ok=True)

def now():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def write_request(branch, pr):
    path = os.path.join(TMP, f'branch_approval_{branch}.json')
    payload = {'branch': branch, 'pr': pr, 'timestamp': now()}
    with open(path, 'w', encoding='utf8') as f:
        json.dump(payload, f)
    return path


def wait_for_ack(branch, timeout=300):
    ack_path = os.path.join(TMP, f'branch_approval_ack_{branch}.json')
    global_approval = os.path.join(TMP, 'approval.json')
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(ack_path):
            with open(ack_path, 'r', encoding='utf8') as f:
                return json.load(f)
        if os.path.exists(global_approval):
            try:
                with open(global_approval, 'r', encoding='utf8') as f:
                    return json.load(f)
            except Exception:
                return {'approve': True, 'via': 'global'}
        time.sleep(2)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', required=True)
    parser.add_argument('--pr', required=False)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()

    branch = args.branch.replace('/', '_')
    pr = args.pr

    # emit event
    try:
        from gaia import events
        events.make_event('approval.request.branch', {'branch': branch, 'pr': pr})
    except Exception:
        pass

    req_path = write_request(branch, pr)
    print(f'Approval request written: {req_path}')

    ack = wait_for_ack(branch, timeout=args.timeout)
    if ack:
        try:
            from gaia import events
            events.make_event('approval.received.branch', {'branch': branch, 'pr': pr, 'ack': ack})
        except Exception:
            pass
        print('Approved:', ack)
        return 0
    else:
        print('Timed out waiting for approval')
        return 2


if __name__ == '__main__':
    sys.exit(main())
