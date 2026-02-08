import os
import sqlite3
import time
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(ROOT, ".tmp")
DB_PATH = os.path.join(DB_DIR, "claims.db")

def _ensure_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA synchronous=NORMAL")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS claims (
                story TEXT NOT NULL,
                todolist TEXT NOT NULL,
                owner TEXT,
                agent_id TEXT,
                fingerprint TEXT,
                claimed_at TEXT,
                ttl_seconds INTEGER,
                version INTEGER,
                PRIMARY KEY(story, todolist)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def _now_ts():
    return time.time()


def _now_iso():
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()


def inspect_claim(story, todolist):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH, timeout=30)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT owner,agent_id,fingerprint,claimed_at,ttl_seconds,version FROM claims WHERE story=? AND todolist=?",
            (story, todolist),
        )
        row = cur.fetchone()
        if not row:
            return None
        owner, agent_id, fingerprint, claimed_at, ttl_seconds, version = row
        return {
            "owner": owner,
            "agent_id": agent_id,
            "fingerprint": fingerprint,
            "claimed_at": claimed_at,
            "ttl_seconds": ttl_seconds,
            "version": version,
        }
    finally:
        conn.close()


def claim(story, todolist, owner, agent_id, fingerprint, ttl_seconds=300):
    """Attempt to claim using SQLite transactional semantics."""
    _ensure_db()
    conn = sqlite3.connect(DB_PATH, timeout=30)
    try:
        # begin immediate to obtain a RESERVED lock for update
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.cursor()
        cur.execute(
            "SELECT owner,claimed_at,ttl_seconds,version,agent_id,fingerprint FROM claims WHERE story=? AND todolist=?",
            (story, todolist),
        )
        row = cur.fetchone()
        now = _now_ts()
        if row:
            existing_owner, claimed_at_iso, existing_ttl, version, existing_agent, existing_fp = row
            try:
                claimed_at = datetime.fromisoformat(claimed_at_iso).timestamp()
            except Exception:
                claimed_at = 0
            if now <= claimed_at + (existing_ttl or 0):
                conn.rollback()
                return False, f"already claimed by {existing_owner}"
            new_version = (version or 0) + 1
            claimed_at_iso = _now_iso()
            cur.execute(
                "UPDATE claims SET owner=?,agent_id=?,fingerprint=?,claimed_at=?,ttl_seconds=?,version=? WHERE story=? AND todolist=?",
                (owner, agent_id, fingerprint, claimed_at_iso, int(ttl_seconds), int(new_version), story, todolist),
            )
            conn.commit()
            return True, {
                "owner": owner,
                "agent_id": agent_id,
                "fingerprint": fingerprint,
                "claimed_at": claimed_at_iso,
                "ttl_seconds": int(ttl_seconds),
                "version": int(new_version),
            }
        else:
            claimed_at_iso = _now_iso()
            cur.execute(
                "INSERT INTO claims(story,todolist,owner,agent_id,fingerprint,claimed_at,ttl_seconds,version) VALUES(?,?,?,?,?,?,?,?)",
                (story, todolist, owner, agent_id, fingerprint, claimed_at_iso, int(ttl_seconds), 1),
            )
            conn.commit()
            return True, {
                "owner": owner,
                "agent_id": agent_id,
                "fingerprint": fingerprint,
                "claimed_at": claimed_at_iso,
                "ttl_seconds": int(ttl_seconds),
                "version": 1,
            }
    except Exception as exc:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        conn.close()


def release(story, todolist, agent_id=None, fingerprint=None):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH, timeout=30)
    try:
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.cursor()
        cur.execute("SELECT agent_id,fingerprint FROM claims WHERE story=? AND todolist=?", (story, todolist))
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False, "no-existing-claim"
        existing_agent, existing_fp = row
        if agent_id and existing_agent != agent_id and existing_fp != fingerprint:
            conn.rollback()
            return False, "not-owner"
        cur.execute("DELETE FROM claims WHERE story=? AND todolist=?", (story, todolist))
        conn.commit()
        return True, "released"
    finally:
        conn.close()


def refresh(story, todolist, agent_id=None, fingerprint=None, ttl_seconds=None):
    _ensure_db()
    conn = sqlite3.connect(DB_PATH, timeout=30)
    try:
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.cursor()
        cur.execute(
            "SELECT agent_id,fingerprint,ttl_seconds,version FROM claims WHERE story=? AND todolist=?",
            (story, todolist),
        )
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False, "no-existing-claim"
        existing_agent, existing_fp, existing_ttl, version = row
        if agent_id and existing_agent != agent_id and existing_fp != fingerprint:
            conn.rollback()
            return False, "not-owner"
        claimed_at_iso = _now_iso()
        new_ttl = int(ttl_seconds) if ttl_seconds is not None else existing_ttl
        new_version = (version or 0) + 1
        cur.execute(
            "UPDATE claims SET claimed_at=?,ttl_seconds=?,version=? WHERE story=? AND todolist=?",
            (claimed_at_iso, new_ttl, int(new_version), story, todolist),
        )
        conn.commit()
        return True, {
            "owner": existing_agent,
            "agent_id": existing_agent,
            "fingerprint": existing_fp,
            "claimed_at": claimed_at_iso,
            "ttl_seconds": new_ttl,
            "version": int(new_version),
        }
    finally:
        conn.close()
