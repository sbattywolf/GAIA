"""Session progress runner.

Sends periodic Telegram updates about GAIA monitor health, queue length, and recent events.
Defaults: interval=600s (10 minutes), duration=3600s (1 hour).

Usage:
  python scripts/session_progress_runner.py --interval 600 --duration 3600
"""
import time
import argparse
from pathlib import Path
import json
from datetime import datetime
import locale
try:
    locale.setlocale(locale.LC_TIME, '')
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
from scripts.env_utils import preferred_env_path
ENV_FILE = preferred_env_path(ROOT)
HEALTH_FILE = ROOT / '.tmp' / 'telegram_health.json'
QUEUE_FILE = ROOT / '.tmp' / 'telegram_queue.json'
EVENTS_FILE = ROOT / 'events.ndjson'

def load_env():
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        if '=' not in line: continue
        k,v=line.split('=',1)
        env[k.strip()] = v.strip()
    return env

def read_health():
    try:
        return json.loads(HEALTH_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}

def read_queue_len():
    try:
        q = json.loads(QUEUE_FILE.read_text(encoding='utf-8'))
        return len(q) if isinstance(q, list) else None
    except Exception:
        return None

def recent_event_counts(seconds=3600):
    try:
        if not EVENTS_FILE.exists():
            return 0
        lines = EVENTS_FILE.read_text(encoding='utf-8').splitlines()
        now = datetime.utcnow()
        cnt = 0
        for l in lines[::-1]:
            try:
                e = json.loads(l)
                ts = e.get('timestamp') or e.get('time')
                if not ts:
                    continue
                if isinstance(ts, str) and ts.endswith('Z'):
                    t = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                else:
                    t = datetime.fromisoformat(ts)
                delta = (now - t).total_seconds()
                if delta <= seconds:
                    cnt += 1
                else:
                    break
            except Exception:
                continue
        return cnt
    except Exception:
        return 0

def send_update(token, chat, note):
    from scripts import telegram_client as tc
    try:
        msg = tc.send_message(token, chat, note)
        return msg.get('ok', False)
    except Exception as e:
        return False

def build_note():
    h = read_health()
    qlen = read_queue_len()
    ev_1h = recent_event_counts(3600)
    ev_24h = recent_event_counts(3600*24)
    lines = []
    human_ts = datetime.utcnow().strftime('%a %b %d %Y %H:%M:%S UTC')
    lines.append(f"GAIA Monitor progress update — {human_ts}")
    if h:
        lines.append(f"- Telegram running: {h.get('running')} (processed: {h.get('processed')})")
        ls = h.get('last_seen') or 'never'
        try:
            # try human-friendly last seen
            if ls and ls.endswith('Z'):
                ldt = datetime.fromisoformat(ls.replace('Z', '+00:00'))
                ls_h = ldt.strftime('%a %b %d %Y %H:%M:%S UTC')
            else:
                ls_h = ls
        except Exception:
            ls_h = ls
        lines.append(f"- Last seen: {ls_h}")
    else:
        lines.append("- Telegram health: unknown")
    lines.append(f"- Queue length: {qlen if qlen is not None else 'unknown'}")
    lines.append(f"- Events: last 1h={ev_1h}, 24h={ev_24h}")
    lines.append("- Next update in configured interval until session end.")
    lines.append("")
    lines.append("Note: I will NOT run any commands automatically. If I need to run a script that performs changes, I'll send a separate approval request to this chat — reply APPROVE to allow it.")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--interval', type=int, default=600, help='Seconds between updates')
    p.add_argument('--duration', type=int, default=3600, help='Total session duration seconds')
    args = p.parse_args()

    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    if not token or not chat:
        print('Missing TELEGRAM_BOT_TOKEN or CHAT_ID in .tmp/telegram.env')
        return 2

    end = time.time() + args.duration
    first = True
    while time.time() < end:
        note = build_note()
        ok = send_update(token, chat, note)
        print('Sent update ok=', ok)
        # after first immediate send, sleep interval
        if first:
            first = False
        time.sleep(min(args.interval, max(1, end - time.time())))

    # final message
    send_update(token, chat, 'GAIA Monitor session updates complete — dispatcher and services remain running.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
