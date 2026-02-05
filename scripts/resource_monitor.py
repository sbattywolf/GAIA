#!/usr/bin/env python3
"""
Lightweight resource monitor: watches CPU and memory and sends Telegram alerts
when thresholds are exceeded. Writes concise logs to .tmp/resource_monitor.log.

Usage: python scripts/resource_monitor.py

Notes:
- Requires `psutil` for accurate metrics. If not installed, the script logs
  an error and exits. Install with `pip install psutil`.
"""
import os
import sys
import time
import subprocess
from datetime import datetime

LOG_PATH = os.path.join('.tmp', 'resource_monitor.log')
ERR_PATH = os.path.join('.tmp', 'resource_monitor.err')
PID_PATH = os.path.join('.tmp', 'resource_monitor_pid.txt')

CPU_THRESHOLD = 90.0
MEM_THRESHOLD = 90.0
SAMPLE_INTERVAL = 10


def log(msg: str):
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_PATH, 'a', encoding='utf8') as f:
        f.write(f'[{ts}] {msg}\n')


def send_telegram(message: str):
    try:
        # call existing helper; PYTHONPATH set by supervisor/scheduler normally
        subprocess.run([sys.executable, 'scripts/send_simple_telegram.py', message], check=False)
        log(f'Telegram notified: {message}')
    except Exception as e:
        log(f'Failed to send telegram: {e}')


def main():
    try:
        import psutil
    except Exception as e:
        with open(ERR_PATH, 'a', encoding='utf8') as ef:
            ef.write(f'[{datetime.utcnow().isoformat()}] psutil import failed: {e}\n')
        print('psutil not available; install with: pip install psutil', file=sys.stderr)
        return 2

    os.makedirs('.tmp', exist_ok=True)
    # write PID
    with open(PID_PATH, 'w', encoding='ascii') as f:
        f.write(str(os.getpid()))

    log('Resource monitor started')

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            vm = psutil.virtual_memory()
            mem = vm.percent
            log(f'cpu={cpu:.1f}% mem={mem:.1f}%')

            if cpu >= CPU_THRESHOLD:
                msg = f'ALERT: CPU at {cpu:.0f}% (threshold {CPU_THRESHOLD}%).'
                send_telegram(msg)

            if mem >= MEM_THRESHOLD:
                msg = f'ALERT: Memory at {mem:.0f}% (threshold {MEM_THRESHOLD}%).'
                send_telegram(msg)

            time.sleep(SAMPLE_INTERVAL)
    except KeyboardInterrupt:
        log('Resource monitor stopped by KeyboardInterrupt')
    except Exception as e:
        log(f'Unhandled error in resource monitor: {e}')
    finally:
        try:
            os.remove(PID_PATH)
        except Exception:
            pass


if __name__ == '__main__':
    sys.exit(main())
