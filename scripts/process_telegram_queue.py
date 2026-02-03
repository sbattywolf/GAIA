"""Process and retry items from .tmp/telegram_queue.json.

Usage: python scripts/process_telegram_queue.py
"""
import time
import os
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = ROOT / '.tmp' / 'telegram_queue.json'
FAILED_FILE = ROOT / '.tmp' / 'telegram_queue_failed.json'
BACKUP_FILE = ROOT / '.tmp' / f"telegram_queue.backup.{int(time.time())}.json"
ENV_FILE = ROOT / '.tmp' / 'telegram.env'

def load_env():
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        if '=' not in line: continue
        k,v = line.split('=',1)
        env[k.strip()] = v.strip()
    return env

def safe_load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return []

def safe_save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    os.replace(str(tmp), str(path))

def send_with_retries(tc, token, chat_id, text, reply_to=None, max_attempts=5):
    delay = 1
    for attempt in range(1, max_attempts+1):
        try:
            tc.send_message(token, chat_id, text, reply_to_message_id=reply_to)
            return True, None
        except Exception as e:
            err = str(e)
            if attempt == max_attempts:
                return False, err
            time.sleep(delay)
            delay = min(delay*2, 30)

def main():
    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print('No TELEGRAM_BOT_TOKEN found in .tmp/telegram.env; aborting')
        return 2
    chat_cfg = env.get('CHAT_ID')

    # import local telegram_client and gaia hooks
    from scripts import telegram_client as tc
    from gaia import events, db

    queue = safe_load_json(QUEUE_FILE)
    if not queue:
        print('Queue empty')
        return 0

    # backup
    try:
        QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        safe_save_json(Path(BACKUP_FILE), queue)
        print('Backed up queue to', BACKUP_FILE)
    except Exception as e:
        print('Backup failed:', e)

    failed = safe_load_json(FAILED_FILE) or []
    processed = 0
    errors = []

    while queue:
        item = queue.pop(0)
        chat_id = item.get('chat_id')
        if chat_cfg and str(chat_id) != str(chat_cfg):
            print('Skipping item from other chat', chat_id)
            continue
        mid = item.get('message_id')
        text = (item.get('text') or '').strip()
        reply_text = f"Processing queued message (id:{mid}): '{(text[:200] + '...') if len(text)>200 else text}'"
        ok, err = send_with_retries(tc, token, chat_id, reply_text, reply_to=mid)
        if ok:
            events.make_event('telegram.processed.manual_retry', {'chat_id': chat_id, 'message_id': mid})
            db.write_trace(action='telegram.processed.manual_retry', status='ok', details={'chat_id': chat_id, 'message_id': mid})
            processed += 1
        else:
            print('Failed to send reply for', mid, 'error:', err)
            item['_error'] = err
            item['_failed_at'] = datetime.utcnow().isoformat() + 'Z'
            failed.append(item)
            errors.append({'message_id': mid, 'error': err})
        # persist queue and failed sets
        safe_save_json(QUEUE_FILE, queue)
        safe_save_json(FAILED_FILE, failed)
        time.sleep(0.5)

    print('Done. processed=', processed, 'errors=', len(errors))
    if errors:
        for e in errors:
            print('ERR:', e)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())