import os
import sys
import json
import requests

# Ensure repository root is on sys.path so local package imports work when running scripts
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gaia.secrets import SecretsManager


def main():
    sm = SecretsManager()
    try:
        from gaia.env_helpers import get_github_token
        token = os.environ.get('AUTOMATION_GITHUB_TOKEN') or sm.get('AUTOMATION_GITHUB_TOKEN') or get_github_token()
    except Exception:
        token = os.environ.get('AUTOMATION_GITHUB_TOKEN') or sm.get('AUTOMATION_GITHUB_TOKEN')
    if not token:
        print('NO_TOKEN')
        raise SystemExit(1)

    owner = 'sbattywolf'
    repo = 'GAIA'
    api = f'https://api.github.com/repos/{owner}/{repo}/issues'
    created = []

    for fn in sorted(os.listdir('doc/ISSUES')):
        if not fn.lower().endswith('.md'):
            continue
        path = os.path.join('doc/ISSUES', fn)
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        title = None
        for line in content.splitlines():
            if line.startswith('Title:'):
                title = line.split(':', 1)[1].strip()
                break
        if not title:
            title = os.path.splitext(fn)[0]

        payload = {'title': title, 'body': content}
        headers = {'Authorization': f'token {token}', 'User-Agent': 'GAIA-Agent', 'Accept': 'application/vnd.github+json'}
        try:
            r = requests.post(api, headers=headers, json=payload, timeout=30)
            if r.status_code in (200, 201):
                data = r.json()
                url = data.get('html_url')
                print('CREATED:', url)
                created.append(url)
            else:
                print('ERROR', r.status_code, r.text)
        except Exception as e:
            print('EXCEPTION', str(e))

    if created:
        print('ALL_CREATED:')
        for u in created:
            print(u)
    else:
        print('NO_ISSUES_CREATED')


if __name__ == '__main__':
    main()
