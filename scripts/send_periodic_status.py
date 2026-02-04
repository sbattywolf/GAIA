#!/usr/bin/env python3
"""Send periodic todo status updates to Telegram.

Sends a short summary every N minutes (default 5) for a duration (default 8 hours).
Writes local status notes to `.tmp/gise_status/` and uses `.tmp/telegram.env` for credentials.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests
import difflib

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


PRIO_ORDER = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}


def parse_epic_tasks(epic_file: Path) -> list[dict]:
    try:
        data = json.loads(epic_file.read_text(encoding='utf-8'))
    except Exception:
        return []
    tasks = []
    for feat in data.get('features', []):
        fname = feat.get('id')
        for story in feat.get('stories', []):
            sk = story.get('story_key') or story.get('story_key')
            for t in story.get('tasks', []):
                tasks.append({
                    'feature': fname,
                    'story': sk,
                    'id': t.get('id'),
                    'title': t.get('title'),
                    'status': t.get('status', 'todo'),
                    'priority': t.get('priority', 'medium')
                })
    return tasks


def top_n_tasks(tasks: list[dict], n: int = 6) -> list[dict]:
    # filter todo
    todo = [t for t in tasks if t.get('status') in (None, 'todo')]
    # sort by priority then id
    todo.sort(key=lambda x: (PRIO_ORDER.get(x.get('priority', 'medium'), 2), x.get('feature') or '', x.get('id') or ''))
    return todo[:n]


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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--duration-hours', type=float, default=8.0)
    p.add_argument('--interval-minutes', type=int, default=10)
    p.add_argument('--diff-only', action='store_true', help='send only lines added since last message')
    p.add_argument('--once', action='store_true', help='run a single iteration and exit')
    p.add_argument('--top-n', type=int, default=6)
    args = p.parse_args()

    from scripts.env_utils import load_preferred_env
    env = load_preferred_env(ROOT)
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')

    epic_file = ROOT / 'doc' / 'EPC_Telegram.current'
    start = datetime.utcnow()
    end = start + timedelta(hours=args.duration_hours)

    note_dir = ROOT / '.tmp' / 'gise_status'
    note_dir.mkdir(parents=True, exist_ok=True)

    while datetime.utcnow() < end:
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        val = run_validator()
        tasks = parse_epic_tasks(epic_file)
        top = top_n_tasks(tasks, n=args.top_n)
        lines = [f'GAIA periodic status {ts}', f'Todo count: {len([t for t in tasks if t.get("status") in (None, "todo")])}']
        lines.append('Validator:')
        if isinstance(val, list):
            lines.extend(val)
        else:
            lines.append(str(val))
        lines.append('Top tasks:')
        for t in top:
            lines.append(f"- {t.get('id')} ({t.get('priority')}): {t.get('title')}")
        msg = '\n'.join(lines)
        # write local note
        (note_dir / f'status_{ts}.txt').write_text(msg, encoding='utf-8')

        # avoid sending duplicate messages — compare with last sent content
        last_path = note_dir / 'last_sent.txt'
        last_msg = None
        if last_path.exists():
            try:
                last_msg = last_path.read_text(encoding='utf-8')
            except Exception:
                last_msg = None

        sent = False
        # choose whether to send full message or only diffs
        if msg != last_msg:
            send_text = msg
            if args.diff_only and last_msg:
                # compute added lines using ndiff
                try:
                        old_lines = last_msg.splitlines()
                    new_lines = msg.splitlines()
                    diffs = list(difflib.ndiff(old_lines, new_lines))
                    added = [d[2:] for d in diffs if d.startswith('+ ')]
                    if not added:
                        print(f'[{ts}] no new lines to send; skipping')
                        # still update last_sent
                        try:
                            last_path.write_text(msg, encoding='utf-8')
                        except Exception:
                            pass
                        if args.once:
                            break
                        time.sleep(args.interval_minutes * 60)
                        continue
                    send_text = '\n'.join([f'GAIA updates {ts} (diff-only)'] + added)
                except Exception:
                    send_text = msg

            if token and chat:
                sent = send_telegram(token, chat, send_text)
            # update last sent regardless
            try:
                last_path.write_text(msg, encoding='utf-8')
            except Exception:
                pass
        else:
            print(f'[{ts}] duplicate message detected; skipping send')

        print(f'[{ts}] sent={sent} todo_count={len(tasks)}')
        time.sleep(args.interval_minutes * 60)
        if args.once:
            break


if __name__ == '__main__':
    main()
