"""Simple file-backed Telegram inbound queue with deduplication.

Provides: append_dedup(update) -> bool (True if new), pop_next() -> dict|None,
and list_queue(). Queue stored in `.tmp/telegram_queue.json`. Processed
update ids are recorded in `.tmp/telegram_queue_seen.json` to avoid re-enqueue.
"""
from pathlib import Path
import json
import os
import tempfile
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
Q_PATH = ROOT / '.tmp' / 'telegram_queue.json'
SEEN_PATH = ROOT / '.tmp' / 'telegram_queue_seen.json'


def _safe_load(path: Path, default):
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def _safe_save(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    try:
        tmp.replace(path)
    except Exception:
        path.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def _get_update_id(update: dict) -> Optional[int]:
    try:
        return int(update.get('update_id'))
    except Exception:
        return None


def append_dedup(update: dict) -> bool:
    """Append update to queue if not already seen.

    Returns True if the update was appended (new), False if it was a duplicate.
    """
    uid = _get_update_id(update)
    seen = set(_safe_load(SEEN_PATH, []))
    if uid is not None and uid in seen:
        return False

    # also dedupe by callback id/message id if update has them
    # fallback: scan existing queue for same update_id
    q = _safe_load(Q_PATH, [])
    for it in q:
        if _get_update_id(it) == uid and uid is not None:
            return False

    q.append(update)
    _safe_save(Q_PATH, q)
    if uid is not None:
        seen.add(uid)
        _safe_save(SEEN_PATH, sorted(list(seen)))
    return True


def pop_next() -> Optional[dict]:
    q = _safe_load(Q_PATH, [])
    if not q:
        return None
    item = q.pop(0)
    _safe_save(Q_PATH, q)
    return item


def list_queue() -> list:
    return _safe_load(Q_PATH, [])


def clear():
    try:
        if Q_PATH.exists():
            Q_PATH.unlink()
    except Exception:
        pass
    try:
        if SEEN_PATH.exists():
            SEEN_PATH.unlink()
    except Exception:
        pass


def requeue(update: dict, front: bool = True) -> bool:
    """Re-insert an update into the queue without touching the seen set.

    This is used to re-queue items on transient processing failures. By
    not modifying `SEEN_PATH` we allow the system to avoid losing the
    ability to dedupe arrival-side duplicates while still retrying the
    current item.
    """
    q = _safe_load(Q_PATH, [])
    try:
        if front:
            q.insert(0, update)
        else:
            q.append(update)
        _safe_save(Q_PATH, q)
        return True
    except Exception:
        return False
