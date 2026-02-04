#!/usr/bin/env python3
"""Snapshot and version .draft/.current and canonical doc files.

Usage:
  python scripts/version_docs.py --archive      # archive matching files to doc/archive with timestamp
  python scripts/version_docs.py --bump v1.2.3  # set 'version' field in JSON files to provided string and archive

This is a lightweight helper to keep file history outside of Git or to create snapshots for releases.
"""
from __future__ import annotations
import argparse
import os
import shutil
import datetime
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ARCHIVE_DIR = os.path.join(ROOT, 'doc', 'archive')


def ensure_archive_dir() -> None:
    os.makedirs(ARCHIVE_DIR, exist_ok=True)


def timestamp() -> str:
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')


def archive_file(path: str) -> str:
    ensure_archive_dir()
    base = os.path.basename(path)
    dest = os.path.join(ARCHIVE_DIR, f"{base}.{timestamp()}.archived")
    shutil.copy2(path, dest)
    return dest


def try_update_json_version(path: str, version: str) -> bool:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return False
    data['version'] = version
    data['versioned_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True


def find_targets(root: str) -> list[str]:
    targets = []
    for folder, _, files in os.walk(root):
        for fn in files:
            if fn.endswith('.draft') or fn.endswith('.current'):
                targets.append(os.path.join(folder, fn))
    # include canonical doc files
    docs = os.path.join(root, 'doc')
    if os.path.isdir(docs):
        for fn in os.listdir(docs):
            if fn.endswith('.current') or fn.endswith('.draft'):
                targets.append(os.path.join(docs, fn))
    return sorted(set(targets))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--archive', action='store_true', help='Archive matching files')
    p.add_argument('--bump', type=str, help='Version string to set in JSON-backed files')
    args = p.parse_args()

    targets = find_targets(ROOT)
    if not targets:
        print('No .draft/.current files found.')
        return

    print(f'Found {len(targets)} targets')
    for t in targets:
        print(' -', t)
        archived = archive_file(t)
        print('   archived ->', archived)
        if args.bump:
            if try_update_json_version(t, args.bump):
                print('   updated version ->', args.bump)
            else:
                print('   not a JSON file, skipped version update')

    print('Done')


if __name__ == '__main__':
    main()
