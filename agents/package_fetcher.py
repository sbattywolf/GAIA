#!/usr/bin/env python3
"""Package fetcher agent

Watches `ALBY_SHARED_STORAGE` (or repo/shared_storage) for
`packages_request_*.json` files and produces `packages_response_*.json`.

This agent is intentionally conservative: by default it simulates
fetching (writes stub files) and is `--dry-run` / `PROTOTYPE_USE_LOCAL_EVENTS`
aware.
"""
import argparse
import json
import os
import sqlite3
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

from .agent_utils import build_event, append_event_atomic, is_dry_run, idempotency_key, run_script
import shlex
import sys
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


def process_request(req_file: Path, shared: Path, dry: bool):
    try:
        doc = json.loads(req_file.read_text(encoding='utf-8'))
    except Exception:
        return False

    agent_id = doc.get('agent_id') or req_file.stem
    req_pkgs = doc.get('required_packages', []) or []

    # prepare response
    resp = {'agent_id': agent_id, 'requested': req_pkgs, 'results': [], 'timestamp': datetime.utcnow().isoformat() + 'Z'}

    cache = shared / 'packages_cache' / agent_id
    if not dry:
        cache.mkdir(parents=True, exist_ok=True)

    for pkg in req_pkgs:
        # If pkg is a file:// URL or an existing local path, copy it into cache.
        status = 'unknown'
        try:
            if pkg.startswith('file://'):
                src = Path(pkg[len('file://'):])
                if src.exists():
                    if not dry:
                        shutil.copy2(src, cache / src.name)
                    status = 'copied'
                else:
                    status = 'missing'
            else:
                p = Path(pkg)
                if p.exists():
                    if not dry:
                        shutil.copy2(p, cache / p.name)
                    status = 'copied'
                else:
                    # attempt to use pip to download the distribution into cache
                    if not dry:
                        try:
                            # prefer safe runner for local script files; otherwise run via subprocess
                            cmd = ['python', '-m', 'pip', 'download', '--no-deps', '-d', str(cache), pkg]
                            # if command refers to an existing file, use run_script; else run subprocess
                            def _run_cmd(cmd_obj, timeout=120):
                                if isinstance(cmd_obj, (list, tuple)):
                                    proc = subprocess.run(cmd_obj, capture_output=True, text=True, check=False, timeout=timeout)
                                    return proc.returncode, proc.stdout, proc.stderr
                                # string path: split
                                try:
                                    tokens = shlex.split(cmd_obj)
                                except Exception:
                                    tokens = [cmd_obj]
                                first = tokens[0] if tokens else ''
                                p = Path(first)
                                if not p.is_absolute():
                                    repo_root = Path(__file__).resolve().parents[1]
                                    cand1 = repo_root / first
                                    cand2 = Path.cwd() / first
                                    if cand1.exists():
                                        p = cand1
                                    elif cand2.exists():
                                        p = cand2
                                if p.exists() and p.is_file():
                                    res = run_script(str(p), args=tokens[1:], timeout=timeout)
                                    return res.get('rc', 255), res.get('stdout', ''), res.get('stderr', '')
                                # fallback
                                proc = subprocess.run(tokens, capture_output=True, text=True, check=False, timeout=timeout)
                                return proc.returncode, proc.stdout, proc.stderr

                            rc, out, err = _run_cmd(cmd, timeout=120)
                            if rc == 0:
                                status = 'downloaded'
                            else:
                                status = f'pip-error: {rc} {err.strip()[:200]}'
                        except Exception as e:
                            status = f'pip-exception: {e}'
                    else:
                        status = 'dry-run'
        except Exception as e:
            status = f'error: {e}'

        resp['results'].append({'package': pkg, 'status': status})

    # write response file
    resp_file = shared / f'packages_response_{agent_id}.json'
    try:
        if not dry:
            resp_file.write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        pass

    # emit event
    events_path = get_events_path()
    payload = {'agent_id': agent_id, 'response_file': str(resp_file), 'results': resp['results']}
    payload['idem'] = idempotency_key('package_fetcher', payload)
    ev = build_event('packages.request.fulfilled', 'package_fetcher', payload)
    append_event_atomic(events_path, ev)
    write_audit('package_fetcher', 'request.processed', agent_id)

    # move processed request to processed/ folder to avoid reprocessing
    try:
        processed = shared / 'processed'
        processed.mkdir(parents=True, exist_ok=True)
        req_file.rename(processed / req_file.name)
    except Exception:
        try:
            req_file.unlink()
        except Exception:
            pass

    return True


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--shared', help='Shared storage path (overrides ALBY_SHARED_STORAGE)')
    p.add_argument('--scan-once', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    dry = args.dry_run or is_dry_run()
    shared = Path(args.shared or os.environ.get('ALBY_SHARED_STORAGE') or (Path(__file__).resolve().parents[1] / 'shared_storage'))
    shared.mkdir(parents=True, exist_ok=True)

    # scan for requests
    found = False
    for f in list(shared.glob('packages_request_*.json')):
        found = True
        process_request(f, shared, dry=dry)

    if not args.scan_once:
        # if not scan-once, run just once but return non-zero when no requests found
        return 0 if found else 2

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
