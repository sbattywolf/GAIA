import json
import os
from pathlib import Path

from agents import package_consumer


def test_package_consumer_copies_cache(tmp_path, monkeypatch):
    shared = tmp_path / 'shared'
    out = tmp_path / 'out'
    events = tmp_path / 'events.ndjson'
    monkeypatch.setenv('ALBY_SHARED_STORAGE', str(shared))
    monkeypatch.setenv('ALBY_OUT_PATH', str(out))
    monkeypatch.setenv('GAIA_EVENTS_PATH', str(events))

    # create cache files for an agent
    agent_id = 'consumer-1'
    cache = shared / 'packages_cache' / agent_id
    cache.mkdir(parents=True, exist_ok=True)
    (cache / 'pkgA.whl').write_text('wheel', encoding='utf-8')

    # write response indicating packages available
    resp = {'agent_id': agent_id, 'requested': ['pkgA'], 'results': [{'package': 'pkgA', 'status': 'downloaded'}]}
    resp_file = shared / f'packages_response_{agent_id}.json'
    resp_file.write_text(json.dumps(resp), encoding='utf-8')

    rc = package_consumer.main(['--scan-once'])
    assert rc in (0, 1)

    vendor = out / 'vendor' / agent_id
    assert vendor.exists()
    files = list(vendor.iterdir())
    assert any(f.name == 'pkgA.whl' for f in files)
