#!/usr/bin/env python3
"""Minimal Gise.0.3 worker scaffold for STR_TestGise.part1 smoke tests.

Responsibilities:
- Load `.tmp/telegram.env` safely (dry-run mode available)
- Provide a `smoke_check()` that verifies essential environment and file access
- Offer a CLI with `--dry-run` and `--smoke` flags

This is intentionally small and safe — expand with agent behavior later.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent


def load_env(env_path: Path) -> dict:
    env = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()
    return env


def smoke_check(dry_run: bool = True) -> int:
    from scripts.env_utils import preferred_env_path
    env_file = preferred_env_path(ROOT)
    print('Smoke check: env file ->', env_file)
    if not env_file.exists():
        print('  WARNING: env file not found (expected for dry-run)')
        return 1 if not dry_run else 0
    try:
        data = load_env(env_file)
        print('  Found entries:', len(data))
        sample_keys = list(data.keys())[:5]
        print('  Sample keys:', sample_keys)
        return 0
    except Exception as e:
        print('  ERROR reading env file:', e)
        return 2


def export_chat_history(output_dir: Path | str = None, limit: int = 200) -> Path | None:
    """Export recent events from `events.ndjson` to `.tmp/exports`.

    Returns path to exported file or None on error.
    """
    try:
        out_base = Path(output_dir) if output_dir else ROOT / '.tmp' / 'exports'
        out_base.mkdir(parents=True, exist_ok=True)
        src = ROOT / 'events.ndjson'
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        dest = out_base / f'events_export_{ts}.ndjson'
        if not src.exists():
            # create empty file with a header note
            dest.write_text(f'# export generated at {ts} — source events.ndjson not found\n', encoding='utf-8')
            return dest

        # Read last `limit` lines efficiently
        with src.open('rb') as f:
            try:
                f.seek(0, os.SEEK_END)
                end = f.tell()
                size = 1024
                data = b''
                while end > 0 and data.count(b'\n') <= limit:
                    read_bytes = min(size, end)
                    f.seek(end - read_bytes)
                    chunk = f.read(read_bytes)
                    data = chunk + data
                    end -= read_bytes
                    if end == 0:
                        break
                lines = data.splitlines()[-limit:]
                # write out as text
                dest.write_text('\n'.join(x.decode('utf-8', errors='ignore') for x in lines) + '\n', encoding='utf-8')
                return dest
            except Exception:
                # fallback: simple read
                text = src.read_text(encoding='utf-8', errors='ignore')
                out = '\n'.join(text.splitlines()[-limit:]) + '\n'
                dest.write_text(out, encoding='utf-8')
                return dest
    except Exception as e:
        print('export_chat_history failed:', e)
        return None


def env_checks_report(env_path: Path | None = None) -> dict:
    """Run a set of environment and file access checks and return a report dict.

    The report contains pass/fail counts and sample values (tokens redacted).
    """
    from scripts.env_utils import preferred_env_path
    env_file = Path(env_path) if env_path else preferred_env_path(ROOT)
    report = {'env_file_exists': env_file.exists(), 'entries': {}, 'redacted': []}
    if env_file.exists():
        data = load_env(env_file)
        for k, v in data.items():
            if 'TOKEN' in k.upper() or 'SECRET' in k.upper():
                report['entries'][k] = '<redacted>'
                report['redacted'].append(k)
            else:
                report['entries'][k] = v
    # check write access to .tmp/exports
    try:
        export_dir = ROOT / '.tmp' / 'exports'
        export_dir.mkdir(parents=True, exist_ok=True)
        test_path = export_dir / '._gise_write_test'
        test_path.write_text('ok', encoding='utf-8')
        test_path.unlink()
        report['can_write_exports'] = True
    except Exception:
        report['can_write_exports'] = False
    return report


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--smoke', action='store_true')
    args = p.parse_args()

    if args.smoke:
        rc = smoke_check(dry_run=args.dry_run)
        print('smoke rc=', rc)
        raise SystemExit(rc)

    print('Gise.0.3 worker scaffold. Use --smoke to run environment checks.')


if __name__ == '__main__':
    main()
