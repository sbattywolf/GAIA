#!/usr/bin/env python3
"""Generate GitHub App installation tokens and store them via SecretsManager.

Requires: PyJWT and requests. Install in venv:
  pip install PyJWT requests

Usage:
  python scripts/github_app_token.py --app-id 12345 --key-path .private/app.pem --installation-id 67890

This script creates a JWT for the GitHub App and exchanges it for an
installation access token (short-lived). It can then persist the token in
the encrypted store using `SecretsManager` or write it to stdout.
"""
from __future__ import annotations
import argparse
import time
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))



def create_jwt(app_id: str, key_path: Path) -> str:
    now = int(time.time())
    payload = {
        'iat': now - 60,
        'exp': now + (9 * 60),  # 9 minutes expiry (max 10)
        'iss': app_id,
    }
    key = key_path.read_bytes()
    try:
        import jwt  # PyJWT
    except Exception:
        print('Missing dependency: PyJWT. Install with: pip install PyJWT')
        raise
    token = jwt.encode(payload, key, algorithm='RS256')
    return token


def get_installation_token(app_jwt: str, installation_id: str) -> str:
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    headers = {
        'Authorization': f'Bearer {app_jwt}',
        'Accept': 'application/vnd.github+json'
    }
    r = requests.post(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    # return token and expiry to callers
    return data.get('token'), data.get('expires_at')


def persist_token(token: str, name: str = 'GAIA_GITHUB_TOKEN') -> bool:
    try:
        from gaia.secrets import SecretsManager
        sm = SecretsManager()
        return sm.set(name, token, provider='encrypted_file')
    except Exception:
        # SecretsManager (and its deps like cryptography) may be unavailable in this environment
        print('SecretsManager unavailable; cannot persist token here')
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--app-id', required=True, help='GitHub App ID')
    parser.add_argument('--key-path', required=True, help='Path to GitHub App private key (PEM)')
    parser.add_argument('--installation-id', required=True, help='Installation ID to exchange for token')
    parser.add_argument('--persist', action='store_true', help='Persist token to encrypted store')
    parser.add_argument('--name', default='GAIA_GITHUB_TOKEN', help='Secret name to persist')
    args = parser.parse_args()

    # Test mode: return the GAIA_GITHUB_TOKEN from SecretsManager or environment if requested
    import os
    if os.environ.get('GAIA_TEST_MODE'):
        tok = None
        try:
            from gaia.secrets import SecretsManager
            sm = SecretsManager()
            tok = sm.get('GAIA_GITHUB_TOKEN') or sm.get('AUTOMATION_GITHUB_TOKEN')
        except Exception:
            tok = os.environ.get('GAIA_GITHUB_TOKEN') or os.environ.get('AUTOMATION_GITHUB_TOKEN')

        if not tok:
            print('')
            return 4
        # print JSON for programmatic consumption
        import json
        print(json.dumps({'token': tok, 'expires_at': None}))
        return 0

    key_path = Path(args.key_path)
    if not key_path.exists():
        print('Key file not found:', key_path)
        return 2

    jwt_token = create_jwt(args.app_id, key_path)

    try:
        token, expires_at = get_installation_token(jwt_token, args.installation_id)
    except Exception as e:
        print('Failed to obtain installation token:', e)
        return 3

    if args.persist:
        ok = persist_token(token, name=args.name)
        print('Persisted token to encrypted store.' if ok else 'Failed to persist token.')
        if expires_at:
            print('expires_at:', expires_at)
    else:
        # Print JSON with token and expiry for programmatic consumption
        out = {'token': token}
        if expires_at:
            out['expires_at'] = expires_at
        import json
        print(json.dumps(out))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
