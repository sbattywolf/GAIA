#!/usr/bin/env python3
"""Fetch GitHub App installation ID for a repo and optionally update consumers.json.

Usage (dry-run):
  GH_API_TOKEN=<token> python scripts/fetch_installation_id.py --repo owner/repo

To write changes:
  GH_API_TOKEN=<token> python scripts/fetch_installation_id.py --repo owner/repo --confirm

The script queries `GET /repos/{owner}/{repo}/installation` which returns the
installation `id`. It will replace any placeholder installation IDs in
`rotation/consumers.json` (values containing '<INSTALLATION_ID') with the
fetched id.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import os
import requests

ROOT = Path(__file__).resolve().parents[1]
CONSUMERS = ROOT / 'rotation' / 'consumers.json'


def get_installation_id(repo: str, token: str) -> int:
    owner, name = repo.split('/', 1)
    url = f'https://api.github.com/repos/{owner}/{name}/installation'
    headers = {'Accept': 'application/vnd.github+json', 'Authorization': f'token {token}'}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()
    return int(data['id'])


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True, help='owner/repo to query installation id for')
    p.add_argument('--config', default=str(CONSUMERS), help='Path to consumers.json')
    p.add_argument('--confirm', action='store_true', help='Write changes to config')
    args = p.parse_args(argv)

    token = os.environ.get('GH_API_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:
        raise SystemExit('GH_API_TOKEN or GITHUB_TOKEN required in environment')

    print('Fetching installation id for', args.repo)
    inst_id = get_installation_id(args.repo, token)
    print('Installation id:', inst_id)

    cfg_path = Path(args.config)
    if not cfg_path.exists():
        raise SystemExit('consumers config not found: ' + str(cfg_path))
    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
    updated = False
    for name, meta in cfg.get('consumers', {}).items():
        v = str(meta.get('installation_id', ''))
        if '<INSTALLATION_ID' in v or v.strip() == '' or v.startswith('<'):
            print('  updating', name, '->', inst_id)
            meta['installation_id'] = str(inst_id)
            updated = True

    out_map = {'repo': args.repo, 'installation_id': str(inst_id), 'updated': updated}
    outp = ROOT / 'rotation' / 'installation_id_fill.json'
    outp.write_text(json.dumps(out_map, indent=2), encoding='utf-8')
    print('Wrote', outp)

    if updated and args.confirm:
        cfg_path.write_text(json.dumps(cfg, indent=2), encoding='utf-8')
        print('Wrote updated consumers config:', cfg_path)
    elif updated:
        print('Dry-run: run with --confirm to write changes to', cfg_path)


if __name__ == '__main__':
    main()
