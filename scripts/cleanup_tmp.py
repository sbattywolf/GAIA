"""Cleanup and archive runtime artifacts under .tmp.

Usage:
  python scripts/cleanup_tmp.py --archive    # create a zip archive of .tmp (dry-run)
  python scripts/cleanup_tmp.py --clean      # delete runtime files under .tmp (dry-run)
  python scripts/cleanup_tmp.py --clean --yes    # perform deletion
  python scripts/cleanup_tmp.py --archive --yes  # perform archive

Defaults to a dry-run; pass --yes to perform destructive actions.
By default the script preserves `telegram.env` and the `archive/` folder.
"""
from pathlib import Path
import argparse
import shutil
import zipfile
import datetime
import sys


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp'


def list_candidates(p: Path):
    if not p.exists():
        return []
    preserve = {'telegram.env', 'telegram.env.bak', 'archive'}
    out = []
    for child in sorted(p.iterdir()):
        if child.name in preserve:
            continue
        out.append(child)
    return out


def make_archive(p: Path, dest_dir: Path, dry_run=True):
    dest_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    archive_name = dest_dir / f'tmp-archive-{ts}.zip'
    candidates = list_candidates(p)
    if dry_run:
        print(f'[dry-run] would create archive: {archive_name}')
        for c in candidates:
            print('  include:', c.relative_to(p))
        return archive_name
    print('creating archive', archive_name)
    with zipfile.ZipFile(archive_name, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for c in candidates:
            if c.is_file():
                z.write(c, arcname=c.name)
            else:
                for f in c.rglob('*'):
                    if f.is_file():
                        z.write(f, arcname=str(f.relative_to(p)))
    print('archive created:', archive_name)
    return archive_name


def clean_tmp(p: Path, dry_run=True):
    candidates = list_candidates(p)
    if not candidates:
        print('nothing to clean')
        return []
    if dry_run:
        print('[dry-run] would remove:')
        for c in candidates:
            print('  remove:', c)
        return candidates
    removed = []
    for c in candidates:
        try:
            if c.is_file():
                c.unlink()
            else:
                shutil.rmtree(c)
            removed.append(c)
        except Exception as e:
            print('error removing', c, e)
    print('removed', len(removed), 'items')
    return removed


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--archive', action='store_true', help='Create a zip archive of .tmp (preserves telegram.env)')
    p.add_argument('--clean', action='store_true', help='Remove runtime artifacts from .tmp (preserves telegram.env)')
    p.add_argument('--yes', action='store_true', help='Perform destructive actions (otherwise dry-run)')
    p.add_argument('--keep-archives-days', type=int, default=30, help='Prune archives older than N days')
    args = p.parse_args(argv)

    TMP.mkdir(parents=True, exist_ok=True)
    archive_dir = TMP / 'archive'

    if not args.archive and not args.clean:
        print('Nothing specified. Use --archive and/or --clean. (dry-run unless --yes)')
        return 0

    dry = not args.yes

    if args.archive:
        make_archive(TMP, archive_dir, dry_run=dry)

    if args.clean:
        clean_tmp(TMP, dry_run=dry)

    # prune old archives
    if archive_dir.exists():
        now = datetime.datetime.utcnow()
        for f in archive_dir.iterdir():
            try:
                m = datetime.datetime.utcfromtimestamp(f.stat().st_mtime)
                age = (now - m).days
                if age > args.keep_archives_days:
                    if dry:
                        print(f'[dry-run] would prune archive: {f.name} (age {age}d)')
                    else:
                        print('pruning old archive', f.name)
                        f.unlink()
            except Exception:
                pass

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
