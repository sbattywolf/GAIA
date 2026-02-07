import os
import sys
import requests


def main():
    if len(sys.argv) < 2:
        print('Usage: send_telegram_message.py <message>', file=sys.stderr)
        sys.exit(2)
    msg = sys.argv[1]
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat = os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat:
        print('Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in secrets', file=sys.stderr)
        sys.exit(1)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    r = requests.post(url, json={'chat_id': chat, 'text': msg})
    r.raise_for_status()
    print('Sent OK', r.json())


if __name__ == '__main__':
    main()
