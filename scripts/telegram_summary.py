#!/usr/bin/env python3
"""Send a short Telegram summary of EPC_Telegram.current counts.

Uses `gaia.alerts.send_telegram` to send a message describing features/stories/tasks (done/pending).
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
EPIC = ROOT / 'doc' / 'EPC_Telegram.current'

def parse_epic(epic_file: Path):
    try:
        data = json.loads(epic_file.read_text(encoding='utf-8'))
    except Exception:
        return None
    stats = {'features': 0, 'stories': 0, 'tasks_total': 0, 'tasks_done': 0, 'tasks_todo': 0}
    features = data.get('features', [])
    stats['features'] = len(features)
    for f in features:
        for s in f.get('stories', []):
            stats['stories'] += 1
            for t in s.get('tasks', []):
                stats['tasks_total'] += 1
                if t.get('status') in ('done', 'completed'):
                    stats['tasks_done'] += 1
                else:
                    stats['tasks_todo'] += 1
    return stats

def build_message(stats):
    if not stats:
        return 'Failed to load epic summary.'
    return (f"GAIA Telegram summary:\nFeatures: {stats['features']}\nStories: {stats['stories']}\n"
            f"Tasks done: {stats['tasks_done']} / {stats['tasks_total']}\nPending: {stats['tasks_todo']}")

def load_env(path: Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k,v = line.split('=',1)
            env[k.strip()] = v.strip()
    return env

def main():
    from scripts.env_utils import load_preferred_env
    env = load_preferred_env(ROOT)
    token = env.get('TELEGRAM_BOT_TOKEN') or ''
    chat = env.get('CHAT_ID') or ''
    stats = parse_epic(EPIC)
    msg = build_message(stats)
    if not token or not chat:
        print('Missing token or chat_id in .tmp/telegram.env; summary:')
        print(msg)
        sys.exit(1)
    # import here to avoid heavy deps on module import path
    try:
        from gaia.alerts import send_telegram
        resp = send_telegram(chat_id=chat, message=msg, token=token)
        print('Sent:', resp)
    except Exception as e:
        print('Failed to send via gaia.alerts:', e)

if __name__ == '__main__':
    main()
