#!/usr/bin/env python3
"""Autonomous runner for Gise.0.3

Usage: python scripts/gise_autonomous_runner.py --duration-hours 20

Behavior:
- Post short status updates to configured Telegram chat every 10 minutes for a configurable period (default 20h)
- Also post every 30 minutes for a configurable period (default 30h)
- Run lightweight validator on each update and include its result
- Gather epic progress from `doc/EPC_Telegram.current` and include counts of features/stories/tasks
- Attempt small STR_TestGise.part1 helpers (smoke_check, export) between updates
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent


def load_env(env_path: Path) -> dict:
    env = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def load_preferred_env() -> dict:
    """Load env preferring `.private/telegram.env` then `.tmp/telegram.env`.

    Returns an env dict (may be empty).
    """
    private = ROOT / '.private' / 'telegram.env'
    tmp = ROOT / '.tmp' / 'telegram.env'
    if private.exists():
        try:
            return load_env(private)
        except Exception:
            print('Warning: failed to read .private/telegram.env; falling back to .tmp/telegram.env')
    return load_env(tmp)


def env_flag_true(env: dict, key: str) -> bool:
    v = env.get(key)
    if v is None:
        return False
    return str(v).lower() in ('1', 'true', 'yes', 'on')


def send_telegram(token: str, chat_id: str, text: str) -> bool:
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': chat_id, 'text': text})
        r.raise_for_status()
        return True
    except Exception:
        return False


def run_validator() -> str:
    script = ROOT / 'scripts' / 'validate_todolists.py'
    if not script.exists():
        return 'validator missing'
    try:
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=False)
        out = (r.stdout or '') + (r.stderr or '')
        return out.strip().splitlines()[-3:] if out else ['no output']
    except Exception as e:
        return [f'validator failed: {e}']


def parse_epic_progress(epic_file: Path) -> dict:
    try:
        text = epic_file.read_text(encoding='utf-8')
        data = json.loads(text)
    except Exception:
        return {'error': 'failed to load epic'}
    features = data.get('features', [])
    feat_count = len(features)
    story_count = 0
    tasks_total = 0
    tasks_done = 0
    for f in features:
        for s in f.get('stories', []):
            story_count += 1
            for t in s.get('tasks', []):
                tasks_total += 1
                if t.get('status') in ('done', 'completed'):
                    tasks_done += 1
    return {'features': feat_count, 'stories': story_count, 'tasks_total': tasks_total, 'tasks_done': tasks_done}


def try_part1_helpers():
    # call gise_worker_0_3 smoke and export helpers
    gw = ROOT / 'scripts' / 'gise_worker_0_3.py'
    out = []
    if gw.exists():
        try:
            r = subprocess.run([sys.executable, str(gw), '--smoke'], capture_output=True, text=True, check=False)
            out.append(('smoke', r.returncode, (r.stdout or '').strip().splitlines()[-3:]))
        except Exception as e:
            out.append(('smoke-exc', str(e)))
        try:
            # call export_chat_history via running script as module
            # it creates files in .tmp/exports
            r2 = subprocess.run([sys.executable, str(gw),], capture_output=True, text=True, check=False)
            out.append(('run', r2.returncode))
        except Exception as e:
            out.append(('run-exc', str(e)))
    else:
        out.append(('gise_worker_missing', True))
    return out


def status_message(epic_summary: dict, validator_out, helper_out) -> str:
    now = datetime.utcnow().isoformat() + 'Z'
    lines = [f'GAIA status {now}', f"Features: {epic_summary.get('features')}, Stories: {epic_summary.get('stories')}", f"Tasks: {epic_summary.get('tasks_done')}/{epic_summary.get('tasks_total')}"]
    lines.append('Validator:')
    if isinstance(validator_out, list):
        lines.extend([str(x) for x in validator_out])
    else:
        lines.append(str(validator_out))
    lines.append('Helpers:')
    for h in helper_out:
        lines.append(str(h))
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--tenmin-hours', type=float, default=20.0, help='Hours to send 10-min updates')
    p.add_argument('--thirtymin-hours', type=float, default=30.0, help='Hours to send 30-min updates')
    p.add_argument('--duration-hours', type=float, default=20.0, help='Primary work duration (hours)')
    p.add_argument('--nogise', action='store_true', help='Do not run Gise helper tasks; run validator and send updates only')
    args = p.parse_args()

    env = load_preferred_env()
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')

    epic_file = ROOT / 'doc' / 'EPC_Telegram.current'

    start = datetime.utcnow()
    end_ten = start + timedelta(hours=args.tenmin_hours)
    end_thirty = start + timedelta(hours=args.thirtymin_hours)
    end_work = start + timedelta(hours=args.duration_hours)

    next_ten = start
    next_thirty = start

    # loop until primary work duration ends; also continue thirty-min updates until their end
    while datetime.utcnow() < end_work or datetime.utcnow() < end_thirty:
        now = datetime.utcnow()
        do_ten = now >= next_ten and now < end_ten
        do_thirty = now >= next_thirty and now < end_thirty
        if do_ten or do_thirty:
            val = run_validator()
            epic = parse_epic_progress(epic_file)
            helpers = []
            if not args.nogise:
                helpers = try_part1_helpers()
            else:
                helpers = [('nogise', 'skipped')]
            msg = status_message(epic, val, helpers)
            sent = False
            # Require explicit opt-in to send notifications; safe default is off
            enabled = env_flag_true(env, 'PERIODIC_NOTIFICATIONS_ENABLED')
            allow_exec = env.get('ALLOW_COMMAND_EXECUTION', '0') == '1'
            prototype_local = env_flag_true(env, 'PROTOTYPE_USE_LOCAL_EVENTS')

            if enabled and token and chat and allow_exec and not prototype_local:
                sent = send_telegram(token, chat, msg)
            else:
                # If prototype local events enabled, treat as simulated send
                if enabled and prototype_local:
                    print('Periodic notifier: prototype local events enabled — simulated send')
                if not enabled:
                    print('Periodic notifier not enabled (set PERIODIC_NOTIFICATIONS_ENABLED=1 to opt-in)')
                if enabled and not allow_exec:
                    print('ALLOW_COMMAND_EXECUTION != 1; not sending')
            # also write a local status note
            note_dir = ROOT / '.tmp' / 'gise_status'
            note_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
            note_file = note_dir / f'status_{ts}.txt'
            note_file.write_text(msg, encoding='utf-8')
            print(f'[{ts}] Posted status (telegram={sent})')
            if do_ten:
                next_ten = now + timedelta(minutes=10)
            if do_thirty:
                next_thirty = now + timedelta(minutes=30)
        # small sleep to avoid busy loop
        time.sleep(15)


if __name__ == '__main__':
    main()
