"""Standalone rotation test (does not import approval_listener).

This writes many lines to `.tmp/approval_debug.log` and performs size-based
rotation keeping .1,.2,.3 backups. Use for validating rotation even if
`approval_listener.py` is temporarily corrupted.
"""
import os
import json
import time
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG = os.path.join(ROOT, '.tmp', 'approval_debug.log')
ROTATE_BYTES = 1024  # small for test


def log_debug(line, rotate_bytes=ROTATE_BYTES):
    p = Path(LOG)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        if p.exists() and p.stat().st_size > int(rotate_bytes):
            for i in (3, 2):
                src = str(p) + f'.{i-1}'
                dst = str(p) + f'.{i}'
                if os.path.exists(src):
                    try:
                        if os.path.exists(dst):
                            os.remove(dst)
                    except Exception:
                        pass
                    try:
                        os.replace(src, dst)
                    except Exception:
                        pass
            try:
                first = str(p) + '.1'
                if os.path.exists(first):
                    os.remove(first)
            except Exception:
                pass
            try:
                os.replace(str(p), str(p) + '.1')
            except Exception:
                pass
    except Exception:
        pass
    with p.open('a', encoding='utf-8') as f:
        f.write(line + '\n')


def main():
    print('Log path:', LOG)
    for i in range(300):
        log_debug(f'test_entry {i}')
        if i % 50 == 0:
            print('wrote', i)
        time.sleep(0.002)

    files = sorted([f for f in os.listdir(os.path.join(ROOT, '.tmp')) if f.startswith('approval_debug.log')])
    for f in files:
        p = os.path.join(ROOT, '.tmp', f)
        print(f, os.path.getsize(p))
    print('done')


if __name__ == '__main__':
    main()
