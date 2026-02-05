#!/usr/bin/env python3
"""Dry-run Telegram realtime notifier + optional send.

Usage:
  python scripts/telegram_realtime.py [--send] [--interval SECONDS]

By default this prints formatted messages instead of sending. Use `--send` to post
to Telegram (requires `.private/.env` with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID).
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_private_env():
    env_path = ROOT / '.private' / '.env'
    if env_path.exists():
        try:
            # lightweight loader: parse KEY=VAL lines
            with open(env_path, 'r', encoding='utf-8') as f:
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


def send_telegram_message(token, chat_id, text):
    try:
        import requests
    except Exception:
        raise RuntimeError('requests library required to send Telegram messages')

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


def tail_events_and_report(interval, do_send):
    events_file = ROOT / 'events.ndjson'
    source = 'realtime-notifier'

    # simple snapshot: count events in last interval and pending approvals from .tmp
    while True:
        now = time.time()
        # count last N lines of events file (best-effort)
        events_count = 0
        try:
            with open(events_file, 'rb') as f:
                f.seek(0, 2)
                size = f.tell()
                # read last 16KB
                read_size = min(size, 16 * 1024)
                f.seek(size - read_size)
                data = f.read().decode('utf-8', errors='ignore')
                lines = [l for l in data.splitlines() if l.strip()]
                events_count = len(lines)
        except Exception:
            events_count = 0

        # queued approvals
        pending = 0
        try:
            tmp = ROOT / '.tmp'
            for p in tmp.glob('approval_required_*.json'):
                pending += 1
        except Exception:
            pending = 0

        metrics = {'EventsTail': events_count, 'ApprovalsPending': pending}
        summary = f'periodic snapshot — events_tail={events_count}, approvals_pending={pending}'
        msg = fmt_message(source, 'running', summary, metrics=metrics)

        if do_send:
            token = os.environ.get('TELEGRAM_BOT_TOKEN')
            chat = os.environ.get('TELEGRAM_CHAT_ID')
            if not token or not chat:
                print('TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing; not sending')
            else:
                try:
                    send_telegram_message(token, chat, msg)
                    print('Sent Telegram snapshot')
                except Exception as e:
                    print('Failed to send Telegram message:', e)
        else:
            print('--- Telegram (dry-run) ---')
            print(msg)
            print('--- end ---')

        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--send', action='store_true', help='Actually send messages to Telegram')
    parser.add_argument('--interval', type=int, default=int(os.environ.get('PERIODIC_INTERVAL_SEC', '300')),
                        help='Snapshot interval in seconds')
    args = parser.parse_args()

    load_private_env()

    try:
        tail_events_and_report(args.interval, args.send)
    except KeyboardInterrupt:
        print('Exiting')


if __name__ == '__main__':
    main()
