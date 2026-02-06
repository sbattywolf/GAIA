#!/usr/bin/env python3
"""Create a timestamped backup of the encrypted secrets store and key."""
from pathlib import Path
from datetime import datetime, timezone
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / '.private'
SE_FILE = PRIVATE / 'secrets.enc'
KEY_FILE = PRIVATE / 'secrets.key'
BACKUP_DIR = PRIVATE / 'backups'

def timestamp():
    return datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')

def main():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = timestamp()
    created = []
    if SE_FILE.exists():
        dest = BACKUP_DIR / f'secrets.enc.bak.{ts}'
        shutil.copy2(SE_FILE, dest)
        created.append(dest)
    else:
        print('Warning: encrypted store not found at', SE_FILE)

    if KEY_FILE.exists():
        destk = BACKUP_DIR / f'secrets.key.bak.{ts}'
        shutil.copy2(KEY_FILE, destk)
        created.append(destk)
    else:
        print('Warning: key file not found at', KEY_FILE)

    if not created:
        print('No files backed up.')
        sys.exit(1)

    print('Backed up:')
    for p in created:
        print(' -', p)

if __name__ == '__main__':
    main()
