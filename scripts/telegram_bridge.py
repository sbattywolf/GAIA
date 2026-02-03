#!/usr/bin/env python3
"""Telegram bridge: polls bot getUpdates and turns user messages into tasks.
Acks the user with a short confirmation containing the task id.

Env vars used: TELEGRAM_BOT_TOKEN (required), optionally CHAT_ID to filter.
"""
import os
import time
import requests
import json
import argparse
from gaia import events, db, task_manager, alerts
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def now():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def run(poll=3):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_filter = os.environ.get('CHAT_ID')
    if not token:
        print('ERROR: TELEGRAM_BOT_TOKEN required')
        return 2
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    offset = None
    print('Starting telegram bridge, poll', poll)
    while True:
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
                user = msg.get('from', {})
                username = user.get('username') or user.get('first_name')
                print('Message from', from_id, 'text=', text)
                if chat_filter and str(from_id) != str(chat_filter):
                    print('Ignored message from', from_id)
                    continue
                # Create a task
                task_id = task_manager.create_task(source='telegram', user_id=from_id, message=text, meta=msg)
                events.make_event('task.created', {'source': 'telegram', 'task_id': task_id, 'user': str(from_id), 'message': text})
                db.write_trace(action='task.created', status='ok', details={'task_id': task_id, 'user': from_id, 'text': text})
                # Acknowledge
                ack = f'Received. Created task #{task_id}. I will evaluate and act ASAP.'
                try:
                    alerts.send_telegram(chat_id=from_id, message=ack, token=token)
                except Exception as e:
                    print('Ack failed', e)
            time.sleep(poll)
        except Exception as e:
            print('bridge poll error', e)
            time.sleep(poll)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--poll', type=int, default=3)
    args = p.parse_args()
    run(poll=args.poll)
