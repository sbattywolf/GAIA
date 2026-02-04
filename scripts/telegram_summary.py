#!/usr/bin/env python3
"""Send a compact, human-friendly task summary to Telegram (or print).

Reads `tasks/todo.json` in the repo root and posts a short message.
Environment variables (optional): TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import textwrap

try:
    import requests
except Exception:
    requests = None


def load_tasks(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def make_message(tasks: list[dict]) -> str:
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    in_progress = [t for t in tasks if t.get("status") == "in-progress"]
    pending = [t for t in tasks if t.get("status") != "completed"]

    lines = []
    lines.append(f"GAIA status — {completed}/{total} completed, {len(pending)} pending")
    if in_progress:
        ip = ", ".join(t.get("title") for t in in_progress)
        lines.append(f"In-progress: {ip}")

    lines.append("")
    lines.append("Top pending:")
    for i, t in enumerate(pending[:6], start=1):
        title = t.get("title")
        desc = t.get("description", "").strip().replace("\n", " ")
        desc = textwrap.shorten(desc, 140)
        lines.append(f"{i}. {title} — {desc}")

    lines.append("")
    ts = datetime.now(timezone.utc).astimezone().isoformat()
    lines.append(f"Updated: {ts}")
    return "\n".join(lines)


def send_telegram(token: str, chat_id: str, text: str) -> bool:
    if requests is None:
        print("requests not available; cannot send Telegram message")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": chat_id, "text": text})
        resp.raise_for_status()
        return True
    except Exception as exc:
        print("Telegram send failed:", exc)
        return False


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    tasks_file = repo_root / "tasks" / "todo.json"
    tasks = load_tasks(tasks_file)
    msg = make_message(tasks)

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if token and chat_id:
        ok = send_telegram(token, chat_id, msg)
        if ok:
            print("Sent Telegram summary")
            return 0
        else:
            print(msg)
            return 0
    else:
        # No secrets configured — print summary to stdout instead of failing
        print(msg)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Send a short Telegram summary of EPC_Telegram.current counts.

Uses `gaia.alerts.send_telegram` to send a message describing features/stories/tasks (done/pending).
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
EPIC = ROOT / 'doc' / 'EPC_Telegram.current'

def parse_epic(epic_file: Path):
    try:
        data = json.loads(epic_file.read_text(encoding='utf-8'))
    except Exception:
        return None
    stats = {'features': 0, 'stories': 0, 'tasks_total': 0, 'tasks_done': 0, 'tasks_todo': 0}
    features = data.get('features', [])
    stats['features'] = len(features)
    for f in features:
        for s in f.get('stories', []):
            stats['stories'] += 1
            for t in s.get('tasks', []):
                stats['tasks_total'] += 1
                if t.get('status') in ('done', 'completed'):
                    stats['tasks_done'] += 1
                else:
                    stats['tasks_todo'] += 1
    return stats

def build_message(stats):
    if not stats:
        return 'Failed to load epic summary.'
    return (f"GAIA Telegram summary:\nFeatures: {stats['features']}\nStories: {stats['stories']}\n"
            f"Tasks done: {stats['tasks_done']} / {stats['tasks_total']}\nPending: {stats['tasks_todo']}")

def load_env(path: Path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k,v = line.split('=',1)
            env[k.strip()] = v.strip()
    return env

def main():
    from scripts.env_utils import load_preferred_env
    env = load_preferred_env(ROOT)
    token = env.get('TELEGRAM_BOT_TOKEN') or ''
    chat = env.get('CHAT_ID') or ''
    stats = parse_epic(EPIC)
    msg = build_message(stats)
    if not token or not chat:
        print('Missing token or chat_id in .tmp/telegram.env; summary:')
        print(msg)
        sys.exit(1)
    # import here to avoid heavy deps on module import path
    try:
        from gaia.alerts import send_telegram
        resp = send_telegram(chat_id=chat, message=msg, token=token)
        print('Sent:', resp)
    except Exception as e:
        print('Failed to send via gaia.alerts:', e)

if __name__ == '__main__':
    main()
