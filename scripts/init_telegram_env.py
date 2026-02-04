#!/usr/bin/env python3
"""Create a starter .tmp/telegram.env file from a template.

Usage:
  python scripts/init_telegram_env.py [--force]

This writes `.tmp/telegram.env` with placeholder values and sets a safe
default for `ALLOW_COMMAND_EXECUTION=0`.
"""
import argparse
import os
from pathlib import Path


TEMPLATE = """
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
ALLOW_COMMAND_EXECUTION=0
"""


def main(force=False):
    tmp = Path(".tmp")
    tmp.mkdir(exist_ok=True)
    out = tmp / "telegram.env"
    if out.exists() and not force:
        print(f"{out} already exists; use --force to overwrite")
        return
    out.write_text(TEMPLATE.lstrip())
    # On POSIX we could chmod 600; on Windows this is best-effort
    try:
        if os.name == "posix":
            out.chmod(0o600)
    except Exception:
        pass
    print(f"Wrote {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = p.parse_args()
    main(force=args.force)
