#!/usr/bin/env python3
"""Initialize the local `.private/` env files from workspace envs.

Behavior:
- Creates `.private/` directory if missing and writes `.private/telegram.env`.
- If `.tmp/telegram.env` exists it will be copied into `.private/telegram.env` (without committing).
- If no source env exists, writes a safe template `.private/.env.template` and exits.

Usage:
  python scripts/init_private_env.py [--force]
"""
from pathlib import Path
import shutil
import argparse
import os


ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / '.private'
TMP_ENV = ROOT / '.tmp' / 'telegram.env'
PRIVATE_ENV = PRIVATE / 'telegram.env'


def main(force=False):
    PRIVATE.mkdir(exist_ok=True)
    if PRIVATE_ENV.exists() and not force:
        print(f"{PRIVATE_ENV} already exists; use --force to overwrite")
        return
    if TMP_ENV.exists():
        shutil.copy2(TMP_ENV, PRIVATE_ENV)
        print(f"Copied {TMP_ENV} -> {PRIVATE_ENV}")
        try:
            if os.name == 'posix':
                PRIVATE_ENV.chmod(0o600)
        except Exception:
            pass
        return
    # fallback: write template
    tpl = PRIVATE / '.env.template'
    if not tpl.exists():
        tpl.write_text("TELEGRAM_BOT_TOKEN=\nTELEGRAM_CHAT_ID=\nALLOW_COMMAND_EXECUTION=0\n")
        try:
            if os.name == 'posix':
                tpl.chmod(0o600)
        except Exception:
            pass
    print(f"No workspace env found. Wrote template at {tpl}. Please fill secrets into {PRIVATE_ENV}.")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--force', action='store_true')
    args = p.parse_args()
    main(force=args.force)
