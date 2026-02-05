#!/usr/bin/env python3
"""
Simple local monitoring framework for GAIA agents.

Features:
- Monitor expected service PID files in `.tmp/*_pid.txt` (approval_listener, automation_runner, resource_monitor)
- Emit events to `gaia.events` (events.ndjson) and write concise logs to `.tmp/monitor_framework.log`
- Send Telegram alerts via `scripts/send_simple_telegram.py` for service down and heartbeats

This is a lightweight orchestrator-monitor intended for local/NAS deployment.
"""
import os
import sys
import time
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TMP = os.path.join(ROOT, '.tmp')
LOG = os.path.join(TMP, 'monitor_framework.log')
PID_TEMPL = os.path.join(TMP, '{}_pid.txt')

SERVICES = ['approval_listener', 'automation_runner', 'resource_monitor']
HEARTBEAT_INTERVAL = 60
CHECK_INTERVAL = 10


def now():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


def flog(msg: str):
    os.makedirs(TMP, exist_ok=True)
    with open(LOG, 'a', encoding='utf8') as f:
        f.write(f'[{now()}] {msg}\n')


def send_telegram(msg: str):
    try:
        import subprocess
        subprocess.run([sys.executable, os.path.join('scripts', 'send_simple_telegram.py'), msg], check=False)
        flog(f'Telegram: {msg}')
    except Exception as e:
        flog(f'Failed to send telegram: {e}')


def pid_alive(pid: int) -> bool:
    try:
        import psutil
        return psutil.pid_exists(pid)
    except Exception:
        # fallback: on Windows try os.kill with signal 0
        try:
            os.kill(pid, 0)
            return True
        except Exception:
            return False


def read_pid(service: str):
    path = PID_TEMPL.format(service)
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='ascii') as f:
            return int(f.read().strip())
    except Exception:
        return None


def main():
    from gaia import events

    flog('monitor_framework started')
    last_heartbeat = 0
    alerted = set()

    while True:
        try:
            any_down = False
            for svc in SERVICES:
                pid = read_pid(svc)
                if pid is None or not pid_alive(pid):
                    any_down = True
                    if svc not in alerted:
                        msg = f'service_down: {svc}'
                        events.make_event('monitor.service.down', {'service': svc})
                        send_telegram(f'GAIA monitor alert: {svc} appears down')
                        flog(msg)
                        alerted.add(svc)
                else:
                    if svc in alerted:
                        events.make_event('monitor.service.up', {'service': svc, 'pid': pid})
                        send_telegram(f'GAIA monitor: {svc} is back (pid {pid})')
                        flog(f'service_up: {svc} pid={pid}')
                        alerted.discard(svc)

            if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                events.make_event('monitor.heartbeat', {'services': SERVICES})
                flog('heartbeat')
                last_heartbeat = time.time()

            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            flog('monitor_framework stopped by KeyboardInterrupt')
            break
        except Exception as e:
            flog(f'unhandled error: {e}')
            time.sleep(5)


if __name__ == '__main__':
    sys.exit(main())
