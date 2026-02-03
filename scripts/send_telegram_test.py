"""Send a Telegram message via Bot API using env var TELEGRAM_BOT_TOKEN and CHAT_ID.
Usage:
$env:TELEGRAM_BOT_TOKEN='123:ABC'; $env:CHAT_ID='-12345678'; python scripts\send_telegram_test.py --text "Hello"

This is a test helper; it does not store tokens in the repo.
"""
import os
import argparse
import requests


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--text', default='GAIA test alert')
    p.add_argument('--chat-id', help='Telegram chat id (overrides CHAT_ID env)')
    p.add_argument('--token', help='Telegram bot token (overrides TELEGRAM_BOT_TOKEN env)')
    args = p.parse_args()
    token = args.token or os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = args.chat_id or os.environ.get('CHAT_ID')
    if not token or not chat_id:
        print('ERROR: TELEGRAM_BOT_TOKEN and CHAT_ID must be provided via --token/--chat-id or environment')
        return 2
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': chat_id, 'text': args.text})
        r.raise_for_status()
        print('Telegram message sent')
        return 0
    except Exception as e:
        print('Failed to send Telegram message:', e)
        # Try to print response body if available
        try:
            print(r.text)
        except Exception:
            pass
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
