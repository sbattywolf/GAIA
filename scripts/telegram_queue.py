"""Simple file-backed Telegram inbound queue with deduplication.

Provides: append_dedup(update) -> bool (True if new), pop_next() -> dict|None,
and list_queue(). Queue stored in `.tmp/telegram_queue.json`. Processed
update ids are recorded in `.tmp/telegram_queue_seen.json` to avoid re-enqueue.
"""
from pathlib import Path
import json
import os
import tempfile
import time
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
    """Pop the next available update respecting `_next_attempt` and
    increment the `_attempts` counter. This avoids processing items
    scheduled for later and provides a simple cooperative retry count.
    """
    q = _safe_load(Q_PATH, [])
    if not q:
        return None
    now = int(time.time())
    for idx, item in enumerate(q):
        next_at = item.get('_next_attempt', 0) or 0
        if next_at and next_at > now:
            # skip items scheduled in the future
            continue
        # remove item from queue
        it = q.pop(idx)
        # increment attempts
        it['_attempts'] = int(it.get('_attempts', 0)) + 1
        it['_last_popped'] = now
        _safe_save(Q_PATH, q)
        return it
    return None


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


def requeue_with_backoff(update: dict, base_delay: int = 30, max_delay: int = 3600, front: bool = True) -> bool:
    """Re-queue an update and set a `_next_attempt` timestamp using
    exponential backoff based on `_attempts`.
    """
    attempts = int(update.get('_attempts', 0))
    # exponential backoff: base_delay * 2^(attempts-1)
    if attempts <= 0:
        delay = base_delay
    else:
        delay = base_delay * (2 ** (attempts - 1))
    if delay > max_delay:
        delay = max_delay
    update['_next_attempt'] = int(time.time()) + int(delay)
    return requeue(update, front=front)
