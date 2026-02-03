#!/usr/bin/env python3
"""Supervisor for telegram_service, dispatcher, and queue processor.

Starts child processes, writes PID files, rotates logs, restarts on failure,
and updates a combined health file `.tmp/telegram_supervisor_health.json`.
"""
import os
import sys
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp'
LOGS = TMP / 'logs'
TMP.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

SERVICE_PID = TMP / 'telegram_service.pid'
DISPATCHER_PID = TMP / 'telegram_dispatcher.pid'
HEALTH_FILE = TMP / 'telegram_supervisor_health.json'

def now():
    return datetime.utcnow().isoformat() + 'Z'

def write_pid(path: Path, pid: int):
    try:
        path.write_text(str(pid), encoding='utf-8')
    except Exception:
        pass

def remove_pid(path: Path):
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass

def rotate_log(p: Path, max_bytes=5*1024*1024):
    try:
        if p.exists() and p.stat().st_size > max_bytes:
            p.rename(p.with_suffix('.log.' + datetime.utcnow().strftime('%Y%m%dT%H%M%S')))
    except Exception:
        pass

def start_process(cmd, stdout_path, stderr_path, env=None):
    rotate_log(stdout_path)
    rotate_log(stderr_path)
    out = open(stdout_path, 'ab')
    err = open(stderr_path, 'ab')
    proc = subprocess.Popen(cmd, stdout=out, stderr=err, env=env)
    return proc, out, err

def update_health(running_services):
    h = {
        'updated': now(),
        'services': running_services
    }
    try:
        tmp = HEALTH_FILE.with_suffix('.tmp')
        tmp.write_text(json.dumps(h, indent=2), encoding='utf-8')
        os.replace(str(tmp), str(HEALTH_FILE))
    except Exception:
        pass

def load_env_file():
    env = os.environ.copy()
    envfile = TMP / 'telegram.env'
    if envfile.exists():
        for line in envfile.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k,v = line.split('=',1)
            env[k.strip()] = v.strip()
    return env

def supervisor_loop(poll_seconds=5):
    env = load_env_file()
    python = sys.executable
    svc_cmd = [python, str(ROOT / 'scripts' / 'telegram_service.py'), '--timeout', '0', '--poll', '10']
    disp_cmd = [python, str(ROOT / 'scripts' / 'dispatcher.py')]
    queue_cmd = [python, str(ROOT / 'scripts' / 'process_telegram_queue.py')]

    svc_log = LOGS / 'telegram_service.log'
    svc_err = LOGS / 'telegram_service.err.log'
    disp_log = LOGS / 'dispatcher.log'
    disp_err = LOGS / 'dispatcher.err.log'
    queue_log = LOGS / 'process_queue.log'
    queue_err = LOGS / 'process_queue.err.log'

    svc_proc = None
    disp_proc = None
    queue_last_run = 0

    try:
        while True:
            # ensure service running
            if not svc_proc or svc_proc.poll() is not None:
                if svc_proc and svc_proc.poll() is not None:
                    print('telegram_service exited, restarting')
                    try:
                        svc_proc.kill()
                    except Exception:
                        pass
                svc_proc, so, se = start_process(svc_cmd, svc_log, svc_err, env=env)
                write_pid(SERVICE_PID, svc_proc.pid)

            # run dispatcher once per poll loop (it processes queue and exits)
            if not disp_proc or disp_proc.poll() is not None:
                try:
                    disp_proc, dso, dse = start_process(disp_cmd, disp_log, disp_err, env=env)
                    write_pid(DISPATCHER_PID, disp_proc.pid)
                except Exception as e:
                    print('failed to start dispatcher', e)

            # periodically run queue retry (every 60s)
            now_ts = time.time()
            if now_ts - queue_last_run > 60:
                try:
                    qproc, qso, qse = start_process(queue_cmd, queue_log, queue_err, env=env)
                    # don't block starting; we simply note start
                    queue_last_run = now_ts
                except Exception:
                    pass

            # update health file
            running = {
                'telegram_service': {'pid': svc_proc.pid if svc_proc else None, 'alive': svc_proc.poll() is None if svc_proc else False},
                'dispatcher': {'pid': disp_proc.pid if disp_proc else None, 'alive': disp_proc.poll() is None if disp_proc else False},
                'last_queue_retry': datetime.utcfromtimestamp(queue_last_run).isoformat() + 'Z' if queue_last_run else None
            }
            update_health(running)

            time.sleep(poll_seconds)
    except KeyboardInterrupt:
        print('supervisor interrupted, terminating children')
    finally:
        try:
            if svc_proc and svc_proc.poll() is None:
                svc_proc.terminate()
        except Exception:
            pass
        try:
            if disp_proc and disp_proc.poll() is None:
                disp_proc.terminate()
        except Exception:
            pass
        remove_pid(SERVICE_PID)
        remove_pid(DISPATCHER_PID)

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--poll', type=int, default=5)
    args = p.parse_args()
    supervisor_loop(poll_seconds=args.poll)

if __name__ == '__main__':
    main()
