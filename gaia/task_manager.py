"""Simple task manager that persists user requests as tasks in `gaia.db`."""
import json
import os
import sqlite3
import threading
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'gaia.db')
_lock = threading.Lock()


def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def _init():
    with _lock:
        conn = _conn()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT,
            user_id TEXT,
            message TEXT,
            status TEXT,
            meta TEXT
        )
        ''')
        conn.commit()
        conn.close()


_init()


def create_task(source, user_id, message, meta=None):
    ts = datetime.datetime.utcnow().isoformat() + 'Z'
    with _lock:
        conn = _conn()
        cur = conn.cursor()
        cur.execute('INSERT INTO tasks (timestamp, source, user_id, message, status, meta) VALUES (?, ?, ?, ?, ?, ?)',
                    (ts, source, str(user_id), message, 'open', json.dumps(meta, default=str) if meta else None))
        conn.commit()
        task_id = cur.lastrowid
        conn.close()
    return task_id


def list_tasks(limit=50):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, timestamp, source, user_id, message, status FROM tasks ORDER BY id DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(id=r[0], timestamp=r[1], source=r[2], user_id=r[3], message=r[4], status=r[5]) for r in rows]
