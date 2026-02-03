from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / '.tmp' / 'metrics.json'


def read_metrics():
    try:
        return json.loads(METRICS_FILE.read_text(encoding='utf-8') or '{}')
    except Exception:
        return {}


def main():
    m = read_metrics()
    if not m:
        print('No metrics recorded')
        return 0
    for k, v in sorted(m.items()):
        print(f'{k}: {v}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
