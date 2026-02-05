#!/usr/bin/env python3
"""Periodic Telegram notifier.

Reads `.private/.env` for `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` and posts
an initial heartbeat and periodic summaries every `interval` seconds.

Usage: python scripts/telegram_notifier.py [interval_seconds]
"""
import os
import time
import json
import requests
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
PRIVATE_ENV = os.path.join(ROOT, '.private', '.env')
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')


def read_env(path):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def send_telegram(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def summarize_events(n=20):
    if not os.path.exists(EVENTS_FILE):
        return 'No events yet.'
    lines = []
    with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)
    if not lines:
        return 'No events yet.'
    tail = lines[-n:]
    summary = []
    for l in tail:
        try:
            j = json.loads(l)
            t = j.get('type', 'event')
            ts = j.get('timestamp', '')
            tid = j.get('task_id') or j.get('task') or ''
            summary.append(f"{ts} {t} {tid}")
        except Exception:
            summary.append(l[:140])
    return '\n'.join(summary)


def tail_automation_log(n=50):
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp', 'automation.log')
    if not os.path.exists(log_path):
        return 'No automation.log yet.'
    lines = []
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                lines.append(line.strip())
    if not lines:
        return 'No automation.log yet.'
    return '\n'.join(lines[-n:])


def main():
    import sys
    interval = 120
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except Exception:
            pass
    env = read_env(PRIVATE_ENV)
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('TELEGRAM_CHAT_ID')
    if not token or not chat:
        print('TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in .private/.env')
        return

    send_telegram(token, chat, f'Automation notifier starting at {datetime.utcnow().isoformat()}Z; interval={interval}s')
    last_summary = ''
    while True:
        summary = summarize_events(10)
        if summary != last_summary:
            msg = f'Automation summary (last events):\n{summary}'
            ok = send_telegram(token, chat, msg)
            if ok:
                last_summary = summary
        time.sleep(interval)


if __name__ == '__main__':
    main()
