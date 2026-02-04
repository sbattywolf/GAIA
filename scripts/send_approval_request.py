#!/usr/bin/env python3
"""Send an approval request message to the configured Telegram chat.
Asks which actions the autonomous agent is allowed to perform without prompting.
"""
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
from scripts.env_utils import preferred_env_path
env_path = preferred_env_path(ROOT)

def load_env(p: Path):
    env = {}
    if not p.exists():
        return env
    for line in p.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k,v = line.split('=',1)
            env[k.strip()] = v.strip()
    return env

env = load_env(env_path)
token = env.get('TELEGRAM_BOT_TOKEN')
chat = env.get('CHAT_ID')

msg = (
    'Autonomous agent approval request:\n'
    'Please reply with the numbers (comma-separated) you approve:\n'
    '1) Allow creating GitHub PRs (`gh pr create`)\n'
    '2) Allow creating/updating remote issues (GitHub/GH)\n'
    '3) Allow rotating admin tokens / running token-rotation scripts\n'
    '4) Allow executing shell commands on this host (risky)\n'
    '5) Allow sending messages to external services (webhooks)\n'
    '6) Allow modifying `.tmp/telegram.env` or secret files\n'
    '\nDefault: none approved. Reply here with approvals to grant.'
)

if token and chat:
    try:
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={'chat_id': chat, 'text': msg})
        r.raise_for_status()
        print('sent')
    except Exception as e:
        print('send-failed', e)
else:
    print('telegram config missing')
from pathlib import Path
from scripts import telegram_client as tc
import datetime

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / '.tmp' / 'telegram.env'

def load_env():
    env = {}
    if not ENV.exists():
        return env
    for l in ENV.read_text(encoding='utf-8').splitlines():
        if '=' in l and not l.strip().startswith('#'):
            k,v = l.split('=',1)
            env[k.strip()] = v.strip()
    return env

def main():
    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    if not token or not chat:
        print('missing token/chat in .tmp/telegram.env')
        return 2
    note = f"GAIA: I will request approval before running any scripts. Reply APPROVE in this chat to allow actions. (Sent at {datetime.datetime.utcnow().strftime('%a %b %d %Y %H:%M:%S UTC')})"
    print('sending approval request...')
    res = tc.send_message(token, chat, note)
    print(res)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
