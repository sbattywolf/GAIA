"""Event helper to append NDJSON events to `events.ndjson`."""
import json
import os
import datetime
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')


def now():
    # Human-local timestamp (no UTC Z) for easier reading
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def append_event(evt: dict):
    if 'timestamp' not in evt:
        evt['timestamp'] = now()
    try:
        with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, default=str) + '\n')
    except Exception:
        # best-effort; do not raise
        pass

    # Also write a concise one-line summary to .tmp/last_messages.log
    try:
        tmpdir = Path(os.path.join(ROOT, '.tmp'))
        tmpdir.mkdir(parents=True, exist_ok=True)
        short_log = tmpdir / 'last_messages.log'
        t = evt.get('timestamp')
        etype = evt.get('type', 'event')
        payload = evt.get('payload') or evt
        try:
            payload_preview = json.dumps(payload, ensure_ascii=False, default=str)
        except Exception:
            payload_preview = str(payload)
        # single-line, truncated
        payload_preview = payload_preview.replace('\n', ' ')[:200]
        line = f"[{t}] {etype}: {payload_preview}\n"
        with open(short_log, 'a', encoding='utf-8') as s:
            s.write(line)
    except Exception:
        pass


def make_event(event_type: str, payload: dict):
    evt = {'type': event_type, 'payload': payload, 'timestamp': now()}
    append_event(evt)
    return evt
