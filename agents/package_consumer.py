#!/usr/bin/env python3
"""Package consumer agent

Watches `ALBY_SHARED_STORAGE` (or repo/shared_storage) for
`packages_response_*.json` files and installs/copies provided packages into
`ALBY_OUT_PATH/vendor/<agent_id>` so local agents can consume them.

Conservative behavior: supports `--scan-once`, is `--dry-run` / `PROTOTYPE_USE_LOCAL_EVENTS`
aware, and emits `packages.installed` events and audit rows.
"""
import argparse
import json
import os
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

from .agent_utils import build_event, append_event_atomic, is_dry_run, idempotency_key
import orchestrator


def get_events_path():
    return os.environ.get('GAIA_EVENTS_PATH') or str(Path(__file__).resolve().parents[1] / 'events.ndjson')


def write_audit(actor, action, details):
    try:
        orchestrator.init_db()
        conn = sqlite3.connect(orchestrator.DB_PATH)
        cur = conn.cursor()
        cur.execute('INSERT INTO audit (timestamp, actor, action, details) VALUES (datetime("now"), ?, ?, ?)', (actor, action, details))
        conn.commit()
        conn.close()
    except Exception:
        pass


def process_response(resp_file: Path, shared: Path, out_root: Path, dry: bool):
    try:
        doc = json.loads(resp_file.read_text(encoding='utf-8'))
    except Exception:
        return False

    agent_id = doc.get('agent_id') or resp_file.stem
    cache = shared / 'packages_cache' / agent_id
    vendor = out_root / 'vendor' / agent_id

    results = []
    if not dry:
        vendor.mkdir(parents=True, exist_ok=True)

    # copy any files from cache for this agent into vendor
    if cache.exists() and cache.is_dir():
        for f in cache.iterdir():
            try:
                if not dry:
                    shutil.copy2(f, vendor / f.name)
                results.append({'file': f.name, 'status': 'copied'})
            except Exception as e:
                results.append({'file': f.name, 'status': f'error: {e}'})
    else:
        results.append({'status': 'no-cache'})

    # emit event indicating packages installed/available
    events_path = get_events_path()
    payload = {'agent_id': agent_id, 'vendor_path': str(vendor), 'results': results}
    payload['idem'] = idempotency_key('package_consumer', payload)
    ev = build_event('packages.installed', 'package_consumer', payload)
    append_event_atomic(events_path, ev)
    write_audit('package_consumer', 'response.processed', agent_id)

    # move processed response to processed/ to avoid reprocessing
    try:
        processed = shared / 'processed'
        processed.mkdir(parents=True, exist_ok=True)
        resp_file.rename(processed / resp_file.name)
    except Exception:
        try:
            resp_file.unlink()
        except Exception:
            pass

    return True


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--shared', help='Shared storage path (overrides ALBY_SHARED_STORAGE)')
    p.add_argument('--out', help='ALBY_OUT_PATH override')
    p.add_argument('--scan-once', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    dry = args.dry_run or is_dry_run()
    shared = Path(args.shared or os.environ.get('ALBY_SHARED_STORAGE') or (Path(__file__).resolve().parents[1] / 'shared_storage'))
    out_root = Path(args.out or os.environ.get('ALBY_OUT_PATH') or (Path(__file__).resolve().parents[1] / 'out'))
    shared.mkdir(parents=True, exist_ok=True)
    out_root.mkdir(parents=True, exist_ok=True)

    found = False
    for f in list(shared.glob('packages_response_*.json')):
        found = True
        process_response(f, shared, out_root, dry=dry)

    if not args.scan_once:
        return 0 if found else 2

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
