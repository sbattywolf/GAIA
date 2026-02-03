import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / '.tmp' / 'metrics.json'

_counters = {}


def _ensure_dir():
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)


def _save():
    try:
        _ensure_dir()
        METRICS_FILE.write_text(json.dumps(_counters, indent=2), encoding='utf-8')
    except Exception:
        pass


def increment(key: str, n: int = 1):
    try:
        _counters[key] = _counters.get(key, 0) + int(n)
        _save()
    except Exception:
        pass


def get(key: str):
    return _counters.get(key, 0)


def dump():
    return dict(_counters)
