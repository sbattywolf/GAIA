"""Safe auto-requeue tool.

Reads `.tmp/telegram_queue_failed_permanent.json` and requeues eligible items
back into `.tmp/telegram_queue_failed.json` for another retry run.

Policy (defaults):
- only items with `_retries` less than `MAX_RETRIES` are eligible (default 3)
- only items failed within `MAX_AGE_HOURS` (default 72 hours) are eligible
- limit number of requeued items per run `MAX_PER_RUN` (default 10)

Usage:
  python scripts/auto_requeue.py --dry-run
"""
from pathlib import Path
import json
import os
from datetime import datetime, timedelta, timezone
import argparse

ROOT = Path(__file__).resolve().parents[1]
PERM_FILE = ROOT / '.tmp' / 'telegram_queue_failed_permanent.json'
FAILED_FILE = ROOT / '.tmp' / 'telegram_queue_failed.json'


def safe_load(path: Path):
    try:
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding='utf-8') or '[]')
    except Exception:
        return []


def safe_save(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    try:
        os.replace(str(tmp), str(path))
    except Exception:
        path.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def parse_env():
    return {
        'MAX_RETRIES': int(os.environ.get('AUTO_REQUEUE_MAX_RETRIES', '3')),
        'MAX_AGE_HOURS': int(os.environ.get('AUTO_REQUEUE_MAX_AGE_HOURS', '72')),
        'MAX_PER_RUN': int(os.environ.get('AUTO_REQUEUE_MAX_PER_RUN', '10')),
    }


def is_eligible(item, now, max_retries, max_age):
    try:
        retries = int(item.get('_retries', 0))
    except Exception:
        retries = 0
    if retries >= max_retries:
        return False
    failed_at = item.get('_failed_at')
    if not failed_at:
        return False
    try:
        dt = datetime.fromisoformat(failed_at.replace('Z', '+00:00'))
    except Exception:
        return False
    if now - dt > timedelta(hours=max_age):
        return False
    return True


def run(dry_run=False):
    env = parse_env()
    perm = safe_load(PERM_FILE)
    failed = safe_load(FAILED_FILE) or []
    now = datetime.now(timezone.utc)
    requeued = []
    kept = []

    for item in perm:
        if len(requeued) >= env['MAX_PER_RUN']:
            kept.append(item)
            continue
        if is_eligible(item, now, env['MAX_RETRIES'], env['MAX_AGE_HOURS']):
            # increment retries and clear failed timestamp
            item['_retries'] = int(item.get('_retries', 0)) + 1
            item.pop('_failed_at', None)
            requeued.append(item)
        else:
            kept.append(item)

    if not dry_run:
        # append requeued to FAILED_FILE (so process_failed_items_once will retry them)
        failed = requeued + failed
        safe_save(FAILED_FILE, failed)
        # persist remaining permanent items
        safe_save(PERM_FILE, kept)

    return {'considered': len(perm), 'requeued': len(requeued), 'remaining_permanent': len(kept)}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)
    out = run(dry_run=args.dry_run)
    print('Auto-requeue:', out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
