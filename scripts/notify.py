#!/usr/bin/env python3
"""Lightweight notification helper for realtime messages.

Provides `notify_event()` to format and optionally send Telegram messages.
This helper is intentionally dependency-light and falls back to dry-run printing.
"""
from pathlib import Path
import os
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent


def load_preferred_env():
    try:
        from scripts.env_utils import load_preferred_env as lpe
        env = lpe(ROOT)
        for k, v in env.items():
            os.environ.setdefault(k, v)
    except Exception:
        # best-effort: also try .private/.env
        p = ROOT / '.private' / '.env'
        if p.exists():
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip())
            except Exception:
                pass


def fmt_message(source, status, summary, metrics=None):
    ts = datetime.now(timezone.utc).isoformat(timespec='seconds')
    sprint = os.environ.get('PROJECT_V2_NUMBER', 'unknown')
    parts = [f"Agent: {source}", f"Time: {ts}", f"Sprint: {sprint}", f"Status: {status}"]
    if metrics:
        for k, v in metrics.items():
            parts.append(f"{k}: {v}")
    parts.append(f"Summary: {summary}")
    return "\n".join(parts)


def send_telegram(token, chat_id, text):
    try:
        import requests
    except Exception:
        raise RuntimeError('requests library required to send Telegram messages')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    r = requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=15)
    r.raise_for_status()
    return r.json()


def notify_event(source, status, summary, metrics=None, send=False):
    # load env values
    load_preferred_env()
    msg = fmt_message(source, status, summary, metrics=metrics)
    # simple throttling: avoid sending identical messages too frequently
    if not should_send_now(status):
        # throttled: still print for local visibility
        print('notify_event: throttled (dry-run):')
        print(msg)
        return False

    if send:
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat = os.environ.get('TELEGRAM_CHAT_ID')
        if not token or not chat:
            print('notify_event: missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID; dry-run')
            print(msg)
            return False
        try:
            send_telegram(token, chat, msg)
            record_send(status)
            return True
        except Exception as e:
            print('notify_event: send failed:', e)
            print(msg)
            return False
    else:
        print('notify_event (dry-run):')
        print(msg)
        record_send(status)
        return True


def _sent_file():
    p = ROOT / '.tmp'
    p.mkdir(exist_ok=True)
    return p / 'notify_sent.json'


def record_send(key):
    f = _sent_file()
    now_ts = int(datetime.now(timezone.utc).timestamp())
    try:
        if f.exists():
            d = json.loads(f.read_text(encoding='utf-8'))
        else:
            d = {}
    except Exception:
        d = {}
    d[key] = now_ts
    try:
        f.write_text(json.dumps(d), encoding='utf-8')
    except Exception:
        pass


def should_send_now(key, min_interval=10):
    """Return True if message with `key` can be sent now (throttling by seconds)."""
    f = _sent_file()
    now_ts = int(datetime.now(timezone.utc).timestamp())
    try:
        if f.exists():
            d = json.loads(f.read_text(encoding='utf-8'))
            last = int(d.get(key, 0))
            if now_ts - last < int(min_interval):
                return False
        return True
    except Exception:
        return True
