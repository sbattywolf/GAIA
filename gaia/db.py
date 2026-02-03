"""Simple SQLite trace writer for GAIA.
Creates a `traces` table in `gaia.db` and provides `write_trace`.
"""
import json
import os
import sqlite3
import threading
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'gaia.db')
_lock = threading.Lock()


def _conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def _init():
    with _lock:
        conn = _conn()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT,
            agent_id TEXT,
            status TEXT,
            details TEXT
        )
        ''')
        conn.commit()
        conn.close()


_init()


def write_trace(action, agent_id=None, status=None, details=None):
    ts = datetime.datetime.utcnow().isoformat() + 'Z'
    with _lock:
        conn = _conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO traces (timestamp, action, agent_id, status, details) VALUES (?, ?, ?, ?, ?)',
                    (ts, action, agent_id, status, json.dumps(details, default=str)))
        conn.commit()
        conn.close()
        return cur.lastrowid


def tail_traces(limit=50):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM traces ORDER BY id DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
