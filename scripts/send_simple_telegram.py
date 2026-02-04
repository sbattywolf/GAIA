#!/usr/bin/env python3
"""Send a simple Telegram message using `.tmp/telegram.env`.

Usage: python scripts/send_simple_telegram.py "message text"
"""
from __future__ import annotations
import sys
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def send(token: str, chat: str, text: str) -> bool:
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': chat, 'text': text})
        r.raise_for_status()
        return True
    except Exception as e:
        print('send failed:', e)
        return False


def main():
    if len(sys.argv) < 2:
        print('Usage: send_simple_telegram.py "message text"')
        sys.exit(1)
    msg = sys.argv[1]
    from scripts.env_utils import load_preferred_env
    env = load_preferred_env(ROOT)
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    if not token or not chat:
        print('telegram env missing')
        sys.exit(1)
    ok = send(token, chat, msg)
    print('sent=', ok)


if __name__ == '__main__':
    main()
