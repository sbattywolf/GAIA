import os
import json
from pathlib import Path
from agents import alby_agent


def test_manifest_dry_run(tmp_path, monkeypatch):
    events = tmp_path / 'events.ndjson'
    os.environ['GAIA_EVENTS_PATH'] = str(events)
    # create a manifest with two steps
    manifest = tmp_path / 'm.json'
    m = {
        'name': 'test-manifest',
        'steps': [
            {'id': 's1', 'cmd': 'echo step1'},
            {'id': 's2', 'cmd': 'echo step2'}
        ]
    }
    manifest.write_text(json.dumps(m), encoding='utf-8')

    rc = alby_agent.main(['--manifest', str(manifest), '--cmd', 'echo x', '--dry-run'])
    assert rc == 0
    text = events.read_text(encoding='utf-8')
    lines = [l for l in text.splitlines() if l.strip()]
    # dry-run should emit two step events and no manifest.complete? we emit job.complete for dry-run steps
    assert len(lines) == 2
    objs = [json.loads(l) for l in lines]
    assert all(o['type'] == 'alby.job.complete' for o in objs)
    assert objs[0]['payload']['step_id'] == 's1'
    assert objs[1]['payload']['step_id'] == 's2'
