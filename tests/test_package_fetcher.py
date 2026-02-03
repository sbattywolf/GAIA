import json
import os
import tempfile
import sys
from pathlib import Path

from agents import package_fetcher


def make_request(shared: Path, agent_id: str, pkgs):
    shared.mkdir(parents=True, exist_ok=True)
    req = {'agent_id': agent_id, 'required_packages': pkgs}
    rf = shared / f'packages_request_{agent_id}.json'
    rf.write_text(json.dumps(req), encoding='utf-8')
    return rf


def test_package_fetcher_copies_local_file(tmp_path, monkeypatch):
    shared = tmp_path / 'shared'
    events = tmp_path / 'events.ndjson'
    monkeypatch.setenv('ALBY_SHARED_STORAGE', str(shared))
    monkeypatch.setenv('GAIA_EVENTS_PATH', str(events))

    # create a dummy "package" file and request it via absolute path
    pkg_src = tmp_path / 'dummy_pkg.tar.gz'
    pkg_src.write_text('dummy content', encoding='utf-8')

    agent_id = 'agent-local-1'
    make_request(shared, agent_id, [str(pkg_src)])

    rc = package_fetcher.main(['--scan-once'])
    assert rc in (0, 1)

    # response file created (may be present even on errors)
    resp = shared / f'packages_response_{agent_id}.json'
    assert resp.exists(), 'response file not written'
    data = json.loads(resp.read_text(encoding='utf-8'))
    assert data['agent_id'] == agent_id
    assert len(data['results']) == 1
    assert data['results'][0]['status'] in ('copied', 'dry-run', 'installed', 'downloaded')
