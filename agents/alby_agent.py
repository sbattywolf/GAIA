#!/usr/bin/env python3
"""Alby 0.3 - minimal local job runner scaffold.

Features:
- CLI: `--task` `--cmd` `--concurrency` `--dry-run`
- Respects `PROTOTYPE_USE_LOCAL_EVENTS=1` or `DRY_RUN=1` for local-only mode.
- Emits NDJSON events to `GAIA_EVENTS_PATH` env or repo root `events.ndjson`.
- Writes simple audit rows into `gaia.db` via `orchestrator.init_db()`.
"""
import argparse
import os
import subprocess
import sqlite3
import uuid
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

from .agent_utils import build_event, append_event_atomic, is_dry_run
from .agent_utils import idempotency_key, retry_with_backoff, run_script
import shlex
import orchestrator


def get_events_path():
    return os.environ.get('GAIA_EVENTS_PATH') or str(Path(__file__).resolve().parents[1] / 'events.ndjson')


def get_out_path():
    # allow override for tests
    return Path(os.environ.get('ALBY_OUT_PATH') or (Path(__file__).resolve().parents[1] / 'out'))


def init_baby(agent_name='Alby 0.3'):
    out_dir = get_out_path()
    status_file = out_dir / 'status.json'
    notif_dir = out_dir / 'notifications'
    repo_root = Path(__file__).resolve().parents[1]

    if status_file.exists():
        return

    # ensure output directories exist early so we can write checklist/notifications
    out_dir.mkdir(parents=True, exist_ok=True)
    notif_dir.mkdir(parents=True, exist_ok=True)

    # capability validation: look for an 'internet_capable_agent.json' marker
    # check common upward locations so tests and different workspace layouts work
    internet_marker = None
    for candidate in (repo_root, repo_root.parent):
        cand = candidate / 'internet_capable_agent.json'
        if cand.exists():
            internet_marker = cand
            break
    # fallback to repo_root location if none found
    if internet_marker is None:
        internet_marker = repo_root / 'internet_capable_agent.json'
    internet_needed = internet_marker.exists()
    secrets_present = any(os.environ.get(k) for k in ('ALBY_INTERNET_TOKEN', 'CI_TOKEN', 'GITHUB_TOKEN'))

    # generate agent id early (used in requests)
    agent_id = str(uuid.uuid4())

    # if internet marker is a JSON file it may include a required_packages list
    required_packages = []
    try:
        if internet_needed:
            with open(internet_marker, 'r', encoding='utf-8') as f:
                try:
                    doc = json.load(f)
                    required_packages = doc.get('required_packages', []) if isinstance(doc, dict) else []
                except Exception:
                    required_packages = []
    except Exception:
        required_packages = []

    if internet_needed and not secrets_present:
        state = 'guarded'
        message = 'Internet-capable skills detected but no secrets set; set ALBY_INTERNET_TOKEN or CI_TOKEN to enable.'
        # write a short checklist for operator with suggested commands and placeholders
        checklist = out_dir / 'CHECKLIST.md'
        checklist_lines = []
        checklist_lines.append(f'# Checklist to enable internet-capable skills for {agent_name}')
        checklist_lines.append('')
        checklist_lines.append('1. Set the required API tokens as environment variables or in your .env file:')
        checklist_lines.append('')
        checklist_lines.append('```powershell')
        checklist_lines.append('setx ALBY_INTERNET_TOKEN "__REPLACE_WITH_TOKEN__"')
        checklist_lines.append('setx CI_TOKEN "__REPLACE_WITH_CI_TOKEN__"')
        checklist_lines.append('```')
        checklist_lines.append('')
        checklist_lines.append('2. Run smoke tests locally to verify skills:')
        checklist_lines.append('')
        checklist_lines.append('```powershell')
        checklist_lines.append('py -3 AGENT_TASKS/agent_runtime/alby_0_2/tests/baby_born_test.py')
        checklist_lines.append('py -3 AGENT_TASKS/agent_runtime/alby_0_2/smoke_skills.py --mode mock')
        checklist_lines.append('```')
        checklist_lines.append('')
        if required_packages:
            checklist_lines.append('3. Required packages to be downloaded and made available to the agent:')
            for pkg in required_packages:
                checklist_lines.append(f'- {pkg}')
            checklist_lines.append('')
        checklist_text = '\n'.join(checklist_lines)
        try:
            with open(checklist, 'w', encoding='utf-8') as f:
                f.write(checklist_text)
        except Exception:
            pass

        # create a package request in shared storage so another agent can pick it up
        try:
            # prefer explicit ALBY_SHARED_STORAGE, otherwise place under discovered repo_root
            shared = Path(os.environ.get('ALBY_SHARED_STORAGE') or (repo_root / 'shared_storage'))
            shared.mkdir(parents=True, exist_ok=True)
            if required_packages:
                req = {
                    'agent_id': agent_id,
                    'agent_name': agent_name,
                    'required_packages': required_packages,
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                }
                req_file = shared / f'packages_request_{agent_id}.json'
                with open(req_file, 'w', encoding='utf-8') as f:
                    json.dump(req, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    else:
        state = 'ready'
        message = f'Agent {agent_name} is ready.'

    agent_id = str(uuid.uuid4())
    payload = {
        'agent_id': agent_id,
        'agent_name': agent_name,
        'state': state,
        'message': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    notif_dir.mkdir(parents=True, exist_ok=True)

    # write status
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # write notification file
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    notif_file = notif_dir / f'ready_{ts}.json'
    with open(notif_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # emit agent-ready event
    events_path = get_events_path()
    ev = build_event('agent-ready', 'alby_agent', payload)
    append_event_atomic(events_path, ev)

    # write audit row
    try:
        orchestrator.init_db()
        write_audit('alby_agent', 'agent.start', agent_id)
    except Exception:
        pass


def write_audit(actor, action, details):
    orchestrator.init_db()
    conn = sqlite3.connect(orchestrator.DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO audit (timestamp, actor, action, details) VALUES (datetime("now"), ?, ?, ?)', (actor, action, details))
    conn.commit()
    conn.close()


def run_cmd(cmd, timeout=300):
    def _run():
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr

    try:
        return retry_with_backoff(_run, retries=3, base_backoff=0.5)
    except Exception as e:
        return 1, '', str(e)


def execute_command(cmd, timeout=300):
    """Execute a command string.

    If the first token is a path to an existing file, prefer the safe
    `agents.agent_utils.run_script` runner which picks the correct
    interpreter. Otherwise fall back to the shell-based `run_cmd`.
    Returns tuple (rc, stdout, stderr).
    """
    try:
        tokens = shlex.split(cmd)
    except Exception:
        # shlex failure: fallback to raw shell execution
        return run_cmd(cmd, timeout=timeout)

    if not tokens:
        return 1, '', 'no command'

    first = tokens[0]
    p = Path(first)
    # try resolving relative to repo root and cwd
    if not p.is_absolute():
        repo_root = Path(__file__).resolve().parents[1]
        cand1 = repo_root / first
        cand2 = Path.cwd() / first
        if cand1.exists():
            p = cand1
        elif cand2.exists():
            p = cand2

    if p.exists() and p.is_file():
        # use agent_utils.run_script which invokes scripts/run_script.py
        res = run_script(str(p), args=tokens[1:], timeout=timeout)
        return res.get('rc', 255), res.get('stdout', ''), res.get('stderr', '')

    # otherwise run via shell
    return run_cmd(cmd, timeout=timeout)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--task', default='run', help='Task type')
    p.add_argument('--cmd', required=True, help='Command to run')
    p.add_argument('--manifest', help='Path to a JSON manifest describing multiple steps')
    p.add_argument('--concurrency', type=int, default=1)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    dry = args.dry_run or is_dry_run()
    events_path = get_events_path()

    # run initialization / baby-born flow (idempotent)
    try:
        init_baby()
    except Exception:
        pass

    jobs = []
    # if manifest provided, manifest consumer will run multi-step tasks
    manifest = None
    if args.manifest:
        import json
        mp = args.manifest
        with open(mp, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

    if manifest:
        # manifest runner ignores concurrency; runs steps sequentially per manifest
        jobs = [{'job_id': str(uuid.uuid4()), 'step': s} for s in manifest.get('steps', [])]
    else:
        # allow multiple parallel runs of the same cmd
        for i in range(args.concurrency):
            jobs.append({'job_id': str(uuid.uuid4()), 'cmd': args.cmd})

    results = []
    if dry:
        for j in jobs:
            if manifest:
                step = j.get('step')
                payload = {'job_id': j['job_id'], 'step_id': step.get('id'), 'cmd': step.get('cmd'), 'returncode': 0, 'stdout': 'DRY_RUN', 'stderr': ''}
            else:
                payload = {'job_id': j['job_id'], 'cmd': j['cmd'], 'returncode': 0, 'stdout': 'DRY_RUN', 'stderr': ''}
            # add idempotency key to payload for tracing and dedup
            payload['idem'] = idempotency_key('alby_agent', payload)
            ev = build_event('alby.job.complete', 'alby_agent', payload)
            append_event_atomic(events_path, ev)
            write_audit('alby_agent', 'job.dry_run', j['job_id'])
            results.append((j['job_id'], 0))
        print('dry-run: emitted events for', len(jobs), 'jobs')
        return 0

    # Run jobs. If manifest provided, run steps sequentially and emit per-step events.
    if manifest:
        # single manifest run
        for j in jobs:
            step = j.get('step')
            step_cmd = step.get('cmd')
            timeout = step.get('timeout', 300)
            allow_fail = step.get('allow_fail', False)
            rc, out, err = execute_command(step_cmd, timeout=timeout)
            payload = {'job_id': j['job_id'], 'step_id': step.get('id'), 'cmd': step_cmd, 'returncode': rc, 'stdout': out, 'stderr': err}
            payload['idem'] = idempotency_key('alby_agent', payload)
            payload['trace'] = {'manifest': manifest.get('name'), 'started_by': os.getenv('USER') or os.getenv('USERNAME') or 'local'}
            ev = build_event('alby.manifest.step', 'alby_agent', payload)
            append_event_atomic(events_path, ev)
            write_audit('alby_agent', 'manifest.step', j['job_id'])
            results.append((j['job_id'], rc))
            if rc != 0 and not allow_fail:
                # stop execution on failure unless allowed
                break

        # emit manifest complete event
        manifest_payload = {'manifest': manifest.get('name'), 'steps': len(jobs), 'results': [{'job_id': r[0], 'rc': r[1]} for r in results]}
        manifest_payload['idem'] = idempotency_key('alby_agent', manifest_payload)
        append_event_atomic(events_path, build_event('alby.manifest.complete', 'alby_agent', manifest_payload))
    else:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = {ex.submit(execute_command, j['cmd']): j for j in jobs}
            for fut in as_completed(futures):
                j = futures[fut]
                rc, out, err = fut.result()
                payload = {'job_id': j['job_id'], 'cmd': j['cmd'], 'returncode': rc, 'stdout': out, 'stderr': err}
                payload['idem'] = idempotency_key('alby_agent', payload)
                # add lightweight trace info
                payload['trace'] = {'started_by': os.getenv('USER') or os.getenv('USERNAME') or 'local', 'worker': os.uname().nodename if hasattr(os, 'uname') else 'win' }
                ev = build_event('alby.job.complete', 'alby_agent', payload)
                append_event_atomic(events_path, ev)
                write_audit('alby_agent', 'job.run', j['job_id'])
                results.append((j['job_id'], rc))

    print('completed', len(results), 'jobs')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
