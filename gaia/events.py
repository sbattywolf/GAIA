"""Event helper to append NDJSON events to `events.ndjson`."""
import json
import os
import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EVENTS_FILE = os.path.join(ROOT, 'events.ndjson')


def now():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def append_event(evt: dict):
    if 'timestamp' not in evt:
        evt['timestamp'] = now()
    try:
        with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evt, default=str) + '\n')
    except Exception:
        # best-effort; do not raise
        pass


def make_event(event_type: str, payload: dict):
    evt = {'type': event_type, 'payload': payload, 'timestamp': now()}
    append_event(evt)
    return evt
