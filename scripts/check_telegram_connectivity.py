"""Check Telegram bot connectivity and write .tmp/telegram_connectivity.json

Performs:
- getMe
- getChat (if CHAT_ID configured)
- a lightweight getUpdates poll to verify bot can read messages
- optionally send a small test message to the chat
"""
import os
import json
from pathlib import Path
import requests
from scripts import telegram_client as tc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.tmp' / 'telegram_connectivity.json'
from scripts.env_utils import preferred_env_path
ENV_FILE = preferred_env_path(ROOT)

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

def call_api(token, method, params=None, timeout=10):
    url = f'https://api.telegram.org/bot{token}/{method}'
    r = requests.get(url, params=(params or {}), timeout=timeout)
    r.raise_for_status()
    return r.json()

def main():
    env = load_env()
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    out = {'ok': False, 'checks': {}, 'chat': chat}
    if not token:
        out['checks']['error'] = 'TELEGRAM_BOT_TOKEN missing in .tmp/telegram.env'
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(out, indent=2), encoding='utf-8')
        print('Missing token; wrote', OUT)
        return 2

    try:
        me = call_api(token, 'getMe')
        out['checks']['getMe'] = me
    except Exception as e:
        out['checks']['getMe_error'] = str(e)

    # check send capability
    try:
        resp = tc.send_message(token, chat, 'GAIA Monitor connectivity check — this is a test message.')
        out['checks']['send'] = resp
    except Exception as e:
        out['checks']['send_error'] = str(e)

    # check getChat if chat configured
    if chat:
        try:
            chat_info = call_api(token, 'getChat', params={'chat_id': chat})
            out['checks']['getChat'] = chat_info
        except Exception as e:
            out['checks']['getChat_error'] = str(e)

    # lightweight getUpdates to verify bot can read
    try:
        updates = tc.get_updates(token, timeout=2)
        out['checks']['getUpdates'] = {'ok': updates.get('ok'), 'result_count': len(updates.get('result', []))}
    except Exception as e:
        out['checks']['getUpdates_error'] = str(e)

    out['ok'] = True
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print('Wrote', OUT)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
