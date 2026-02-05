#!/usr/bin/env python3
"""Simple scheduler to start/stop GAIA background services based on a JSON schedule.

Schedule format (.tmp/schedule.json):
[
  {"service":"monitor","action":"start","start_immediately":true},
  {"service":"telegram_bridge","action":"start","start_immediately":true}
]

Services supported: monitor, telegram_bridge, approval_listener, periodic_runner
This script is intentionally simple: it executes the corresponding .tmp/*.ps1 starter scripts.
"""
import time
import json
import os
import subprocess
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE_FILE = ROOT / '.tmp' / 'schedule.json'
SCRIPTS = {
    'monitor': ROOT / '.tmp' / 'start_monitor.ps1',
    'telegram_bridge': ROOT / '.tmp' / 'telegram_bridge_job.ps1',
    'approval_listener': ROOT / '.tmp' / 'approval_job.ps1',
    'periodic_runner': ROOT / '.tmp' / 'periodic_job.ps1'
}

# pid files are kept in .tmp as <service>_pid.txt when services write them
PID_DIR = ROOT / '.tmp'


def run_script(ps_path):
    if not ps_path.exists():
        print('script missing', ps_path)
        return False
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(ps_path)]
    try:
        subprocess.Popen(cmd)
        print('started', ps_path)
        return True
    except Exception as e:
        print('failed to start', ps_path, e)
        return False


def _pidfile_for(service):
    return PID_DIR / f"{service}_pid.txt"


def _read_pid(service):
    p = _pidfile_for(service)
    if not p.exists():
        return None
    try:
        with open(p, 'r', encoding='utf-8') as f:
            txt = f.read().strip()
        return int(txt)
    except Exception:
        return None


def _is_pid_running(pid):
    if pid is None:
        return False
    try:
        # Windows-friendly check using tasklist
        out = subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'], stderr=subprocess.DEVNULL, text=True)
        return str(pid) in out
    except Exception:
        return False


def _kill_pid(pid):
    try:
        subprocess.check_call(['taskkill', '/PID', str(pid), '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def main(loop_interval=60):
    print('Scheduler starting, reading', SCHEDULE_FILE)
    while True:
        try:
            if SCHEDULE_FILE.exists():
                with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                    sched = json.load(f)
                for entry in sched:
                    svc = entry.get('service')
                    action = entry.get('action')
                    # allow schedule entries to be enabled/disabled
                    if action == 'enable':
                        entry['enabled'] = True
                    elif action == 'disable':
                        entry['enabled'] = False

                    enabled = entry.get('enabled', True)

                    if entry.get('start_immediately') and action == 'start' and enabled:
                        s = SCRIPTS.get(svc)
                        if s:
                            # optionally ensure single instance by killing previous pid
                            if entry.get('ensure_single'):
                                pid = _read_pid(svc)
                                if pid and _is_pid_running(pid):
                                    print(f'Killing previous {svc} pid {pid}')
                                    ok = _kill_pid(pid)
                                    if ok:
                                        try:
                                            _pidfile_for(svc).unlink()
                                        except Exception:
                                            pass
                            run_script(s)
                            # clear flag so we don't restart endlessly
                            entry['start_immediately'] = False
                # write back to persist cleared flags
                with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(sched, f, indent=2)
            else:
                print('No schedule file at', SCHEDULE_FILE)
        except Exception as e:
            print('scheduler error', e)
        time.sleep(loop_interval)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--interval', type=int, default=60, help='Loop interval seconds')
    args = p.parse_args()
    main(loop_interval=args.interval)
