import os
import json
from typing import List

GITHUB_API = 'https://api.github.com/graphql'


def _read_local_backlog(path: str = '.tmp/backlog.json', n: int = 6) -> List[str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        items = []
        for i, it in enumerate(data[:n]):
            title = it.get('title') or it.get('name') or str(it)
            desc = it.get('desc') or it.get('description') or ''
            items.append(f"{i+1}. {title} - {desc}".strip())
        return items
    except Exception:
        return []


def _github_prs(repo: str, token: str, n: int = 6) -> List[str]:
    try:
        import requests
    except Exception:
        return []
    if not repo or not token:
        return []
    owner, name = repo.split('/') if '/' in repo else (None, repo)
    if not owner or not name:
        return []
    query = '''
    query($owner: String!, $name: String!, $n:Int!) {
      repository(owner: $owner, name: $name) {
        pullRequests(states: OPEN, first: $n, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes {
            number
            title
            url
            updatedAt
            reviewDecision
            mergeable
            labels(first:5) { nodes { name } }
          }
        }
      }
    }
    '''
    variables = {"owner": owner, "name": name, "n": n}
    try:
        r = requests.post(GITHUB_API, json={'query': query, 'variables': variables}, headers={'Authorization': f'bearer {token}'}, timeout=10)
        r.raise_for_status()
        j = r.json()
        nodes = j.get('data', {}).get('repository', {}).get('pullRequests', {}).get('nodes', [])
        items = []
        for node in nodes:
            number = node.get('number')
            title = node.get('title')
            review = node.get('reviewDecision') or 'REVIEW_UNKNOWN'
            mergeable = node.get('mergeable')
            labels = [l.get('name') for l in node.get('labels', {}).get('nodes', []) if l.get('name')]
            lbls = f" [{', '.join(labels)}]" if labels else ''
            items.append(f"PR #{number} {title} — {review}{lbls}")
        return items
    except Exception:
        return []


def get_top_pending(n: int = 6) -> List[str]:
    """Return a list of top pending items as short strings.

    Strategy: prefer GitHub (requires `AUTOMATION_GITHUB_REPOSITORY` and `GAIA_GITHUB_TOKEN` in env),
    else fallback to `.tmp/backlog.json`.
    """
    from gaia.env_helpers import get_github_token
    repo = os.environ.get('AUTOMATION_GITHUB_REPOSITORY') or os.environ.get('AUTOMATION_GITHUB_REPO') or os.environ.get('GITHUB_REPOSITORY')
    token = get_github_token()
    if repo and token:
        items = _github_prs(repo, token, n)
        if items:
            return items
    # fallback
    items = _read_local_backlog('.tmp/backlog.json', n)
    return items


if __name__ == '__main__':
    for l in get_top_pending(6):
        print(l)
