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
