#!/usr/bin/env python3
"""Send initial plan notification listing features to work on next 20 hours."""
from __future__ import annotations
import json
import os
from pathlib import Path
import requests

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


def assemble_message(epic_file: Path) -> str:
    text = epic_file.read_text(encoding='utf-8')
    try:
        data = json.loads(text)
        features = data.get('features', [])
    except Exception:
        # fallback: best-effort scan for feature ids and names
        features = []
        current = {}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith('"id":') and 'F-' in line:
                # extract id
                try:
                    val = line.split(':', 1)[1].strip().rstrip(',').strip('"')
                    current['id'] = val
                except Exception:
                    continue
            if line.startswith('"name":') and current is not None:
                try:
                    val = line.split(':', 1)[1].strip().rstrip(',').strip('"')
                    current['name'] = val
                except Exception:
                    continue
            # when we have both, append and reset
            if 'id' in current and 'name' in current:
                features.append({'id': current.get('id'), 'name': current.get('name'), 'stories': []})
                current = {}
    lines = [f'Gise plan — next 20 hours ({len(features)} features available):']
    for f in features:
        fid = f.get('id') or f.get('name')
        name = f.get('name')
        # compute story/task counts
        stories = f.get('stories', [])
        s_count = len(stories)
        t_count = sum(len(s.get('tasks', [])) for s in stories)
        lines.append(f'- {fid}: {name} — stories: {s_count}, tasks: {t_count}')
    lines.append('\nPlanned execution: work through `F-helper-gise` (part1→part2), then prioritize high/critical stories: security, command-safety, integration-tests, retryer. I will run validator/tests and small helpers, archive snapshots, update scoring and append progress notes every 10 minutes. No prompts unless a hard failure requires attention.')
    return '\n'.join(lines)


def send_telegram(token: str, chat: str, text: str) -> bool:
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        r = requests.post(url, json={'chat_id': chat, 'text': text})
        r.raise_for_status()
        return True
    except Exception as e:
        # also write failure locally
        (ROOT / '.tmp' / 'gise_status').mkdir(parents=True, exist_ok=True)
        (ROOT / '.tmp' / 'gise_status' / 'send_plan_fail.txt').write_text(str(e), encoding='utf-8')
        return False


def main():
    from scripts.env_utils import load_preferred_env
    env = load_preferred_env(ROOT)
    token = env.get('TELEGRAM_BOT_TOKEN')
    chat = env.get('CHAT_ID')
    epic = ROOT / 'doc' / 'EPC_Telegram.current'
    msg = assemble_message(epic)
    # also write local note
    (ROOT / '.tmp' / 'gise_status').mkdir(parents=True, exist_ok=True)
    (ROOT / '.tmp' / 'gise_status' / 'initial_plan.txt').write_text(msg, encoding='utf-8')
    if token and chat:
        ok = send_telegram(token, chat, msg)
        print('sent=', ok)
    else:
        print('telegram token/chat missing; wrote local plan to .tmp/gise_status/initial_plan.txt')


if __name__ == '__main__':
    main()
