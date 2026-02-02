#!/usr/bin/env python3
"""Secret helper: try Bitwarden CLI, fallback to .env file.

Functions:
  get_secret(key) -> str|None

Usage example:
  from scripts.secret_helper import get_secret
  token = get_secret('GH_TOKEN')
"""
import os
import subprocess
import shlex


def _read_env(key, env_path=None):
    env_path = env_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_path):
        return None
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            if k.strip() == key:
                return v.strip()
    return None


def _bw_get(key):
    # Attempt to read via Bitwarden CLI: `bw get password <key>`
    try:
        # Check status
        st = subprocess.run(['bw', 'status'], capture_output=True, text=True)
        if st.returncode != 0:
            return None
        # Attempt to get password by item name/key
        proc = subprocess.run(['bw', 'get', 'password', key], capture_output=True, text=True)
        if proc.returncode == 0:
            return proc.stdout.strip()
    except FileNotFoundError:
        return None
    except Exception:
        return None
    return None


def get_secret(key):
    """Return secret value for `key`.

    Priority: Bitwarden CLI -> environment var -> .env file -> None
    """
    # 1) try environment
    val = os.environ.get(key)
    if val:
        return val

    # 2) try Bitwarden CLI
    val = _bw_get(key)
    if val:
        return val

    # 3) fallback to .env
    return _read_env(key)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('key')
    args = p.parse_args()
    v = get_secret(args.key)
    if v is None:
        print('')
        raise SystemExit(2)
    print(v)
