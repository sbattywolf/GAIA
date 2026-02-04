#!/usr/bin/env python3
"""Check staged files for accidental `.private` or `.tmp` env files.

Usage: invoked from a git pre-commit hook.
Exits with 0 when safe, 1 when disallowed files are staged.
"""
import subprocess
import sys
import re


def get_staged_files():
    p = subprocess.run(['git', 'diff', '--name-only', '--cached'], capture_output=True, text=True)
    if p.returncode != 0:
        return []
    return [l.strip() for l in p.stdout.splitlines() if l.strip()]


DISALLOWED_PATTERNS = [
    re.compile(r'^\.private(/|$)'),
    re.compile(r'^\.tmp/.*telegram.*'),
    re.compile(r'.*telegram\.env$'),
]


def main():
    bad = []
    for f in get_staged_files():
        for pat in DISALLOWED_PATTERNS:
            if pat.search(f):
                bad.append(f)
                break

    if bad:
        print('Commit blocked: staged files appear to contain environment secrets:')
        for b in bad:
            print('  ', b)
        print('\nMove secrets to `.private/` (ignored) and do not commit `.private` or `.tmp` env files.')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
