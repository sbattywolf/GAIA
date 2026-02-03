"""Local agent harness for dry-run simulation of agents.

Usage:
  python scripts/agent_harness.py --name Alby --once
  python scripts/agent_harness.py --name Gise --loop --interval 2

The harness is safe by default: it only writes events to `events.ndjson` and
can optionally append pending commands for testing approval flows.
"""
import argparse
import json
import time
import uuid
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / 'events.ndjson'
PENDING = ROOT / '.tmp' / 'pending_commands.json'


def append_event(evt: dict):
    evt['timestamp'] = evt.get('timestamp') or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    try:
        EVENTS.parent.mkdir(parents=True, exist_ok=True)
        with open(EVENTS, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, ensure_ascii=False) + '\n')
    except Exception:
        pass


def enqueue_pending(cmd_text: str, creator='harness'):
    item = {
        'id': str(uuid.uuid4()),
        'chat_id': 'harness_chat',
        'message_id': str(int(time.time() * 1000)),
        'command': cmd_text,
        'from': {'first_name': creator},
        'status': 'pending',
        'created': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    PENDING.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(PENDING.read_text(encoding='utf-8')) if PENDING.exists() else []
    except Exception:
        data = []
    data.append(item)
    PENDING.write_text(json.dumps(data, indent=2), encoding='utf-8')
    append_event({'type': 'command.enqueued', 'payload': {'id': item['id'], 'command_preview': cmd_text[:120]}})
    return item


def run_once(name: str, make_pending: bool = False):
    append_event({'type': 'agent.heartbeat', 'payload': {'agent': name}})
    if make_pending:
        item = enqueue_pending(f'echo "hello from {name}"', creator=name)
        print('enqueued', item['id'])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', default='Alby')
    p.add_argument('--loop', action='store_true')
    p.add_argument('--once', action='store_true')
    p.add_argument('--interval', type=float, default=5.0)
    p.add_argument('--pending', action='store_true', help='also enqueue a pending command for approval testing')
    args = p.parse_args()

    if args.once:
        run_once(args.name, make_pending=args.pending)
        return 0

    try:
        while True:
            run_once(args.name, make_pending=args.pending)
            time.sleep(max(0.5, args.interval))
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
