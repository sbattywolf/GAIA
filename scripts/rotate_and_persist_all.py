#!/usr/bin/env python3
"""Rotate installation tokens for configured consumers and persist them.

This script reads `rotation/consumers.json` (or a provided config) which maps
consumer names to installation IDs and desired secret names. For safety the
default mode is `--dry-run` which doesn't persist tokens; pass `--confirm`
to actually write tokens into the encrypted store.

Supports GAIA_TEST_MODE for local testing (reads `GAIA_GITHUB_TOKEN` from env).
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / 'rotation' / 'consumers.json'


def load_config(path: Path) -> Dict:
    if not path.exists():
        sample = ROOT / 'rotation' / 'consumers.sample.json'
        if sample.exists():
            print('Using sample consumers config:', sample)
            return json.loads(sample.read_text(encoding='utf-8'))
        raise SystemExit(f'Config not found: {path} and no sample available')
    return json.loads(path.read_text(encoding='utf-8'))


def get_installation_token(app_id: str, key_path: str, installation_id: str) -> Dict:
    cmd = [sys.executable, 'scripts/github_app_token.py', '--app-id', str(app_id), '--key-path', str(key_path), '--installation-id', str(installation_id)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout or 'helper error')
    try:
        return json.loads(proc.stdout)
    except Exception:
        # fallback: helper may print raw token
        return {'token': proc.stdout.strip(), 'expires_at': None}


def persist_token(name: str, token: str) -> None:
    # Use rotate_tokens_helper to persist safely (it mirrors canonical names)
    cmd = [sys.executable, 'scripts/rotate_tokens_helper.py', '--name', name, '--token', token]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError('persist helper failed: ' + (proc.stderr or proc.stdout))


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--config', default=str(DEFAULT_CONFIG), help='Path to consumers JSON')
    p.add_argument('--app-id', required=False, help='App ID override (optional)')
    p.add_argument('--key-path', default='.private/gaia_app.pem', help='Path to App private key (PEM)')
    p.add_argument('--confirm', action='store_true', help='Actually persist tokens (default: dry-run)')
    args = p.parse_args(argv)

    cfg = load_config(Path(args.config))
    app_id = args.app_id or cfg.get('app_id')
    if not app_id:
        raise SystemExit('app_id must be provided either in config or via --app-id')

    key_path = Path(args.key_path)
    if not key_path.exists() and not (args.confirm is False):
        print('Warning: key file not found; in GAIA_TEST_MODE this is ok')

    consumers = cfg.get('consumers', {})
    results = {}
    for name, meta in consumers.items():
        inst_id = meta.get('installation_id')
        secret_name = meta.get('secret_name') or meta.get('name') or f'GAIA_{name.upper()}_TOKEN'
        print('Rotating for', name, 'installation=', inst_id, '->', secret_name)
        try:
            data = get_installation_token(app_id, str(key_path), inst_id)
        except Exception as e:
            print('Failed to get token for', name, ':', e)
            results[name] = {'ok': False, 'error': str(e)}
            continue

        token = data.get('token')
        expires = data.get('expires_at')
        print('  token:', ('[REDACTED]' if token else 'NONE'), 'expires_at:', expires)

        if args.confirm:
            try:
                persist_token(secret_name, token)
                print('  persisted as', secret_name)
                results[name] = {'ok': True, 'persisted_as': secret_name, 'expires_at': expires}
            except Exception as e:
                print('  persist failed:', e)
                results[name] = {'ok': False, 'error': str(e)}
        else:
            print('  dry-run: not persisted')
            results[name] = {'ok': True, 'dry': True, 'expires_at': expires}

    # Write results
    out = Path('rotation') / 'rotate_results.json'
    out.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print('Wrote', out)


if __name__ == '__main__':
    main()
