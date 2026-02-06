#!/usr/bin/env python3
"""Sanitize and relocate plaintext secret files into an external env file.

Usage:
  python scripts/sanitize_secrets.py --external E:\\Workspaces\\Git\\.secret\\.env

Behavior:
- Copies `.private/.env` -> external path (if present) and backs up any existing external file.
- Moves known candidate token files into `.private/backups/` with timestamped names.
"""
from pathlib import Path
import shutil
import argparse
import os
import time


ROOT = Path(__file__).resolve().parent.parent


def timestamp():
    return time.strftime('%Y%m%dT%H%M%S')


def ensure_dir(p: Path):
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)


def move_to_backup(src: Path, backup_dir: Path):
    ensure_dir(backup_dir)
    dest = backup_dir / (src.name + '.bak.' + timestamp())
    shutil.move(str(src), str(dest))
    print(f'Moved {src} -> {dest}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--external', help='External env path to create/use', default=None)
    args = p.parse_args()

    ext = args.external or os.environ.get('PRIVATE_ENV_PATH') or str(Path('E:/Workspaces/Git/.secret/.env'))
    ext_path = Path(ext)

    private_env = ROOT / '.private' / '.env'
    backup_dir = ROOT / '.private' / 'backups'

    # Backup existing external file if present
    if ext_path.exists():
        ensure_dir(ext_path.parent)
        b = ext_path.parent / (ext_path.name + '.bak.' + timestamp())
        shutil.copy2(str(ext_path), str(b))
        print(f'Backed up existing external env: {ext_path} -> {b}')

    # Copy .private/.env to external if exists
    if private_env.exists():
        ensure_dir(ext_path.parent)
        shutil.copy2(str(private_env), str(ext_path))
        print(f'Copied {private_env} -> {ext_path}')
    else:
        # create placeholder external file if missing
        ensure_dir(ext_path.parent)
        if not ext_path.exists():
            ext_path.write_text('# External env file created by sanitize_secrets.py\n')
            print(f'Created placeholder external env: {ext_path}')

    # Candidate files to sanitize/move
    candidates = [
        ROOT / '.private' / '.env',
        ROOT / '.private' / 'telegram.env',
        ROOT / '.tmp' / 'telegram.env',
    ]

    for c in candidates:
        if c.exists():
            # if c equals external path, skip
            try:
                # Do not remove the external file we just created/copied
                if c.resolve() == ext_path.resolve():
                    print(f'Skipping external file {c}')
                    continue
            except Exception:
                pass
            move_to_backup(c, backup_dir)

    print('Sanitize complete. Set PRIVATE_ENV_PATH to', ext_path)


if __name__ == '__main__':
    main()
