#!/usr/bin/env python3
"""Persist `GAIA_GITHUB_TOKEN` encrypted with `GAIA_FERNET_KEY`.

Writes a small encrypted file containing the token so operator steps can
persist and audit rotation without keeping plaintext in the repo.

Usage:
  GAIA_GITHUB_TOKEN=... GAIA_FERNET_KEY=... python scripts/persist_token.py

If `GAIA_FERNET_KEY` is not set the script will exit with a helpful message.
"""
import os
import sys
from pathlib import Path


def load_env_file_if_present():
    try:
        from scripts import env_loader
    except Exception:
        env_loader = None
    env_path = Path(__file__).resolve().parent.parent / '.private' / '.env'
    if env_path.exists() and env_loader:
        try:
            env_loader.load_env(str(env_path))
        except Exception:
            pass


def main():
    load_env_file_if_present()

    token = os.environ.get('GAIA_GITHUB_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        print('No GAIA_GITHUB_TOKEN or GITHUB_TOKEN found in environment. Aborting.', file=sys.stderr)
        return 2

    key = os.environ.get('GAIA_FERNET_KEY')
    if not key:
        print('\nGAIA_FERNET_KEY is not set. To persist the token you must provide a Fernet key.', file=sys.stderr)
        print('Generate one with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"', file=sys.stderr)
        return 3

    try:
        from cryptography.fernet import Fernet
    except Exception:
        print('cryptography is required: pip install cryptography', file=sys.stderr)
        return 4

    f = Fernet(key.encode() if isinstance(key, str) else key)
    token_bytes = token.encode()
    token_enc = f.encrypt(token_bytes)

    out_dir = Path(__file__).resolve().parent.parent / '.private'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'gaia_github_token.enc'
    out_file.write_bytes(token_enc)

    print('Encrypted token written to', out_file)
    return 0


if __name__ == '__main__':
    sys.exit(main())
