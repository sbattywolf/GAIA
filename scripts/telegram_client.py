"""Lightweight Telegram Bot API client helpers with retries and long-poll support.

Provides `get_updates()` and `send_message()` helpers used by listeners.
Designed to be small, dependency-free (requests used), and robust with retries.
"""
import time
import requests
import json
import os


def _with_retries(fn, attempts=None, backoff=None):
    """Run `fn()` with retries and exponential backoff.

    If `attempts` or `backoff` are None the values are read from
    environment variables: `TELEGRAM_RETRIES` (int) and
    `TELEGRAM_BACKOFF_MS` (milliseconds, int). Defaults: 3 attempts,
    500ms backoff.
    """
    # env-configurable defaults
    try:
        if attempts is None:
            attempts = int(os.environ.get('TELEGRAM_RETRIES', '3'))
    except Exception:
        attempts = 3
    try:
        if backoff is None:
            ms = int(os.environ.get('TELEGRAM_BACKOFF_MS', '500'))
            backoff = max(0.01, ms / 1000.0)
    except Exception:
        backoff = 0.5

    last = None
    for n in range(1, max(1, int(attempts)) + 1):
        try:
            return fn()
        except Exception as e:
            last = e
            # exponential factor
            try:
                time.sleep(backoff * (2 ** (n - 1)))
            except Exception:
                pass
    raise last


def send_message(token: str, chat_id, text: str, parse_mode=None, timeout=6, reply_to_message_id=None, reply_markup=None):
    """Send a text message. Raises on failure.

    Returns the parsed JSON response on success.
    """
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    def call():
        payload = {'chat_id': chat_id, 'text': text}
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = int(reply_to_message_id)
        if reply_markup is not None:
            # reply_markup should be JSON-serializable (dict or list)
            payload['reply_markup'] = reply_markup
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()

    return _with_retries(call)


def get_updates(token: str, offset=None, timeout=60):
    """Call getUpdates with optional offset and timeout (long-poll).

    Returns a dict containing the parsed JSON from Telegram.
    """
    url = f'https://api.telegram.org/bot{token}/getUpdates'

    def call():
        params = {'timeout': int(timeout)}
        if offset is not None:
            params['offset'] = int(offset)
        r = requests.get(url, params=params, timeout=timeout + 10)
        r.raise_for_status()
        return r.json()

    return _with_retries(call)


def safe_load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def safe_save_json(path, obj):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2)
    except Exception:
        pass


def answer_callback(token: str, callback_query_id: str, text: str = None, show_alert: bool = False, timeout=6):
    """Answer a callback_query to acknowledge a pressed inline button."""
    url = f'https://api.telegram.org/bot{token}/answerCallbackQuery'

    def call():
        payload = {'callback_query_id': callback_query_id}
        if text is not None:
            payload['text'] = text
        if show_alert:
            payload['show_alert'] = True
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()

    return _with_retries(call)


def send_chat_action(token: str, chat_id, action: str = 'typing', timeout=6):
    """Send a chat action (e.g., 'typing') to indicate the bot is working.

    Returns the parsed JSON response.
    """
    url = f'https://api.telegram.org/bot{token}/sendChatAction'

    def call():
        payload = {'chat_id': chat_id, 'action': action}
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()

    return _with_retries(call)


def edit_message_text(token: str, chat_id, message_id, text: str, parse_mode=None, reply_markup=None, timeout=6):
    """Edit a sent message's text and optionally its inline keyboard."""
    url = f'https://api.telegram.org/bot{token}/editMessageText'

    def call():
        payload = {'chat_id': chat_id, 'message_id': int(message_id), 'text': text}
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if reply_markup is not None:
            payload['reply_markup'] = reply_markup
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()

    return _with_retries(call)


# record failed outbound replies for operator inspection/retry
FAILED_PATH = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'telegram_queue_failed.json')


def record_failed_reply(obj: dict):
    try:
        os.makedirs(os.path.dirname(FAILED_PATH), exist_ok=True)
        arr = []
        try:
            with open(FAILED_PATH, 'r', encoding='utf-8') as f:
                arr = json.load(f) or []
        except Exception:
            arr = []
        arr.append(obj)
        with open(FAILED_PATH, 'w', encoding='utf-8') as f:
            json.dump(arr, f, indent=2)
    except Exception:
        pass
