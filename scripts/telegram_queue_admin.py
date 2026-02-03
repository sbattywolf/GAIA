"""Admin CLI for inspecting and retrying failed Telegram queue items.

This is a lightweight helper to inspect `.tmp/telegram_queue_failed.json`
and either requeue items back to the main `.tmp/telegram_queue.json` or
remove them after manual handling.
"""
import argparse
import json
import os
from pathlib import Path

from scripts import telegram_queue as tq

ROOT = Path(__file__).resolve().parents[1]
FAILED = ROOT / '.tmp' / 'telegram_queue_failed.json'


def _safe_load(path: Path, default):
    try:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def _safe_save(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    try:
        os.replace(str(tmp), str(path))
    except Exception:
        path.write_text(json.dumps(obj, indent=2), encoding='utf-8')


def list_failed():
    items = _safe_load(FAILED, [])
    for i, it in enumerate(items):
        uid = it.get('update_id')
        cb = (it.get('callback_query') or {}).get('id') if it else None
        print(f"[{i}] update_id={uid} callback_id={cb} summary={str(it)[:80]}")


def requeue_index(idx: int):
    items = _safe_load(FAILED, [])
    if idx < 0 or idx >= len(items):
        print('invalid index')
        return
    item = items.pop(idx)
    ok = tq.requeue(item, front=False)
    if ok:
        _safe_save(FAILED, items)
        print('requeued', idx)
    else:
        print('requeue failed')


def requeue_all():
    items = _safe_load(FAILED, [])
    if not items:
        print('no failed items')
        return
    for it in items:
        tq.requeue(it, front=False)
    _safe_save(FAILED, [])
    print('requeued all')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--list', action='store_true')
    p.add_argument('--requeue-all', action='store_true')
    p.add_argument('--requeue', type=int, help='requeue a single failed index')
    args = p.parse_args()

    if args.list:
        list_failed()
        return 0
    if args.requeue_all:
        requeue_all()
        return 0
    if args.requeue is not None:
        requeue_index(args.requeue)
        return 0
    p.print_help()


if __name__ == '__main__':
    raise SystemExit(main())
