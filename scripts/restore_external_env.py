#!/usr/bin/env python3
"""Restore the most recent external env backup back to the external path.

This helper looks for files matching `.secret.env.bak.*` in the repo root and
restores the newest one to `E:/Workspaces/Git/.secret.env`. It does not
overwrite an existing target unless `--force` is provided.
"""
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
BACKUP_GLOB = ROOT / '.secret.env.bak.*'
TARGET = Path('E:/Workspaces/Git/.secret.env')


def find_latest_backup():
    files = sorted(ROOT.glob('.secret.env.bak.*'))
    return files[-1] if files else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--force', action='store_true', help='Overwrite target if exists')
    args = p.parse_args()

    latest = find_latest_backup()
    if not latest:
        print('No backup files found matching .secret.env.bak.*')
        sys.exit(2)

    if TARGET.exists() and not args.force:
        print(f'Target {TARGET} already exists; use --force to overwrite')
        sys.exit(1)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(latest, TARGET)
    print(f'Restored {latest} -> {TARGET}')


if __name__ == '__main__':
    main()
