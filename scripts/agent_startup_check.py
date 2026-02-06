#!/usr/bin/env python3
"""Agent startup token validation.

Checks a small set of required tokens on agent startup and raises audit
impediments when validations fail. Intended to be invoked by agent entrypoints
early during boot (or from service wrappers).

Behavior:
- Read required token names from `STARTUP_REQUIRED_TOKENS` env var (comma-separated),
  default: `TELEGRAM_BOT_TOKEN,AUTOMATION_GITHUB_TOKEN`.
- For each key, attempt lightweight validation (Telegram `getMe`, GitHub `/user`).
- Write an audit row via `orchestrator.write_audit()` and a local status file
  `.private/startup_check.json` summarizing results.

Exit codes:
- 0: all required tokens validated
- 1: one or more tokens failed validation (impediment logged)
- 2: unexpected error (missing modules, etc.)
"""
import os
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT / '.private'
PRIV.mkdir(parents=True, exist_ok=True)
STATUS_FILE = PRIV / 'startup_check.json'

try:
    from gaia.secrets import SecretsManager
    import orchestrator
except Exception as e:
    print('Startup check import error:', e, file=sys.stderr)
    sys.exit(2)

import requests


def now_iso():
    return datetime.now(timezone.utc).isoformat() + 'Z'


def check_telegram(token: str):
    url = f'https://api.telegram.org/bot{token}/getMe'
    try:
        r = requests.get(url, timeout=5)
        return {'ok': r.status_code == 200, 'status_code': r.status_code, 'text': r.text}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def check_github(token: str):
    url = 'https://api.github.com/user'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        return {'ok': r.status_code == 200, 'status_code': r.status_code, 'text': r.text}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def main():
    required = os.environ.get('STARTUP_REQUIRED_TOKENS', 'TELEGRAM_BOT_TOKEN,AUTOMATION_GITHUB_TOKEN')
    keys = [k.strip() for k in required.split(',') if k.strip()]
    sm = SecretsManager()
    results = {'timestamp': now_iso(), 'results': {}}
    impediments = []

    for k in keys:
        v = sm.get(k)
        if not v:
            msg = f'missing {k}'
            results['results'][k] = {'ok': False, 'error': msg}
            orchestrator.write_audit('agent_startup', 'impediment', json.dumps({'key': k, 'error': msg}))
            impediments.append({'key': k, 'error': msg})
            continue

        # select validator
        if 'TELEGRAM' in k.upper():
            res = check_telegram(v)
        elif 'GITHUB' in k.upper():
            res = check_github(v)
        else:
            res = {'ok': True, 'note': 'no validation rule; present'}

        results['results'][k] = res
        if not res.get('ok'):
            orchestrator.write_audit('agent_startup', 'impediment', json.dumps({'key': k, 'result': res}))
            impediments.append({'key': k, 'result': res})
        else:
            orchestrator.write_audit('agent_startup', 'validate', json.dumps({'key': k, 'result': {'ok': True}}))

    # write status
    try:
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    if impediments:
        print('Startup impediments detected:', json.dumps(impediments, indent=2))
        sys.exit(1)
    print('Startup token validation: all required tokens OK')
    sys.exit(0)


if __name__ == '__main__':
    main()
