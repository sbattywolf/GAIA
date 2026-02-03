from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parents[1]
SEEN_PATH = ROOT / '.tmp' / 'telegram_idempotency.json'


def _safe_load():
    try:
        if not SEEN_PATH.exists():
            return {}
        return json.loads(SEEN_PATH.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _safe_save(obj):
    SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = SEEN_PATH.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, indent=2), encoding='utf-8')
    try:
        os.replace(str(tmp), str(SEEN_PATH))
    except Exception:
        pass


def seen_callback(cqid: str) -> bool:
    d = _safe_load()
    seen = d.get('callbacks', [])
    return cqid in seen


def mark_callback(cqid: str):
    d = _safe_load()
    seen = set(d.get('callbacks', []))
    seen.add(cqid)
    d['callbacks'] = sorted(list(seen))
    _safe_save(d)


def clear():
    try:
        if SEEN_PATH.exists():
            SEEN_PATH.unlink()
    except Exception:
        pass
