#!/usr/bin/env python3
"""Scaffold: validate a Telegram bot token and write an audit trace.

This is a scaffold: validation is a simple call to getMe; when successful it
writes an event to `events.ndjson` and a gaia.db trace (if db available).
"""
from pathlib import Path
import requests
import json
import sys
ROOT = Path(__file__).resolve().parent.parent

def validate_token(token: str) -> dict:
    url = f'https://api.telegram.org/bot{token}/getMe'
    try:
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {'ok': False, 'error': str(e)}

def append_event(evt: dict):
    fn = ROOT / 'events.ndjson'
    try:
        with open(fn, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt) + "\n")
    except Exception:
        pass

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--token', required=True)
    p.add_argument('--target-file', default=str(ROOT / '.tmp' / 'telegram.env'))
    args = p.parse_args()
    resp = validate_token(args.token)
    if not resp.get('ok'):
        print('Validation failed:', resp)
        evt = {'type': 'token.rotate.attempt', 'payload': {'token_ok': False, 'resp': resp}}
        append_event(evt)
        sys.exit(2)
    # token valid — write to target file (careful: this is a scaffold; consider secure storage)
    tf = Path(args.target_file)
    tf.parent.mkdir(parents=True, exist_ok=True)
    content = f"TELEGRAM_BOT_TOKEN={args.token}\n"
    try:
        with open(tf, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Wrote token to', tf)
        evt = {'type': 'token.rotate.success', 'payload': {'resp': resp}}
        append_event(evt)
    except Exception as e:
        print('Failed to write token:', e)
        evt = {'type': 'token.rotate.error', 'payload': {'error': str(e)}}
        append_event(evt)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""Scaffold: rotate_admin_token

Safe scaffold to rotate an admin token. It supports `--dry-run` to preview actions.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--token-file', default=str(ROOT / '.tmp' / 'telegram.env'))
    args = p.parse_args()

    print('rotate_admin_token: dry_run=', args.dry_run)
    tf = Path(args.token_file)
    if not tf.exists():
        print('token file not found:', tf)
        sys.exit(1)

    # This scaffold does not perform real rotation; it demonstrates safe steps.
    content = tf.read_text(encoding='utf-8')
    print('Found token file, length:', len(content))
    if args.dry_run:
        print('Would call secrets store or API to rotate token and update .tmp/telegram.env')
        return

    # In live mode we would call the secrets provider and update the file atomically.
    print('Rotation requested but scaffold will not change tokens. Implement secrets provider integration.')


if __name__ == '__main__':
    main()
