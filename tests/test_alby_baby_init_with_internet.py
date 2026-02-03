import os
import json
from pathlib import Path
from agents import alby_agent


def test_baby_init_writes_checklist_and_package_request(tmp_path, monkeypatch):
    # place internet_capable_agent.json in repo root
    repo_root = Path(__file__).resolve().parents[2]
    marker = tmp_path / 'internet_capable_agent.json'
    marker.write_text(json.dumps({'required_packages': ['packageA==1.2.3', 'packageB>=4.0']}), encoding='utf-8')

    # monkeypatch repo root location by copying marker to actual repo root used by agent
    # alby_agent determines repo_root from its __file__ parents; we will set ALBY_SHARED_STORAGE and ALBY_OUT_PATH to tmp
    os.environ['ALBY_OUT_PATH'] = str(tmp_path / 'out')
    os.environ['GAIA_EVENTS_PATH'] = str(tmp_path / 'events.ndjson')
    os.environ['ALBY_SHARED_STORAGE'] = str(tmp_path / 'shared')

    # copy marker into repo root location expected by agent
    repo_marker = repo_root / 'internet_capable_agent.json'
    # write into repo root (workspace) for test
    with open(repo_marker, 'w', encoding='utf-8') as f:
        f.write(marker.read_text(encoding='utf-8'))

    try:
        # ensure tokens not present
        for k in ('ALBY_INTERNET_TOKEN', 'CI_TOKEN', 'GITHUB_TOKEN'):
            if k in os.environ:
                del os.environ[k]

        rc = alby_agent.main(['--cmd', 'echo hi', '--dry-run'])
        assert rc == 0

        # CHECKLIST.md exists
        checklist = Path(os.environ['ALBY_OUT_PATH']) / 'CHECKLIST.md'
        assert checklist.exists()
        text = checklist.read_text(encoding='utf-8')
        assert 'ALBY_INTERNET_TOKEN' in text

        # package request written to shared storage
        shared = Path(os.environ['ALBY_SHARED_STORAGE'])
        files = list(shared.glob('packages_request_*.json'))
        assert files, 'no package request files found'
        req = json.loads(files[0].read_text(encoding='utf-8'))
        assert 'required_packages' in req and len(req['required_packages']) == 2
    finally:
        # cleanup marker
        try:
            repo_marker.unlink()
        except Exception:
            pass
