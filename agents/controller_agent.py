"""Local controller agent that coordinates agents, interfaces, and schedulers.

This controller watches active tasks, assigns todos to local workers,
keeps a short active-tool list per agent, and can notify via Telegram or
the monitor UI. It's lightweight and intended for local orchestration.

Usage:
    python agents/controller_agent.py --once --simulate
    python agents/controller_agent.py --poll 5
"""
from pathlib import Path
import time
import argparse
import json
import threading
import os
from scripts import sequence_manager as sm
from agents import sequence_worker as sw
from scripts import telegram_client as tc


class ControllerAgent:
    def __init__(self, simulate=True):
        self.simulate = simulate
        self.active_file = sm.ACTIVE_FILE
        self.running = False

    def scan_active(self):
        if not self.active_file.exists():
            return None
        try:
            return json.loads(self.active_file.read_text(encoding='utf-8'))
        except Exception:
            return None

    def list_open_todos(self, seq_id):
        todos = sm._load_todos()
        open_items = [v for k, v in todos.items() if v.get('seq_id') == seq_id and v.get('status') != 'done']
        # sort by id
        open_items.sort(key=lambda x: x.get('id'))
        return open_items

    def assign_and_run_one(self):
        active = self.scan_active()
        if not active:
            print('No active sequence to manage.')
            return False
        seq_id = active.get('active_sequence')
        open_items = self.list_open_todos(seq_id)
        if not open_items:
            print('No open todos; attempting finalize.')
            sm._maybe_finish_sequence(seq_id)
            return True
        # pick first todo
        t = open_items[0]
        tid = t.get('id')
        title = t.get('title')
        print(f"Assigning todo {tid}: {title}")
        # notify via Telegram if configured and not sim
        token, chat = self._load_telegram_env()
        if token and chat and not self.simulate:
            try:
                tc.send_message(token, chat, f"Controller assigned: {tid} — {title}")
            except Exception:
                pass
        # simulate processing by marking done
        if ':' in tid and tid.count(':') >= 2:
            parts = tid.split(':')
            seq, si, sj = parts[0], int(parts[1]), int(parts[2])
            sm._mark_todo_done(seq, si, sj)
        else:
            parts = tid.split(':')
            seq, si = parts[0], int(parts[1])
            sm._mark_todo_done(seq, si, None)
        # after processing, attempt finish
        sm._maybe_finish_sequence(seq_id)
        return True

    def run_once(self):
        return self.assign_and_run_one()

    def run_poll(self, poll_seconds=5):
        self.running = True
        try:
            while self.running:
                progressed = self.assign_and_run_one()
                time.sleep(poll_seconds)
        except KeyboardInterrupt:
            self.running = False

    def _load_telegram_env(self):
        # read .tmp/telegram.env if present
        p = Path('.tmp/telegram.env')
        if not p.exists():
            return (None, None)
        env = {}
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
        return (env.get('TELEGRAM_BOT_TOKEN'), env.get('CHAT_ID'))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--once', action='store_true')
    p.add_argument('--poll', type=int, default=0)
    p.add_argument('--simulate', action='store_true')
    args = p.parse_args()
    ctrl = ControllerAgent(simulate=args.simulate)
    if args.once or args.poll <= 0:
        ctrl.run_once()
    else:
        ctrl.run_poll(args.poll)


if __name__ == '__main__':
    main()
