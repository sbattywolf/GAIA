#!/usr/bin/env python3
"""Helper to initialize the local SQLite DB used by the orchestrator.

Usage: python scripts/init_db.py
"""
import os
import sys
from orchestrator import init_db, DB_PATH


def main():
    # create containing dir if needed
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    init_db()
    print(f"Initialized DB at {DB_PATH}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Failed to init DB:', e, file=sys.stderr)
        sys.exit(1)
