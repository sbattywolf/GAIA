#!/usr/bin/env python3
"""Generate rotation/permissions.csv from rotation/inventory.json

This script applies conservative heuristics to recommend minimal GitHub App
permissions per consumer found in the inventory.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENT = ROOT / 'rotation' / 'inventory.json'
OUT = ROOT / 'rotation' / 'permissions.csv'

DEFAULT = 'contents:read'

def recommend(path: str, usages) -> (str, str):
    p = path.lower()
    notes = []
    perms = set()
    if 'publish' in p or 'issues' in p or 'publish_issues' in p:
        perms.add('issues:write')
        notes.append('issue publisher')
    if 'token_cache' in p or 'token-cache' in p or 'token_cache_server' in p or 'token_cache.py' in p:
        perms.update(['contents:read', 'issues:write'])
        notes.append('token-cache returns install tokens for agents; needs union of consumers')
    if 'github_app_token' in p or 'github-app-token' in p:
        perms.add('metadata:read')
        notes.append('creates JWT and exchanges for installation token')
    if p.startswith('.github/workflows') or 'workflows' in p:
        # inspect usages
        for u in usages:
            usage = u.get('usage','') if isinstance(u, dict) else str(u)
            if 'secrets.' in usage and 'gaia' in usage.lower():
                perms.add('use GAIA_GITHUB_TOKEN')
                notes.append('workflow reads GAIA_GITHUB_TOKEN')
            elif 'secrets.' in usage:
                perms.add('use repo secrets')
                notes.append('workflow reads repo secrets')
    if 'rotate_tokens_helper' in p or 'rotate' in p:
        perms.add('secrets:write')
        notes.append('persists tokens to encrypted store')
    if 'agents/' in p or '/agents' in p:
        perms.update(['contents:read'])
        notes.append('agent script, default read access')

    if not perms:
        perms.add(DEFAULT)
        notes.append('default conservative read-only')

    return ','.join(sorted(perms)), '; '.join(notes)


def main():
    data = json.loads(INVENT.read_text(encoding='utf-8'))
    findings = data.get('findings', [])
    # Build a mapping for workflows from data
    wf_usages = {}
    for w in data.get('workflows', []):
        wf = w.get('workflow')
        if wf not in wf_usages:
            wf_usages[wf] = []
        wf_usages[wf].append(w)

    rows = []
    for item in findings:
        path = item.get('path')
        usages = []
        if path.startswith('.github/workflows/'):
            usages = wf_usages.get(path, [])
        perms, note = recommend(path, usages)
        rows.append((path, perms, note))

    # also include known scripts if not found
    extra = [
        ('scripts/github_app_token.py','metadata:read','token exchange helper'),
        ('scripts/publish_issues.py','issues:write','issue publisher helper'),
        ('scripts/token_cache_server.py','contents:read,issues:write','token-cache server'),
        ('gaia/token_cache.py','contents:read,issues:write','token cache logic'),
    ]
    for e in extra:
        if not any(r[0]==e[0] for r in rows):
            rows.append(e)

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open('w', encoding='utf-8') as f:
        f.write('path,recommended_permissions,notes\n')
        for r in rows:
            # simple CSV escaping
            line = '"%s","%s","%s"\n' % (r[0].replace('"','""'), r[1].replace('"','""'), r[2].replace('"','""'))
            f.write(line)

    print('Wrote', OUT)


if __name__ == '__main__':
    main()
