import json
import os
from datetime import datetime
import uuid
import hashlib
import time
import subprocess
import sys
from pathlib import Path


def build_event(event_type, source, payload, target=None, task_id=None):
    return {
        'type': event_type,
        'source': source,
        'target': target or os.path.basename(os.getcwd()),
        'task_id': task_id,
        'payload': payload,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'trace_id': str(uuid.uuid4()),
    }


def append_event_atomic(path, event):
    # simple atomic append: open in append mode and write newline-terminated JSON
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + '\n')


def is_dry_run():
    # PROTOTYPE_USE_LOCAL_EVENTS=1 means local-only; also support explicit DRY_RUN env
    return os.environ.get('PROTOTYPE_USE_LOCAL_EVENTS') == '1' or os.environ.get('DRY_RUN') == '1'


def idempotency_key(source: str, payload: dict) -> str:
    """Generate a short deterministic idempotency key for an event.

    Uses SHA256 over source + sorted JSON of payload to produce a stable key.
    """
    j = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    h = hashlib.sha256((source + '|' + j).encode('utf-8')).hexdigest()
    return h[:32]


def retry_with_backoff(fn, retries: int = 3, base_backoff: float = 0.5, exceptions=(Exception,), sleep=time.sleep):
    """Simple retry helper with exponential backoff.

    `sleep` is injectable for tests to avoid real delays.
    Returns the function result or re-raises the last exception.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except exceptions as e:
            last_exc = e
            if attempt == retries:
                break
            backoff = base_backoff * (2 ** (attempt - 1))
            sleep(backoff)
    raise last_exc


def run_script(script_path: str, args: list = None, timeout: int = None) -> dict:
    """Run a script via `scripts/run_script.py` to ensure correct interpreter.

    Returns a dict: {'rc': int, 'stdout': str, 'stderr': str}
    """
    args = args or []
    root = Path(__file__).resolve().parent.parent
    runner = root / 'scripts' / 'run_script.py'
    cmd = [sys.executable, str(runner), script_path] + args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {'rc': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
    except Exception as e:
        return {'rc': 255, 'stdout': '', 'stderr': str(e)}
