#!/usr/bin/env python3
"""Validate that `doc/todo-archive.ndjson` matches `gaia.db` backlog table.

Exit code 0 if in sync; 1 otherwise. Prints differences.
"""
import json
import sqlite3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
NDJSON = ROOT / 'doc' / 'todo-archive.ndjson'
DB = ROOT / 'gaia.db'

def load_ndjson(path):
    out = {}
    # use utf-8-sig to tolerate BOM; normalize numeric ids to int for comparison with DB
    with path.open('r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            # normalize id type: DB uses integer ids, so prefer int when possible
            raw_id = obj.get('id')
            try:
                key = int(raw_id)
            except Exception:
                key = raw_id
            out[key] = obj
    return out

def load_db(path):
    conn = sqlite3.connect(str(path))
    cur = conn.cursor()
    cur.execute('SELECT id, title, status, priority, est_hours FROM backlog')
    rows = {}
    for r in cur.fetchall():
        raw_id = r[0]
        try:
            key = int(raw_id)
        except Exception:
            key = raw_id
        rows[key] = {'id': raw_id, 'title': r[1], 'status': r[2], 'priority': r[3], 'est_hours': r[4]}
    conn.close()
    return rows

def main():
    if not NDJSON.exists():
        print('Missing', NDJSON)
        return 1
    if not DB.exists():
        print('Missing', DB)
        return 1
    nd = load_ndjson(NDJSON)
    db = load_db(DB)
    nd_ids = set(nd.keys())
    db_ids = set(db.keys())
    only_nd = sorted(nd_ids - db_ids, key=str)
    only_db = sorted(db_ids - nd_ids, key=str)
    mismatches = []
    for id_ in sorted(nd_ids & db_ids, key=str):
        a = nd[id_]
        b = db[id_]
        diffs = []
        if str(a.get('status')) != str(b.get('status')):
            diffs.append(f"status ND:{a.get('status')} DB:{b.get('status')}")
        if str(a.get('title')) != str(b.get('title')):
            diffs.append("title mismatch")
        if diffs:
            mismatches.append((id_, diffs))
    ok = not (only_nd or only_db or mismatches)
    if ok:
        print('OK: todo-archive.ndjson and gaia.db backlog are in sync (ids match, statuses match).')
        return 0
    print('DIFFERENCES FOUND:')
    if only_nd:
        print('\nIn NDJSON but missing in DB (count={}):'.format(len(only_nd)))
        for i in only_nd[:50]:
            print('-', i)
    if only_db:
        print('\nIn DB but missing in NDJSON (count={}):'.format(len(only_db)))
        for i in only_db[:50]:
            print('-', i)
    if mismatches:
        print('\nMismatched entries (status/title):')
        for id_, diffs in mismatches[:50]:
            print('-', id_, '->', ';'.join(diffs))
    return 1

if __name__ == '__main__':
    sys.exit(main())
