#!/usr/bin/env python3
"""Periodic runner: runs `scripts/gaia_run_tests.py` on a schedule and notifies via Telegram.

Environment:
- TELEGRAM_BOT_TOKEN, CHAT_ID optional (falls back to env used by gaia.alerts)

Usage:
  python scripts/gaia_periodic_runner.py --interval 3600
"""
import subprocess
import time
import datetime
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp'
TMP.mkdir(exist_ok=True)
REPORT_DIR = TMP / 'reports'
REPORT_DIR.mkdir(exist_ok=True)

from gaia import alerts


def run_tests():
    cmd = [str(Path('python')), '-m', 'scripts.gaia_run_tests'] if False else ['python', str(ROOT / 'scripts' / 'gaia_run_tests.py')]
    start = datetime.datetime.utcnow()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        rc = proc.returncode
        out = proc.stdout + '\n' + proc.stderr
    except Exception as e:
        rc = 255
        out = str(e)
    end = datetime.datetime.utcnow()
    stamp = start.isoformat() + 'Z'
    report = {'start': stamp, 'end': end.isoformat() + 'Z', 'rc': rc, 'output_preview': out[:4000]}
    path = REPORT_DIR / (datetime.datetime.utcnow().strftime('report_%Y%m%dT%H%M%SZ.json'))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    return report, path


def notify(report):
    summary = f"GAIA periodic run: rc={report['rc']}, start={report['start']}, end={report['end']}"
    try:
        alerts.send_telegram(message=summary)
    except Exception:
        pass


def main(interval=3600):
    print('Starting periodic runner, interval', interval)
    while True:
        report, path = run_tests()
        notify(report)
        time.sleep(interval)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--interval', type=int, default=3600)
    args = p.parse_args()
    main(interval=args.interval)
