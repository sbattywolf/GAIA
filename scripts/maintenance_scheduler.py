"""Maintenance scheduler: periodically run housekeeping tasks.

Usage:
  python scripts/maintenance_scheduler.py --interval 3600    # run every hour
  python scripts/maintenance_scheduler.py --once             # run once and exit

This script is simple and intended to be run under the existing supervisor or as a scheduled task.
"""
import time
import argparse
import sys
sys.path.insert(0, '.')

from importlib import import_module

parser = argparse.ArgumentParser()
parser.add_argument('--interval', '-i', type=int, default=3600, help='Seconds between runs')
parser.add_argument('--once', action='store_true', help='Run once and exit')
args = parser.parse_args()

# attempt to import tasks
try:
    tcm = import_module('scripts.tg_command_manager')
except Exception:
    tcm = None
try:
    procq = import_module('scripts.process_telegram_queue')
except Exception:
    procq = None

def run_once():
    print('maintenance: running once')
    if tcm:
        try:
            print('maintenance: expire_old')
            tcm.expire_old()
        except Exception as e:
            print('expire_old failed:', e)
    else:
        print('tg_command_manager not importable; skipping expire_old')
    if procq:
        try:
            print('maintenance: process_telegram_queue.run() (if present)')
            # best-effort: call run() or main() if exists
            if hasattr(procq, 'run'):
                procq.run()
            elif hasattr(procq, 'main'):
                procq.main()
            else:
                print('process_telegram_queue has no run/main callable; skipping')
        except Exception as e:
            print('process_telegram_queue failed:', e)
    else:
        print('process_telegram_queue not importable; skipping')

if args.once:
    run_once()
    sys.exit(0)

print('maintenance scheduler starting; interval=', args.interval)
while True:
    run_once()
    time.sleep(args.interval)
