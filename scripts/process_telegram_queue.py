"""Retry worker for failed Telegram outbound actions.

Reads `.tmp/telegram_queue_failed.json` (written by the listener/client when
outbound calls fail) and attempts to retry the action. Transient errors are
retried with exponential backoff; permanent failures (client 4xx except 429)
are moved to a permanent failed file for manual inspection.

Exports `process_failed_items_once()` for testability and a `main()` loop.
"""

import time
import os
import json
from pathlib import Path
from datetime import datetime

from gaia import events as gaia_events
from scripts import metrics as metrics

ROOT = Path(__file__).resolve().parents[1]
FAILED_FILE = ROOT / '.tmp' / 'telegram_queue_failed.json'
PERM_FAILED_FILE = ROOT / '.tmp' / 'telegram_queue_failed_permanent.json'
from scripts.env_utils import preferred_env_path
ENV_FILE = preferred_env_path(ROOT)


def load_env():
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def safe_load_json(path: Path):
    try:
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding='utf-8')) or []
    except Exception:
        return []


def safe_save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    try:
        os.replace(str(tmp), str(path))
    except Exception:
        path.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def _classify_exception(e):
    # Prefer to inspect requests' HTTPError.response.status_code when available
    try:
        import requests
        # if it's a requests HTTPError, use the response
        if isinstance(e, requests.exceptions.HTTPError):
            resp = getattr(e, 'response', None)
            if resp is not None:
                code = getattr(resp, 'status_code', None)
                if code is not None:
                    code = int(code)
                    if 400 <= code < 500 and code != 429:
                        return 'permanent'
                    return 'transient'
        # network-level RequestException are transient
        if isinstance(e, requests.exceptions.RequestException):
            return 'transient'
    except Exception:
        pass

    # Fallbacks: check common attributes or strings
    try:
        resp = getattr(e, 'response', None)
        if resp is not None:
            code = getattr(resp, 'status_code', None)
            if code is not None:
                code = int(code)
                if 400 <= code < 500 and code != 429:
                    return 'permanent'
                return 'transient'
    except Exception:
        pass

    try:
        s = str(e)
        for token in (' 400', ' 401', ' 403', ' 404', 'bad request'):
            if token in s.lower():
                return 'permanent'
    except Exception:
        pass

    return 'transient'


def _perform_action(item, env):
    """Perform the outbound action described by `item`.

    Returns (True, None) on success, (False, error_message) on failure where
    error_message is the exception string.
    """
    from scripts import telegram_client as tc

    token = env.get('TELEGRAM_BOT_TOKEN')
    if not token:
        return False, 'no_token'

    action = item.get('action')
    try:
        if action == 'answer_callback':
            cqid = item.get('callback_query_id') or (item.get('update') or {}).get('callback_query', {}).get('id')
            text = item.get('text')
            # call answer_callback; tc.answer_callback will apply its own retries
            tc.answer_callback(token, cqid, text=text)
            return True, None
        elif action == 'send_message':
            chat = item.get('chat_id') or (item.get('update') or {}).get('message', {}).get('chat', {}).get('id')
            text = item.get('text') or item.get('body')
            tc.send_message(token, chat, text, reply_to_message_id=item.get('reply_to'))
            return True, None
        else:
            # unknown action - treat as permanent
            return False, 'unknown_action'
    except Exception as e:
        # return exception object for richer classification
        return False, e


def process_failed_items_once():
    """Process the failed-file once. Returns a dict with summary."""
    env = load_env()
    # Fallback to environment variables for keys not present in the env file.
    for key in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        # prefer a non-empty value from the environment if the env file has no value
        if (key not in env or not env.get(key)) and key in os.environ:
            env[key] = os.environ.get(key)
    attempts = int(os.environ.get('TELEGRAM_RETRY_WORKER_ATTEMPTS', '3'))
    backoff_ms = int(os.environ.get('TELEGRAM_RETRY_WORKER_BACKOFF_MS', '500'))

    failed = safe_load_json(FAILED_FILE) or []
    if not failed:
        return {'processed': 0, 'succeeded': 0, 'moved_permanent': 0}

    perm = safe_load_json(PERM_FAILED_FILE) or []
    new_failed = []
    succeeded = 0
    moved_permanent = 0

    from gaia import db as gaia_db

    for item in failed:
        retries = int(item.get('_retries', 0))
        success = False
        last_err = None
        # emit trace for start
        try:
            gaia_db.write_trace('telegram.retry.attempt', agent_id='retryer', status='start', details={'id': item.get('callback_query_id') or item.get('update', {}).get('update_id'), 'retries': retries})
        except Exception:
            pass
        try:
            metrics.increment('telegram.retry.attempt.start')
        except Exception:
            pass

        for attempt in range(retries + 1, attempts + 1):
            ok, err = _perform_action(item, env)
            if ok:
                success = True
                try:
                    gaia_db.write_trace('telegram.retry.attempt', agent_id='retryer', status='ok', details={'id': item.get('callback_query_id') or item.get('update', {}).get('update_id'), 'attempt': attempt})
                except Exception:
                    pass
                try:
                    metrics.increment('telegram.retry.succeeded')
                except Exception:
                    pass
                break
            last_err = err
            try:
                gaia_db.write_trace('telegram.retry.attempt', agent_id='retryer', status='error', details={'id': item.get('callback_query_id') or item.get('update', {}).get('update_id'), 'attempt': attempt, 'error': str(err)})
            except Exception:
                pass
            try:
                metrics.increment('telegram.retry.attempt.error')
            except Exception:
                pass
            # classify
            cls = 'transient'
            try:
                # attempt to classify by parsing simple status code if present
                if isinstance(err, str) and err.isdigit():
                    code = int(err)
                    if 400 <= code < 500 and code != 429:
                        cls = 'permanent'
                else:
                    # if exception string mentions 400/401/403/404 treat permanent
                    s = (err or '').lower()
                    if '400' in s or '401' in s or '403' in s or '404' in s or 'bad request' in s:
                        cls = 'permanent'
            except Exception:
                cls = 'transient'

            if cls == 'permanent':
                break

            # backoff before next attempt
            try:
                time.sleep((backoff_ms / 1000.0) * (2 ** (attempt - 1)))
            except Exception:
                pass

        if success:
            succeeded += 1
            try:
                gaia_events.make_event('telegram.retry.succeeded', {'id': item.get('callback_query_id') or item.get('update', {}).get('update_id')})
            except Exception:
                pass
            continue

        # failed after attempts or classified permanent
        # if classification permanent or retries exhausted, move to permanent
        perm.append({**item, '_error': str(last_err), '_failed_at': datetime.utcnow().isoformat() + 'Z'})
        moved_permanent += 1
        try:
            metrics.increment('telegram.retry.moved_permanent')
        except Exception:
            pass

    # persist
    safe_save_json(PERM_FAILED_FILE, perm)
    # any items not processed are removed from FAILED_FILE (we moved all to perm or succeeded)
    safe_save_json(FAILED_FILE, [])
    return {'processed': len(failed), 'succeeded': succeeded, 'moved_permanent': moved_permanent}


def main(poll=30):
    try:
        while True:
            out = process_failed_items_once()
            if out.get('processed', 0):
                print('processed', out)
            time.sleep(poll)
    except KeyboardInterrupt:
        print('stopped')


if __name__ == '__main__':
    raise SystemExit(main())
