import json
import os
import sys
import tempfile
from pathlib import Path


def test_alby_agent_dry_run(monkeypatch):
    import agents.alby_agent as alby

    with tempfile.TemporaryDirectory() as td:
        ev_path = Path(td) / 'events.ndjson'
        monkeypatch.setenv('GAIA_EVENTS_PATH', str(ev_path))
        monkeypatch.setenv('DRY_RUN', '1')
        monkeypatch.setattr(sys, 'argv', ['alby_agent.py', '--cmd', 'echo hi', '--concurrency', '2'])

        # run main
        alby.main()

        txt = ev_path.read_text(encoding='utf-8').strip()
        assert txt
        lines = txt.splitlines()
        assert len(lines) == 2
        obj = json.loads(lines[-1])
        assert obj['type'] == 'alby.job.complete'
        assert obj['payload']['cmd'] == 'echo hi'
        assert obj['payload']['stdout'] == 'DRY_RUN'
