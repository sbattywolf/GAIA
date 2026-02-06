#!/usr/bin/env python3
"""Run pytest with repo root on sys.path to ensure local packages import.

Usage: python scripts/run_tests.py
"""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import pytest

if __name__ == '__main__':
    raise SystemExit(pytest.main(['-q']))
