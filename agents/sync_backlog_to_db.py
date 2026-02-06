#!/usr/bin/env python3
"""Sync `doc/todo-archive.ndjson` into `gaia.db` backlog table.

Creates `backlog` and `audit` tables if missing and inserts/updates entries.
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
NDJSON = ROOT / 'doc' / 'todo-archive.ndjson'
DB = ROOT / 'gaia.db'

def ensure_tables(conn):
    conn.execute('''
    CREATE TABLE IF NOT EXISTS backlog (
        id TEXT PRIMARY KEY,
        title TEXT,
        status TEXT,
        priority TEXT,
        est_hours REAL,
        source_file TEXT,
        added_at TEXT,
        raw JSON
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        action TEXT,
        actor TEXT
    )
    ''')
    # migrate: ensure 'detail' column exists
    cols = [r[1] for r in conn.execute("PRAGMA table_info('audit')").fetchall()]
    if 'detail' not in cols:
        try:
            conn.execute("ALTER TABLE audit ADD COLUMN detail TEXT")
        except Exception:
            pass
    conn.commit()

def load_ndjson(path):
    if not path.exists():
        raise SystemExit('NDJSON file not found: ' + str(path))
    entries = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                # skip malformed lines
                continue
            entries.append(obj)
    return entries

def upsert_backlog(conn, item):
    now = datetime.utcnow().isoformat() + 'Z'
    conn.execute('''
    INSERT INTO backlog(id, title, status, priority, est_hours, source_file, added_at, raw)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
      title=excluded.title,
      status=excluded.status,
      priority=excluded.priority,
      est_hours=excluded.est_hours,
      source_file=excluded.source_file,
      added_at=excluded.added_at,
      raw=excluded.raw
    ''', (
        item.get('id'),
        item.get('title'),
        item.get('status'),
        item.get('priority'),
        item.get('est_hours'),
        item.get('source_file', 'doc/todo-archive.ndjson'),
        item.get('added_at', now),
        json.dumps(item, ensure_ascii=False)
    ))

def main():
    entries = load_ndjson(NDJSON)
    conn = sqlite3.connect(DB)
    ensure_tables(conn)
    for e in entries:
        # Normalize fields
        if 'id' not in e:
            continue
        upsert_backlog(conn, e)
    conn.commit()
    # write audit row
    conn.execute('INSERT INTO audit(timestamp, action, actor, detail) VALUES (?, ?, ?, ?)', (
        datetime.utcnow().isoformat() + 'Z',
        'sync_backlog',
        'agents/sync_backlog_to_db.py',
        f'Imported {len(entries)} entries from {NDJSON.name}'
    ))
    conn.commit()
    print('Synced', len(entries), 'entries to', DB)

if __name__ == '__main__':
    main()
