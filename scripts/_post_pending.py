from pathlib import Path
import json, os, sys
ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / '.tmp' / 'pending_commands.json'
ENV = ROOT / '.tmp' / 'telegram.env'

TARGET_ID = 'fa1cde9e-1234-4bcd-8f1a-0fa1cde00001'


def load_env(path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        if '=' not in line: continue
        k,v=line.split('=',1)
        env[k.strip()] = v.strip()
    return env


def main():
    if not PENDING.exists():
        print('pending file not found', file=sys.stderr)
        return 2
    items = json.loads(PENDING.read_text(encoding='utf-8'))
    target = None
    for it in items:
        if it.get('id') == TARGET_ID:
            target = it
            break
    if not target:
        print('target id not found in pending', file=sys.stderr)
        return 3
    env = load_env(ENV)
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID') or target.get('chat_id')
    if not token or not chat:
        print('telegram token or chat missing', file=sys.stderr)
        return 4
    # build message
    is_test = False
    try:
        opts = target.get('options') or {}
        is_test = bool(opts.get('is_test'))
    except Exception:
        is_test = False
    warn_prefix = '⚠️ TEST COMMAND — DO NOT PRESS PROCEED\n\n' if is_test else ''
    text = warn_prefix + f"Approval requested:\n{(target.get('command') or '')}\n\nid: {target.get('id')}\ncreated: {target.get('created')}"
    # build buttons
    if is_test:
        buttons = [
            [ { 'text': '🧪 Approve (test)', 'callback_data': f"approve:{target['id']}" }, { 'text': 'Deny', 'callback_data': f"deny:{target['id']}" } ],
            [ { 'text': 'Info', 'callback_data': f"info:{target['id']}" } ],
            [ { 'text': '🔴 Proceed (disabled - TEST)', 'callback_data': f"proceed_disabled:{target['id']}" } ]
        ]
    else:
        buttons = [
            [ { 'text': 'Approve', 'callback_data': f"approve:{target['id']}" }, { 'text': 'Deny', 'callback_data': f"deny:{target['id']}" } ],
            [ { 'text': 'Info', 'callback_data': f"info:{target['id']}" } ],
            [ { 'text': 'Proceed (disabled)', 'callback_data': f"proceed_disabled:{target['id']}" } ]
        ]
    reply_markup = { 'inline_keyboard': buttons }
    try:
        from scripts.telegram_client import send_message
        resp = send_message(token, chat, text, reply_markup=reply_markup)
        print('ok', json.dumps(resp, indent=2))
        return 0
    except Exception as e:
        print('send failed:', str(e), file=sys.stderr)
        return 5

if __name__ == '__main__':
    sys.exit(main())
