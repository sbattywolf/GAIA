#!/usr/bin/env python3
"""Check presence of required secrets for CI or local runs.

Usage:
  python scripts/check_secrets_ci.py

Exits 0 when required secrets are available either in the environment or
via an external env file (`PRIVATE_ENV_PATH`) or repository external file
like E:\\Workspaces\\Git\\.secret\\.env. Exits 2 with a helpful message
if secrets are missing.
"""
from pathlib import Path
import os
import sys


REQUIRED = [
    # core runtime
    'TELEGRAM_BOT_TOKEN',
    'TELEGRAM_CHAT_ID',
    # one of these for GitHub operations
]
GITHUB_ALTERNATIVES = ['AUTOMATION_GITHUB_TOKEN', 'AUTOMATION_GITHUB_TOKEN_PAI', 'GITHUB_TOKEN', 'GH_TOKEN']


def load_env_file(path: Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def main():
    # gather from os.environ first
    found = {k: os.environ.get(k) for k in REQUIRED}
    github_found = any(os.environ.get(k) for k in GITHUB_ALTERNATIVES)

    # try external env path if missing
    ext = os.environ.get('PRIVATE_ENV_PATH')
    candidates = []
    if ext:
        candidates.append(Path(ext))
    # common external location (mirrors sanitize helper)
    candidates.append(Path('E:/Workspaces/Git/.secret/.env'))
    candidates.append(Path('.private/.env'))

    for c in candidates:
        if not c.exists():
            continue
        env = load_env_file(c)
        for k in REQUIRED:
            if not found.get(k) and env.get(k):
                found[k] = env.get(k)
        if not github_found and any(env.get(k) for k in GITHUB_ALTERNATIVES):
            github_found = True

    missing = [k for k, v in found.items() if not v]
    if missing or not github_found:
        print('Missing required secrets:')
        for k in missing:
            print(' -', k)
        if not github_found:
            print(' - (one of) ' + ', '.join(GITHUB_ALTERNATIVES))
        print('\nSet them via your CI secrets or point PRIVATE_ENV_PATH to an external env file.')
        return 2

    print('Secrets check OK: required secrets available (values hidden).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
