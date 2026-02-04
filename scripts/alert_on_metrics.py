#!/usr/bin/env python3
"""Read `.tmp/metrics.json` and post alerts to admin chat when thresholds are crossed.

This is a small scaffold: it supports `--dry-run` and a `--threshold` override.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import json
import requests
import os

ROOT = Path(__file__).resolve().parent.parent


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def send_telegram(token: str, chat: str, text: str) -> bool:
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': chat, 'text': text})
        r.raise_for_status()
        return True
    except Exception:
        return False


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--metrics', default=str(ROOT / '.tmp' / 'metrics.json'))
    p.add_argument('--threshold', type=int, default=100)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    mfile = Path(args.metrics)
    if not mfile.exists():
        print('metrics file not found:', mfile)
        return
    data = json.loads(mfile.read_text(encoding='utf-8'))
    # naive check: sum counters
    total = sum(int(v) for v in data.get('counters', {}).values()) if isinstance(data.get('counters'), dict) else 0
    print('metrics total counters:', total)
    if total < args.threshold:
        print('below threshold')
        return

    from scripts.env_utils import load_preferred_env
    env = load_preferred_env(ROOT)
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    msg = f'Alert: metrics total {total} crossed threshold {args.threshold}'
    print(msg)
    if args.dry_run:
        return
    if token and chat:
        ok = send_telegram(token, chat, msg)
        print('alert sent:', ok)
    else:
        print('telegram env missing; cannot send')


if __name__ == '__main__':
    main()
"""Alert script that checks persisted metrics and notifies when thresholds exceeded.

Usage:
  python scripts/alert_on_metrics.py --threshold moved_permanent=1 --threshold retry_errors=10

If `TELEGRAM_BOT_TOKEN` and `TELEGRAM_NOTIFY_CHAT` are set in `.tmp/telegram.env`, the script will attempt to send a Telegram message; otherwise it prints to stdout.
"""
import argparse
import json
from pathlib import Path
import os
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / '.tmp' / 'metrics.json'
from scripts.env_utils import preferred_env_path
ENV_FILE = preferred_env_path(ROOT)


def read_metrics() -> Dict[str, int]:
    try:
        text = METRICS_FILE.read_text(encoding='utf-8')
        return json.loads(text or '{}')
    except Exception:
        return {}


def load_env() -> Dict[str, str]:
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def evaluate(metrics: Dict[str, int], thresholds: Dict[str, int]) -> Tuple[bool, Dict[str, Tuple[int, int]]]:
    """Return (should_alert, details) where details map key->(value, threshold) for exceeded keys."""
    details = {}
    for key, thr in thresholds.items():
        val = int(metrics.get(key, 0))
        if val >= thr:
            details[key] = (val, thr)
    return (len(details) > 0), details


def notify_via_telegram(env: Dict[str, str], text: str) -> bool:
    try:
        token = env.get('TELEGRAM_BOT_TOKEN')
        chat = env.get('TELEGRAM_NOTIFY_CHAT') or env.get('CHAT_ID')
        if not token or not chat:
            return False
        from scripts import telegram_client as tc
        tc.send_message(token, chat, text)
        return True
    except Exception:
        return False


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--threshold', action='append', help='metric=threshold, e.g. telegram.retry.moved_permanent=1')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args(argv)

    # parse thresholds
    th = {}
    if args.threshold:
        for t in args.threshold:
            if '=' in t:
                k, v = t.split('=', 1)
                try:
                    th[k.strip()] = int(v.strip())
                except Exception:
                    pass

    # defaults
    if not th:
        th = {
            'telegram.retry.moved_permanent': 1,
            'telegram.retry.attempt.error': 10,
        }

    metrics = read_metrics()
    ok, details = evaluate(metrics, th)
    if not ok:
        print('No alerts')
        return 0

    # build message
    lines = ['GAIA alert: metrics thresholds exceeded']
    for k, (v, thr) in details.items():
        lines.append(f'- {k}: {v} >= {thr}')
    msg = '\n'.join(lines)

    env = load_env()
    sent = False
    if not args.dry_run:
        sent = notify_via_telegram(env, msg)

    if sent:
        print('Alert sent via Telegram')
    else:
        print(msg)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
