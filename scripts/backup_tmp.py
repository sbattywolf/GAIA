#!/usr/bin/env python3
"""Create a timestamped archive of the `.tmp` directory for backups.

Usage:
  python scripts/backup_tmp.py --out-dir .tmp/backups --dry-run
"""
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--out-dir', default=str(ROOT / '.tmp' / 'backups'))
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    src = ROOT / '.tmp'
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    dest = out_dir / f'tmp-backup-{ts}.zip'
    print('Backup .tmp ->', dest)
    if args.dry_run:
        return
    if not src.exists():
        print('.tmp directory not found; nothing to back up')
        sys.exit(0)
    shutil.make_archive(str(dest.with_suffix('')), 'zip', root_dir=str(src))
    print('Created', dest)


if __name__ == '__main__':
    main()
