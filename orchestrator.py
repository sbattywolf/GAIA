"""Simple orchestrator stub for GAIA.

Provides a tiny SQLite-backed audit table (existing) and a basic
task queue suitable for local coordination in prototypes.

API provided:
- init_db(): create schema
- enqueue_task(task_type, payload): add a new pending task
- claim_task(worker_id): atomically claim a pending task, returning its row
- complete_task(task_id, result): mark task completed and store result
- fail_task(task_id, error): mark task failed
- list_tasks(status=None): list tasks optionally filtered by status
"""
import sqlite3
import os
import json
from datetime import datetime
import logging

LOG_PATH = os.path.join(os.path.dirname(__file__), 'orchestrator.log')
logger = logging.getLogger('orchestrator')
if not logger.handlers:
    h = logging.FileHandler(LOG_PATH)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    h.setFormatter(fmt)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

DB_PATH = os.path.join(os.path.dirname(__file__), 'gaia.db')


def _connect():
    return sqlite3.connect(DB_PATH, timeout=30)


def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY, timestamp TEXT, actor TEXT, action TEXT, details TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS approvals (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        event_type TEXT,
        task_id TEXT,
        request_id TEXT,
        trace_id TEXT,
        payload TEXT
    )''')
    # project metadata table for simple project tracking (used by dashboard/agents)
    cur.execute('''CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        description TEXT,
        created_at TEXT,
        metadata TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY,
        created_at TEXT,
        task_type TEXT,
        payload TEXT,
        status TEXT,
        owner TEXT,
        started_at TEXT,
        finished_at TEXT,
        result TEXT
    )''')
    conn.commit()

    # ensure migration: add reclaim_attempts and last_reclaimed_at if missing
    cur.execute("PRAGMA table_info(queue)")
    cols = {r[1] for r in cur.fetchall()}
    if 'reclaim_attempts' not in cols:
        try:
            cur.execute('ALTER TABLE queue ADD COLUMN reclaim_attempts INTEGER DEFAULT 0')
        except Exception:
            pass
    if 'last_reclaimed_at' not in cols:
        try:
            cur.execute('ALTER TABLE queue ADD COLUMN last_reclaimed_at TEXT')
        except Exception:
            pass
    conn.commit()

    # ensure migration: add `timestamp` and `actor` columns to `audit` if missing
    try:
        cur.execute("PRAGMA table_info(audit)")
        audit_cols = {r[1] for r in cur.fetchall()}
        if 'timestamp' not in audit_cols:
            try:
                cur.execute("ALTER TABLE audit ADD COLUMN timestamp TEXT")
            except Exception:
                # best-effort migration; ignore if not possible
                pass
        if 'actor' not in audit_cols:
            try:
                cur.execute("ALTER TABLE audit ADD COLUMN actor TEXT")
            except Exception:
                # best-effort migration; ignore if not possible
                pass
    except Exception:
        pass

    conn.commit()
    conn.close()


def write_audit(actor: str, action: str, details: str):
    """Write an audit row to the audit table; best-effort."""
    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()
        cur.execute('INSERT INTO audit (timestamp, actor, action, details) VALUES (?, ?, ?, ?)', (datetime.utcnow().isoformat() + 'Z', actor, action, details))
        conn.commit()
        conn.close()
    except Exception as e:
        try:
            logger.exception('write_audit failed: %s', e)
        except Exception:
            pass


def write_approval(event: dict):
    """Persist an approval event (request/received) into the approvals table.

    Best-effort: does not raise on failure.
    """
    try:
        init_db()
        conn = _connect()
        cur = conn.cursor()
        ts = event.get('timestamp') or (datetime.utcnow().isoformat() + 'Z')
        et = event.get('type')
        task_id = event.get('task_id')
        request_id = event.get('request_id') or (event.get('payload') or {}).get('request_id')
        trace_id = event.get('trace_id') or (event.get('payload') or {}).get('trace_id')
        payload = json.dumps(event.get('payload') or {}, ensure_ascii=False)
        cur.execute('INSERT INTO approvals (timestamp, event_type, task_id, request_id, trace_id, payload) VALUES (?, ?, ?, ?, ?, ?)', (ts, et, task_id, request_id, trace_id, payload))
        conn.commit()
        conn.close()
    except Exception as e:
        try:
            logger.exception('write_approval failed: %s', e)
        except Exception:
            pass


def enqueue_task(task_type: str, payload: dict) -> int:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat() + 'Z'
    cur.execute('INSERT INTO queue (created_at, task_type, payload, status) VALUES (?, ?, ?, ?)', (now, task_type, json.dumps(payload, ensure_ascii=False), 'pending'))
    task_id = cur.lastrowid
    conn.commit()
    conn.close()
    return task_id


def claim_task(worker_id: str):
    """Atomically claim the oldest pending task and mark it in-progress.

    Returns the task row as a dict or None when no pending tasks.
    """
    init_db()
    conn = _connect()
    cur = conn.cursor()
    try:
        # lock the DB to avoid races in concurrent claimers
        cur.execute('BEGIN IMMEDIATE')
        cur.execute("SELECT id, created_at, task_type, payload FROM queue WHERE status = 'pending' ORDER BY created_at LIMIT 1")
        row = cur.fetchone()
        if not row:
            conn.commit()
            return None
        task_id = row[0]
        now = datetime.utcnow().isoformat() + 'Z'
        cur.execute('UPDATE queue SET status = ?, owner = ?, started_at = ? WHERE id = ?', ('in_progress', worker_id, now, task_id))
        conn.commit()
        # return task
        return {'id': task_id, 'created_at': row[1], 'task_type': row[2], 'payload': json.loads(row[3])}
    finally:
        conn.close()


def complete_task(task_id: int, result: dict):
    init_db()
    conn = _connect()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat() + 'Z'
    cur.execute('UPDATE queue SET status = ?, finished_at = ?, result = ? WHERE id = ?', ('completed', now, json.dumps(result, ensure_ascii=False), task_id))
    conn.commit()
    conn.close()


def fail_task(task_id: int, error: str):
    init_db()
    conn = _connect()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat() + 'Z'
    cur.execute('UPDATE queue SET status = ?, finished_at = ?, result = ? WHERE id = ?', ('failed', now, json.dumps({'error': error}, ensure_ascii=False), task_id))
    conn.commit()
    conn.close()


def list_tasks(status: str = None):
    init_db()
    conn = _connect()
    cur = conn.cursor()
    if status:
        cur.execute('SELECT id, created_at, task_type, status, owner FROM queue WHERE status = ? ORDER BY created_at', (status,))
    else:
        cur.execute('SELECT id, created_at, task_type, status, owner FROM queue ORDER BY created_at')
    rows = cur.fetchall()
    conn.close()
    return [{'id': r[0], 'created_at': r[1], 'task_type': r[2], 'status': r[3], 'owner': r[4]} for r in rows]


def reclaim_stale_tasks(ttl_seconds: int = 300, max_attempts: int = 3) -> int:
    """Reclaim tasks stuck in 'in_progress' longer than `ttl_seconds`.

    Moves stale tasks back to 'pending' and clears `owner` and `started_at` so
    they can be claimed again. Returns the number of reclaimed tasks.
    """
    init_db()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, started_at FROM queue WHERE status = 'in_progress'")
    rows = cur.fetchall()
    now = datetime.utcnow()
    reclaimed = []
    for row in rows:
        task_id, started_at = row
        reclaim = False
        if not started_at:
            reclaim = True
        else:
            try:
                s = started_at.rstrip('Z')
                st = datetime.fromisoformat(s)
                if (now - st).total_seconds() > ttl_seconds:
                    reclaim = True
            except Exception:
                reclaim = True

        if not reclaim:
            continue

        # check current attempts
        cur.execute('SELECT reclaim_attempts FROM queue WHERE id = ?', (task_id,))
        r = cur.fetchone()
        attempts = r[0] if r and r[0] is not None else 0

        # max_attempts parameter controls how many times a task may be reclaimed
        # before being marked as failed to avoid flapping.
        # It's provided by the caller (default 3).
        if attempts >= max_attempts:
            # give up and mark failed to avoid flapping
            cur.execute('UPDATE queue SET status = ?, finished_at = ?, result = ? WHERE id = ?', ('failed', datetime.utcnow().isoformat() + 'Z', json.dumps({'error': 'reclaim_max_attempts'}), task_id))
            try:
                cur.execute('INSERT INTO audit (timestamp, actor, action, details) VALUES (?, ?, ?, ?)', (datetime.utcnow().isoformat() + 'Z', 'orchestrator', 'reclaim_failed', json.dumps({'task_id': task_id, 'reason': 'reclaim_max_attempts'})))
            except Exception:
                logger.exception('failed to write reclaim_failed audit for %s', task_id)
        else:
            # increment attempts and move back to pending
            attempts += 1
            cur.execute('UPDATE queue SET status = ?, owner = NULL, started_at = NULL, reclaim_attempts = ?, last_reclaimed_at = ? WHERE id = ?', ('pending', attempts, datetime.utcnow().isoformat() + 'Z', task_id))
            reclaimed.append(task_id)
            try:
                cur.execute('INSERT INTO audit (timestamp, actor, action, details) VALUES (?, ?, ?, ?)', (datetime.utcnow().isoformat() + 'Z', 'orchestrator', 'reclaim', json.dumps({'task_id': task_id, 'attempts': attempts})))
            except Exception:
                logger.exception('failed to write reclaim audit for %s', task_id)

    conn.commit()
    conn.close()
    return len(reclaimed)


def reclaim_and_report(ttl_seconds: int = 300, max_attempts: int = 3, status_path: str = None):
    """Run reclaim and produce a small metrics report.

    Returns a dict with keys: reclaimed, reclaim_audit_reclaim, reclaim_audit_failed,
    pending, in_progress, timestamp.
    Optionally writes the dict as JSON to `status_path`.
    """
    start = datetime.utcnow()
    reclaimed = reclaim_stale_tasks(ttl_seconds, max_attempts)

    # count audit rows written since start
    conn = _connect()
    cur = conn.cursor()
    start_iso = start.isoformat() + 'Z'
    cur.execute("SELECT COUNT(*) FROM audit WHERE action = 'reclaim' AND timestamp >= ?", (start_iso,))
    reclaim_audit_reclaim = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM audit WHERE action = 'reclaim_failed' AND timestamp >= ?", (start_iso,))
    reclaim_audit_failed = cur.fetchone()[0]
    # count pending/in_progress
    cur.execute("SELECT COUNT(*) FROM queue WHERE status = 'pending'")
    pending = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM queue WHERE status = 'in_progress'")
    inprog = cur.fetchone()[0]
    conn.close()

    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'reclaimed': reclaimed,
        'reclaim_audit_reclaim': reclaim_audit_reclaim,
        'reclaim_audit_failed': reclaim_audit_failed,
        'pending': pending,
        'in_progress': inprog,
    }

    if status_path:
        try:
            with open(status_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        except Exception:
            logger.exception('failed to write status file %s', status_path)

    return report


if __name__ == '__main__':
    init_db()
    # Run startup token validation early; fail fast if required tokens are missing
    try:
        try:
            # import the startup check helper from scripts
            from scripts.agent_startup_check import main as agent_startup_main
            agent_startup_main()
        except SystemExit as e:
            # propagate non-zero exit codes to stop startup
            if e.code != 0:
                print('Agent startup check failed; exiting with code', e.code)
                raise
        except Exception as e:
            # log but continue on unexpected errors in startup check
            logger.exception('agent_startup_check failed: %s', e)
    except Exception:
        # If the startup check indicated an impediment, abort startup
        import sys
        sys.exit(1)

    print('GAIA orchestrator initialized. DB at', DB_PATH)
