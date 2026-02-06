#!/usr/bin/env python3
"""Validate tokens stored in the secrets manager by performing lightweight API checks.

This script retrieves `TELEGRAM_BOT_TOKEN` and `AUTOMATION_GITHUB_TOKEN` (or
`GITHUB_TOKEN`) from the `SecretsManager` and attempts a simple API call for
each. Timeouts are short so failures are quick for fake tokens.
"""
import sys
from pathlib import Path
import json

# Ensure repository root is on sys.path so `gaia` package can be imported
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
    sm = SecretsManager()

    results = {}

    tg = sm.get('TELEGRAM_BOT_TOKEN')
    if tg:
        print('Testing TELEGRAM_BOT_TOKEN...')
        results['telegram'] = check_telegram(tg)
    else:
        print('TELEGRAM_BOT_TOKEN not present')

    gh = sm.get('AUTOMATION_GITHUB_TOKEN') or sm.get('GITHUB_TOKEN') or sm.get('GH_TOKEN')
    if gh:
        print('Testing GitHub token...')
        results['github'] = check_github(gh)
    else:
        print('GitHub token not present')

    print('\nValidation results (values hidden):')
    print(json.dumps(results, indent=2))

    # Return non-zero if any check failed
    for v in results.values():
        if not v.get('ok'):
            sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
