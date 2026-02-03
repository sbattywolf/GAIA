#!/usr/bin/env python3
"""Prune closed todos: keep N most recent closed items, archive the rest.

Usage:
  python scripts/prune_closed_todos.py --ndjson Gaia/doc/todo-archive.ndjson --keep 7
"""
import argparse
import json
import os
from datetime import datetime


def read_ndjson(path):
    if not os.path.exists(path):
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
                # skip malformed
                continue
    return out


def write_ndjson(path, items, mode='w'):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    with open(path, mode, encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + '\n')


def is_closed(obj):
    s = obj.get('status')
    if isinstance(s, str) and s.lower() == 'closed':
        return True
    if obj.get('closed') in (True, 'true', 'True'):
        return True
    return False


def parse_time(ts: str):
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None


def prune(ndjson_path, keep=7, older_out=None):
    items = read_ndjson(ndjson_path)
    closed = [it for it in items if is_closed(it)]
    open_items = [it for it in items if not is_closed(it)]

    # sort closed by timestamp desc
    closed_sorted = sorted(closed, key=lambda it: parse_time(it.get('timestamp') or '' ) or datetime.min, reverse=True)
    keep_set = closed_sorted[:keep]
    archive_set = closed_sorted[keep:]

    # rewrite main ndjson: all open items + kept closed (keep ordering: open then kept closed newest first)
    new_main = open_items + keep_set
    write_ndjson(ndjson_path, new_main, mode='w')

    # append older archived to older_out
    if older_out and archive_set:
        write_ndjson(older_out, archive_set, mode='a')

    return len(new_main), len(archive_set)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--ndjson', default=os.path.join('Gaia', 'doc', 'todo-archive.ndjson'))
    p.add_argument('--keep', type=int, default=7)
    p.add_argument('--older-out', default=os.path.join('Gaia', 'doc', 'todo-archive-older.ndjson'))
    args = p.parse_args(argv)

    main_count, archived = prune(args.ndjson, keep=args.keep, older_out=args.older_out)
    print(f'Wrote main archive ({main_count} records); moved {archived} older closed todos to {args.older_out}')


if __name__ == '__main__':
    main()
