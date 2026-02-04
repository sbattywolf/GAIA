import os
import json
from agents import alby_agent


def test_dry_run_trace_emitted(tmp_path, monkeypatch):
    events = tmp_path / 'events.ndjson'
    monkeypatch.setenv('GAIA_EVENTS_PATH', str(events))
    monkeypatch.setenv('PROTOTYPE_USE_LOCAL_EVENTS', '1')

    rc = alby_agent.main(['--cmd', 'echo hi', '--concurrency', '2', '--dry-run'])
    assert rc == 0
    text = events.read_text(encoding='utf-8')
    lines = [l for l in text.splitlines() if l.strip()]
    assert len(lines) == 2
    for line in lines:
        obj = json.loads(line)
        assert obj['type'] == 'alby.job.complete'
        assert 'idem' in obj['payload']
