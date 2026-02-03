"""Telegram service: long-poll getUpdates, enqueue messages, send friendly ACKs, and maintain health/pid files.

Usage: python scripts/telegram_service.py --timeout 0 --poll 5
"""
import os
import time
import json
import argparse
import random
import tempfile
import signal
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = ROOT / '.tmp' / 'telegram_queue.json'
STATE_FILE = ROOT / '.tmp' / 'telegram_state.json'
PID_FILE = ROOT / '.tmp' / 'telegram_service.pid'
HEALTH_FILE = ROOT / '.tmp' / 'telegram_health.json'

from scripts import telegram_client as tc
from scripts import tg_command_manager as tcm
from gaia import events, db


def now():
    return datetime.utcnow().isoformat() + 'Z'


def safe_load(p):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def safe_save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    os.replace(str(tmp), str(p))


WARM_ACKS = [
    "Thanks — I'll check and report back shortly.",
    "Got it — I'm on it and will update you soon.",
    "Appreciate the heads-up — I'll investigate and reply.",
]


def write_pid():
    os.makedirs(PID_FILE.parent, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='tgsvc_pid_', suffix='.tmp', dir=str(PID_FILE.parent))
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(str(os.getpid()))
    os.replace(tmp, str(PID_FILE))


def remove_pid():
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception:
        pass


def update_health(running=True, last_seen=None, processed=None):
    h = safe_load(HEALTH_FILE) or {}
    h['running'] = running
    h['started'] = h.get('started') or now()
    if last_seen:
        h['last_seen'] = last_seen
    if processed is not None:
        h['processed'] = processed
    h['last_update'] = now()
    safe_save(HEALTH_FILE, h)


def enqueue(item):
    q = safe_load(QUEUE_FILE) or []
    # dedupe by message_id
    mid = item.get('message_id')
    if any(x.get('message_id') == mid for x in q):
        return False
    q.append(item)
    safe_save(QUEUE_FILE, q)
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--timeout', type=int, default=0, help='Seconds to run (0=infinite)')
    p.add_argument('--poll', type=int, default=10, help='Long-poll timeout (max 60)')
    args = p.parse_args()

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_cfg = os.environ.get('CHAT_ID')
    if not token:
        print('ERROR: TELEGRAM_BOT_TOKEN missing')
        return 2

    # write pid
    try:
        write_pid()
    except Exception:
        pass

    def _cleanup(signum=None, frame=None):
        update_health(running=False)
        remove_pid()
        raise SystemExit(0)

    try:
        signal.signal(signal.SIGINT, _cleanup)
        signal.signal(signal.SIGTERM, _cleanup)
    except Exception:
        pass

    # load state
    state = safe_load(STATE_FILE) or {}
    offset = state.get('offset')
    processed = 0
    deadline = time.time() + args.timeout if args.timeout > 0 else None

    update_health(running=True, last_seen=None, processed=processed)

    lp = min(max(1, int(args.poll)), 60)

    print('Starting telegram_service (poll=%s) pid=%s' % (lp, os.getpid()))

    while True:
        if deadline and time.time() >= deadline:
            break
        try:
            resp = tc.get_updates(token, offset=offset, timeout=lp)
            if not resp or not resp.get('ok'):
                time.sleep(1)
                continue
            for upd in resp.get('result', []):
                offset = upd['update_id'] + 1
                # persist offset
                state['offset'] = offset
                safe_save(STATE_FILE, state)
                msg = upd.get('message') or upd.get('channel_post')
                if not msg:
                    continue
                chat = msg.get('chat') or {}
                chat_id = chat.get('id')
                text = msg.get('text') or ''
                sender = msg.get('from') or {}
                processed += 1
                update_health(running=True, last_seen=now(), processed=processed)

                # respect CHAT_ID if configured
                if chat_cfg and str(chat_id) != str(chat_cfg):
                    continue

                print('Got message', chat_id, text[:80])

                # immediate friendly ACK for short messages
                try:
                    first = sender.get('first_name')
                    warm = random.choice(WARM_ACKS)
                    if first:
                        ack = f"Hi {first}! {warm}"
                    else:
                        ack = warm
                    tc.send_message(token, chat_id, ack, reply_to_message_id=msg.get('message_id'))
                except Exception:
                    pass

                item = {
                    'chat_id': chat_id,
                    'message_id': msg.get('message_id'),
                    'text': text,
                    'from': sender,
                    'ts': now(),
                }
                en = enqueue(item)
                # also check for embedded commands and enqueue them for manual approval
                try:
                    added_cmds = tcm.enqueue_command(chat_id, msg.get('message_id'), text, sender)
                    if added_cmds:
                        events.make_event('telegram.command.enqueued', {'chat_id': chat_id, 'message_id': msg.get('message_id'), 'commands': [c['id'] for c in added_cmds]})
                        db.write_trace(action='telegram.command.enqueued', status='ok', details={'chat_id': chat_id, 'message_id': msg.get('message_id'), 'count': len(added_cmds)})
                except Exception:
                    # do not interrupt main loop on command-manager errors
                    pass
                if en:
                    events.make_event('telegram.enqueued', {'chat_id': chat_id, 'message_id': msg.get('message_id')})
                    db.write_trace(action='telegram.enqueued', status='ok', details=item)

        except Exception as e:
            print('poll error', e)
            time.sleep(2)
            continue

    update_health(running=False, last_seen=now(), processed=processed)
    remove_pid()
    print('telegram_service exiting')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
