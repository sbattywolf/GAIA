#!/usr/bin/env python3
"""Inventory tokens and secret usages across the repository.

Produces:
- rotation/inventory.json
- rotation/inventory.csv

Searches for common token names and secret access patterns.
"""
from __future__ import annotations
import re
import json
import csv
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'rotation'
OUT_DIR.mkdir(exist_ok=True)

PATTERNS = [
    r'GITHUB_TOKEN',
    r'GAIA_GITHUB_TOKEN',
    r'AUTOMATION_GITHUB_TOKEN',
    r'gh secret set',
    r'secrets\.',
    r"\$\{\{\s*secrets\.",
    r"SecretsManager",
    r"get\(['\"]?[A-Z0-9_]+['\"]?\)",
    r'GHA_TOKEN',
    r'PAT',
    r'installations',
]

IGNORE_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', 'rotation', '.private'}


def scan_file(path: Path):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return []
    hits = []
    for patt in PATTERNS:
        for m in re.finditer(patt, text, flags=re.IGNORECASE):
            line_no = text.count('\n', 0, m.start()) + 1
            snippet = text.splitlines()[line_no-1].strip() if line_no-1 < len(text.splitlines()) else ''
            hits.append({'pattern': patt, 'line': line_no, 'snippet': snippet})
    return hits


def walk_and_scan(root: Path):
    results = []
    for p in root.rglob('*'):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        if p.is_file():
            rel = p.relative_to(root)
            hits = scan_file(p)
            if hits:
                results.append({'path': str(rel).replace('\\','/'), 'matches': hits})
    return results


def scan_workflows(root: Path):
    wf_dir = root / '.github' / 'workflows'
    entries = []
    if not wf_dir.exists():
        return entries
    for f in wf_dir.glob('*.y*ml'):
        text = f.read_text(encoding='utf-8', errors='ignore')
        # find secrets usage
        for m in re.finditer(r"secrets\.[A-Z0-9_]+", text, flags=re.IGNORECASE):
            entries.append({'workflow': str(f.relative_to(root)).replace('\\','/'), 'usage': m.group(0)})
        for m in re.finditer(r"\$\{\{\s*secrets\.([A-Z0-9_]+)\s*\}\}", text, flags=re.IGNORECASE):
            entries.append({'workflow': str(f.relative_to(root)).replace('\\','/'), 'usage': m.group(1)})
    return entries


def main():
    print('Scanning repository for token and secret usage...')
    results = walk_and_scan(ROOT)
    workflows = scan_workflows(ROOT)

    out = {'repo': str(ROOT), 'findings': results, 'workflows': workflows}
    jpath = OUT_DIR / 'inventory.json'
    with jpath.open('w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    # also CSV: path, pattern, line, snippet
    cpath = OUT_DIR / 'inventory.csv'
    with cpath.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['path', 'pattern', 'line', 'snippet'])
        for item in results:
            for m in item['matches']:
                w.writerow([item['path'], m['pattern'], m['line'], m['snippet']])

    print('Wrote', jpath, 'and', cpath)


if __name__ == '__main__':
    main()
