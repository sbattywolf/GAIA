"""Alert utilities.

Provides real Telegram send (uses env vars or passed token/chat_id) and the previous
stub behavior for WhatsApp. All attempts append events and write traces to `gaia.db`.
"""
from . import events, db
import os
import requests


def send_telegram(chat_id=None, message=None, token=None):
    """Send a Telegram message via Bot API.

    token and chat_id may be provided or read from env vars `TELEGRAM_BOT_TOKEN` and `CHAT_ID`.
    Returns dict with API response or error info.
    """
    token = token or os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = chat_id or os.environ.get('CHAT_ID')
    payload = {'channel': 'telegram', 'chat_id': chat_id, 'message': message}
    events.make_event('alert.requested', payload)
    try:
        if not token or not chat_id:
            raise ValueError('token or chat_id not provided')
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        r = requests.post(url, json={'chat_id': chat_id, 'text': message}, timeout=10)
        try:
            resp = r.json()
        except Exception:
            resp = {'status_code': r.status_code, 'text': r.text}
        status = 'sent' if resp.get('ok') else 'failed'
        db.write_trace(action='alert.telegram.sent', status=status, details={'chat_id': chat_id, 'resp': resp})
        events.make_event('alert.sent', {'channel': 'telegram', 'chat_id': chat_id, 'resp': resp})
        return resp
    except Exception as e:
        db.write_trace(action='alert.telegram.error', status='error', details={'error': str(e), 'chat_id': chat_id})
        events.make_event('alert.error', {'channel': 'telegram', 'chat_id': chat_id, 'error': str(e)})
        return {'ok': False, 'error': str(e)}


def send_whatsapp_stub(phone=None, message=None):
    payload = {'channel': 'whatsapp', 'phone': phone, 'message': message}
    evt = events.make_event('alert.requested', payload)
    try:
        db.write_trace(action='alert.whatsapp.requested', status='queued', details=payload)
    except Exception:
        pass
    return evt
