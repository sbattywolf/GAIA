#!/usr/bin/env python3
"""Small helper to perform micro-commits when allowed by env flags.

Usage: python scripts/micro_commit.py --message "msg"

Safest behavior: only runs when `AUTOCOMMIT_ENABLED=1` and `ALLOW_COMMAND_EXECUTION=1`.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys


def allowed() -> bool:
    return os.environ.get('AUTOCOMMIT_ENABLED') == '1' and os.environ.get('ALLOW_COMMAND_EXECUTION') == '1'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--message', required=True)
    args = p.parse_args()

    if not allowed():
        print('Micro-commit disabled by environment')
        return 0

    # create or checkout feature branch
    branch = 'feat/copilot-autowork'
    try:
        subprocess.run(['git', 'checkout', branch], check=False)
        subprocess.run(['git', 'add', '-A'], check=True)
        subprocess.run(['git', 'commit', '-m', args.message], check=True)
        print('Micro-commit created on', branch)
        return 0
    except subprocess.CalledProcessError as e:
        print('Micro-commit failed:', e)
        return 2


if __name__ == '__main__':
    sys.exit(main())
