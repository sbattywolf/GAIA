#!/usr/bin/env python3
"""Validate required secrets for GAIA Telegram workflows.

Checks environment variables and optional .private/.env file for required keys.
Exits with non-zero status if any required secret is missing and prints guidance.
"""
import os
import sys
from pathlib import Path

REQ = [
    ("TELEGRAM_BOT_TOKEN", "Telegram bot token (create a bot via BotFather)"),
    ("TELEGRAM_CHAT_ID", "Telegram chat id (get via @userinfobot or by sending a message to the bot and reading updates)"),
]

# Try loading .private/.env if present
env_file = Path(".private/.env")
if not env_file.exists():
    env_file = Path(".tmp/telegram.env")

if env_file.exists():
    with env_file.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())

missing = []
for key, hint in REQ:
    val = os.environ.get(key)
    if not val:
        missing.append((key, hint))

if not missing:
    print("All required secrets present:")
    for key, _ in REQ:
        print(f" - {key}")
    sys.exit(0)

print("Missing required secrets:")
for key, hint in missing:
    print(f" - {key}: {hint}")

print()
print("Guidance to obtain the missing items:")
for key, hint in missing:
    if key == "TELEGRAM_BOT_TOKEN":
        print("\nTELEGRAM_BOT_TOKEN (create a bot):")
        print("  1) In Telegram, message @BotFather and run /newbot.")
        print("  2) Follow prompts to set a name and username; BotFather will return a token like 12345:ABC...\n")
    elif key == "TELEGRAM_CHAT_ID":
        print("\nTELEGRAM_CHAT_ID (obtain a chat id):")
        print("  Option A (individual): Add and message @userinfobot in Telegram to get your numeric id.")
        print("  Option B (group): Add your bot to a group, send a message, then call the getUpdates API or use the mock server to read the chat id from updates.")

print()
print("After you have the values, you can either:")
print(" - export them to your shell and re-run this script, e.g. (bash):\n    export TELEGRAM_BOT_TOKEN=...\n    export TELEGRAM_CHAT_ID=...\n    python scripts/validate_secrets.py")
print(" - or create .private/.env with lines:\n    TELEGRAM_BOT_TOKEN=...\n    TELEGRAM_CHAT_ID=...")

sys.exit(2)
