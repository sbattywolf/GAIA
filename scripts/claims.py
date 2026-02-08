import os
import json
import time
import uuid
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLAIMS_DIR = os.path.join(ROOT, ".tmp", "claims")

def _ensure_dir():
    os.makedirs(CLAIMS_DIR, exist_ok=True)

def _safe_name(story, todolist):
    name = f"{story}.{todolist}".replace("/", "_").replace("\\", "_")
    return name

def _path_for(story, todolist):
    _ensure_dir()
    name = _safe_name(story, todolist) + ".json"
    return os.path.join(CLAIMS_DIR, name)

def _now_ts():
    return time.time()

def _now_iso():
    return datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

def _read_claim(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def _acquire_lock_for(path, timeout=0.5):
    lock_path = path + ".lock"
    # allow overriding lock timeout via env var for noisy systems
    try:
        env_timeout = float(os.getenv("CLAIMS_LOCK_TIMEOUT", "5.0"))
    except Exception:
        env_timeout = 5.0
    if timeout is None:
        timeout = env_timeout

    start = time.time()
    backoff = 0.01
    while time.time() - start < timeout:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            return True
        except FileExistsError:
            time.sleep(backoff)
            # exponential backoff with cap to avoid long sleeps
            backoff = min(backoff * 2, 0.1)
    return False


def _release_lock_for(path):
    lock_path = path + ".lock"
    try:
        os.remove(lock_path)
    except Exception:
        pass

def _write_atomic(path, data):
    tmp = path + "." + uuid.uuid4().hex + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        try:
            os.fsync(f.fileno())
        except Exception:
            pass

    # simple file-based lock to avoid concurrent replace races on Windows
    lock_path = path + ".lock"
    try:
        write_timeout = float(os.getenv("CLAIMS_LOCK_TIMEOUT", "5.0"))
    except Exception:
        write_timeout = 5.0
    start = time.time()
    got = False
    backoff = 0.01
    while time.time() - start < write_timeout:
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            got = True
            break
        except FileExistsError:
            time.sleep(backoff)
            backoff = min(backoff * 2, 0.1)
    try:
        if not got:
            # fallback to replace without lock (last-wins)
            os.replace(tmp, path)
        else:
            try:
                os.replace(tmp, path)
            finally:
                try:
                    os.remove(lock_path)
                except Exception:
                    pass
    except Exception:
        # best-effort cleanup of tmp file
        try:
            os.remove(tmp)
        except Exception:
            pass
        raise

def inspect_claim(story, todolist):
    path = _path_for(story, todolist)
    return _read_claim(path)

def claim(story, todolist, owner, agent_id, fingerprint, ttl_seconds=300):
    """Attempt to claim a todo list. Returns (True, claim) on success or (False, reason).

    Claim file fields: owner, agent_id, fingerprint, claimed_at (iso), ttl_seconds, version
    """
    path = _path_for(story, todolist)
    got = _acquire_lock_for(path)
    if not got:
        return False, "lock-timeout"
    try:
        now = _now_ts()
        existing = _read_claim(path)
        if existing:
            try:
                claimed_at = datetime.fromisoformat(existing.get("claimed_at")).timestamp()
            except Exception:
                claimed_at = 0
            existing_ttl = existing.get("ttl_seconds", 0)
            if now <= claimed_at + existing_ttl:
                return False, f"already claimed by {existing.get('owner')}"
            # expired -> allow take-over
            version = existing.get("version", 0) + 1
        else:
            version = 1

        claim_obj = {
            "owner": owner,
            "agent_id": agent_id,
            "fingerprint": fingerprint,
            "claimed_at": _now_iso(),
            "ttl_seconds": int(ttl_seconds),
            "version": int(version),
        }
        _write_atomic(path, claim_obj)
        return True, claim_obj
    finally:
        _release_lock_for(path)

def release(story, todolist, agent_id=None, fingerprint=None):
    path = _path_for(story, todolist)
    got = _acquire_lock_for(path)
    if not got:
        return False, "lock-timeout"
    try:
        existing = _read_claim(path)
        if not existing:
            return False, "no-existing-claim"
        if agent_id and existing.get("agent_id") != agent_id and existing.get("fingerprint") != fingerprint:
            return False, "not-owner"
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        return True, "released"
    finally:
        _release_lock_for(path)

def refresh(story, todolist, agent_id=None, fingerprint=None, ttl_seconds=None):
    path = _path_for(story, todolist)
    got = _acquire_lock_for(path)
    if not got:
        return False, "lock-timeout"
    try:
        existing = _read_claim(path)
        if not existing:
            return False, "no-existing-claim"
        if agent_id and existing.get("agent_id") != agent_id and existing.get("fingerprint") != fingerprint:
            return False, "not-owner"
        existing["claimed_at"] = _now_iso()
        if ttl_seconds is not None:
            existing["ttl_seconds"] = int(ttl_seconds)
        existing["version"] = int(existing.get("version", 0)) + 1
        _write_atomic(path, existing)
        return True, existing
    finally:
        _release_lock_for(path)


# Optional SQLite backend override. Enable by setting CLAIMS_BACKEND=sqlite
_USE_SQLITE = os.getenv("CLAIMS_BACKEND", "").lower() == "sqlite" or os.getenv("CLAIMS_USE_SQLITE", "").lower() in ("1", "true")
if _USE_SQLITE:
    try:
        from .claims_sqlite import inspect_claim as _ci, claim as _cc, release as _cr, refresh as _cf
        inspect_claim = _ci
        claim = _cc
        release = _cr
        refresh = _cf
    except Exception:
        # fall back to file-based implementation if import fails
        pass
