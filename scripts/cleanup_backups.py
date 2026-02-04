#!/usr/bin/env python3
"""Cleanup old backups from `.tmp/backups` older than N days.

Usage: python scripts/cleanup_backups.py --days 30 --dry-run
"""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime, timedelta
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--days', type=int, default=30)
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--backups-dir', default=str(ROOT / '.tmp' / 'backups'))
    args = p.parse_args()

    bd = Path(args.backups_dir)
    if not bd.exists():
        print('backups dir not found:', bd)
        return
    cutoff = datetime.utcnow() - timedelta(days=args.days)
    removed = 0
    for f in bd.iterdir():
        try:
            m = datetime.utcfromtimestamp(f.stat().st_mtime)
        except Exception:
            continue
        if m < cutoff:
            print('remove:', f)
            if not args.dry_run:
                try:
                    f.unlink()
                    removed += 1
                except Exception as e:
                    print('failed to remove', f, e)
    print('removed count:', removed)


if __name__ == '__main__':
    main()
