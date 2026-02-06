#!/usr/bin/env python3
"""Export selected keys from the encrypted store to a plaintext external env file.

Defaults to keys listed in `STARTUP_REQUIRED_TOKENS` or the `--keys` arg.
Writes to `E:/Workspaces/Git/.secret.env` by default.

Use with care: this writes plaintext tokens to disk.
"""
import argparse
import os
from pathlib import Path
from gaia.secrets import SecretsManager

DEFAULT_TARGET = Path('E:/Workspaces/Git/.secret.env')


def parse_keys(arg: str):
    return [k.strip() for k in arg.split(',') if k.strip()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--keys', help='Comma-separated keys to export')
    p.add_argument('--target', help='Target file path', default=str(DEFAULT_TARGET))
    p.add_argument('--force', action='store_true', help='Overwrite existing target')
    args = p.parse_args()

    keys = []
    if args.keys:
        keys = parse_keys(args.keys)
    else:
        env_keys = os.environ.get('STARTUP_REQUIRED_TOKENS')
        if env_keys:
            keys = parse_keys(env_keys)
        else:
            keys = ['TELEGRAM_BOT_TOKEN', 'AUTOMATION_GITHUB_TOKEN']

    target = Path(args.target)
    if target.exists() and not args.force:
        print(f'Target {target} exists; use --force to overwrite')
        return 2

    sm = SecretsManager()
    out_lines = []
    for k in keys:
        v = sm.get(k)
        if v is None:
            print(f'Warning: key {k} not found in encrypted store; skipping')
            continue
        out_lines.append(f'{k}={v}')

    if not out_lines:
        print('No keys exported')
        return 1

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
    print(f'Exported {len(out_lines)} keys to {target}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
