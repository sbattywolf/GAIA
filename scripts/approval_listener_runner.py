#!/usr/bin/env python3
"""Standalone approval listener runner that does not import `gaia` package.
Writes approval events to `events.ndjson` and inserts a trace into `gaia.db`.
"""
import os
import time
import json
import sqlite3
import argparse
import requests
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')
DB_PATH = os.path.join(ROOT, 'gaia.db')
APPR_FILE = os.path.join(ROOT, '.tmp', 'approval.json')


def now():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def append_event(evt):
    try:
        with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, default=str) + '\n')
    except Exception as e:
        print('WARN append_event', e)


def write_trace(action, status, details=None):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT,
            agent_id TEXT,
            status TEXT,
            details TEXT
        )''')
        conn.commit()
        cur.execute('INSERT INTO traces (timestamp, action, status, details) VALUES (?, ?, ?, ?)',
                    (now(), action, status, json.dumps(details, default=str) if details is not None else None))
        conn.commit()
        conn.close()
    except Exception as e:
        print('WARN write_trace', e)


def write_approval_file(payload):
    try:
        os.makedirs(os.path.join(ROOT, '.tmp'), exist_ok=True)
        with open(APPR_FILE, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
    except Exception as e:
        print('WARN write_approval_file', e)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--timeout', type=int, default=1800)
    p.add_argument('--poll', type=int, default=5)
    args = p.parse_args()

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id_env = os.environ.get('CHAT_ID')
    if not token:
        print('ERROR: TELEGRAM_BOT_TOKEN env required')
        return 2

    url = f'https://api.telegram.org/bot{token}/getUpdates'
    offset = None
    deadline = time.time() + args.timeout
    print('Listening for APPROVE messages until', time.ctime(deadline))

    while time.time() < deadline:
        try:
            params = {}
            if offset:
                params['offset'] = offset
            r = requests.get(url, params=params, timeout=10)
            j = r.json()
            for item in j.get('result', []):
                offset = item['update_id'] + 1
                msg = item.get('message') or item.get('channel_post')
                if not msg:
                    continue
                chat = msg.get('chat', {})
                text = msg.get('text', '')
                from_id = chat.get('id')
                print('Got message from', from_id, 'text=', text)
                if chat_id_env and str(from_id) != str(chat_id_env):
                    print('Ignoring message from other chat', from_id)
                    continue
                if isinstance(text, str) and text.strip().upper() == 'APPROVE':
                    payload = {'approved_by': from_id, 'timestamp': now(), 'raw': msg}
                    append_event({'type': 'approval.received', 'payload': payload, 'timestamp': now()})
                    write_trace('approval.received', 'ok', payload)
                    write_approval_file(payload)
                    print('Approval recorded')
                    return 0
        except Exception as e:
            print('poll error:', e)
        time.sleep(args.poll)
    print('Timeout waiting for approval')
    append_event({'type': 'approval.timeout', 'payload': {'timeout': args.timeout}, 'timestamp': now()})
    write_trace('approval.timeout', 'timeout', {'timeout': args.timeout})
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
