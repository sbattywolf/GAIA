#!/usr/bin/env python3
"""Import a single secret (from stdin) into the encrypted store and validate it.

Usage:
  echo "<value>" | python scripts/import_and_validate_key.py KEY_NAME

The script sets the key in the `SecretsManager` and performs a lightweight
API check if the key looks like a Telegram or GitHub token.
"""
import sys
from pathlib import Path
import json

# ensure repo root on path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from gaia.secrets import SecretsManager
except Exception as e:
    print('Failed to import SecretsManager:', e, file=sys.stderr)
    sys.exit(2)

import requests


def check_telegram(token: str) -> dict:
    url = f'https://api.telegram.org/bot{token}/getMe'
    try:
        r = requests.get(url, timeout=5)
        return {'ok': r.status_code == 200, 'status_code': r.status_code, 'text': r.text}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def check_github(token: str) -> dict:
    url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return {'ok': r.status_code == 200, 'status_code': r.status_code, 'text': r.text}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def main():
    if len(sys.argv) < 2:
        print('Usage: echo "value" | python scripts/import_and_validate_key.py KEY_NAME', file=sys.stderr)
        sys.exit(2)

    key = sys.argv[1]
    val = sys.stdin.read().strip()
    if not val:
        print('No value provided on stdin', file=sys.stderr)
        sys.exit(2)

    sm = SecretsManager()
    ok = sm.set(key, val)
    if not ok:
        print('Failed to set key in SecretsManager', file=sys.stderr)
        sys.exit(2)

    result = {'key': key, 'set': True}

    if 'TELEGRAM' in key.upper():
        print('Running Telegram check...')
        result['check'] = check_telegram(val)
    elif 'GITHUB' in key.upper() or key.upper() in ('GITHUB_TOKEN', 'GH_TOKEN', 'AUTOMATION_GITHUB_TOKEN'):
        print('Running GitHub check...')
        result['check'] = check_github(val)
    else:
        print('No validation rule for this key; stored only.')

    print(json.dumps(result, indent=2))
    if result.get('check') and not result['check'].get('ok'):
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
