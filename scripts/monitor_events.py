#!/usr/bin/env python3
"""Small monitor for GAIA events.ndjson — prints counts and simple metrics.

Usage:
  python scripts/monitor_events.py --events GAIA/events.ndjson
"""
import argparse
import json
import os
from collections import Counter


def read_events(path):
    if not os.path.exists(path):
        print('events file not found:', path)
        return []
    out = []
    with open(path, 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            try:
                out.append(json.loads(l))
            except Exception:
                continue
    return out


def is_error(ev):
    t = ev.get('type') or ''
    if 'error' in t.lower() or 'fail' in t.lower():
        return True
    p = ev.get('payload') or {}
    if isinstance(p, dict) and p.get('status') in ('error', 'failed'):
        return True
    return False


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--events', default='GAIA/events.ndjson')
    args = p.parse_args(argv)

    events = read_events(args.events)
    total = len(events)
    types = Counter([e.get('type') or 'unknown' for e in events])
    trace_ids = [e.get('trace_id') for e in events if e.get('trace_id')]
    dup_count = total - len(set(trace_ids))
    error_count = sum(1 for e in events if is_error(e))

    print('Events monitor report')
    print('---------------------')
    print('Total events:', total)
    print('Event types:')
    for k, v in types.most_common(10):
        print(' -', k, v)
    print('Duplicate trace_id count:', dup_count)
    print('Error-like events:', error_count)


if __name__ == '__main__':
    main()
