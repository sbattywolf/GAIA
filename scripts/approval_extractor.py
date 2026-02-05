#!/usr/bin/env python3
"""Small helper to pair approval.request -> approval.received events.

API:
- extract_approval_pairs(events) -> {matched: [(req, recv)], missing_requests: [req], unmatched_received: [recv]}

Matching strategy (simple):
- Prefer matching by `request_id` if present on both events.
- Otherwise match by `trace_id`.
- Otherwise match by `task_id` and chronological order (first received after request).
"""
from collections import defaultdict
from typing import List, Dict, Tuple


def _group_by_type(events: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    requests = [e for e in events if (e.get('type') or '').endswith('approval.request') or e.get('type') == 'approval.request']
    received = [e for e in events if (e.get('type') or '').endswith('approval.received') or e.get('type') == 'approval.received']
    return requests, received


def extract_approval_pairs(events: List[Dict]):
    requests, received = _group_by_type(events)

    # index received events by request_id / trace_id / task_id
    by_request_id = defaultdict(list)
    by_trace = defaultdict(list)
    by_task = defaultdict(list)
    for r in received:
        rid = r.get('request_id') or (r.get('payload') or {}).get('request_id')
        if rid:
            by_request_id[rid].append(r)
            continue
        tid = r.get('trace_id') or (r.get('payload') or {}).get('trace_id')
        if tid:
            by_trace[tid].append(r)
            continue
        task = r.get('task_id') or (r.get('payload') or {}).get('task_id')
        if task:
            by_task[task].append(r)

    matched = []
    missing_requests = []
    used_received = set()

    for req in requests:
        rid = req.get('request_id') or (req.get('payload') or {}).get('request_id')
        paired = None
        if rid and by_request_id.get(rid):
            paired = by_request_id[rid].pop(0)
        if not paired:
            tid = req.get('trace_id') or (req.get('payload') or {}).get('trace_id')
            if tid and by_trace.get(tid):
                paired = by_trace[tid].pop(0)
        if not paired:
            task = req.get('task_id') or (req.get('payload') or {}).get('task_id')
            if task and by_task.get(task):
                paired = by_task[task].pop(0)

        if paired:
            matched.append((req, paired))
            used_received.add(id(paired))
        else:
            missing_requests.append(req)

    # any remaining received that weren't used are unmatched_received
    unmatched = []
    for r in received:
        if id(r) in used_received:
            continue
        # if it still exists in any index lists, it's unmatched
        unmatched.append(r)

    return {
        'matched': matched,
        'missing_requests': missing_requests,
        'unmatched_received': unmatched,
    }


if __name__ == '__main__':
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'events.ndjson'
    ev = []
    with open(path, 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            try:
                ev.append(json.loads(l))
            except Exception:
                continue
    res = extract_approval_pairs(ev)
    print('matched:', len(res['matched']))
    print('missing_requests:', len(res['missing_requests']))
    print('unmatched_received:', len(res['unmatched_received']))
