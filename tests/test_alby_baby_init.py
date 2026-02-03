import os
import json
from pathlib import Path
from agents import alby_agent


def test_baby_initialization_creates_status_and_event(tmp_path, monkeypatch):
    # set ALBY_OUT_PATH to tmp
    out_dir = tmp_path / 'out'
    os.environ['ALBY_OUT_PATH'] = str(out_dir)
    events = tmp_path / 'events.ndjson'
    os.environ['GAIA_EVENTS_PATH'] = str(events)
    # ensure no pre-existing status
    assert not (out_dir / 'status.json').exists()

    # run agent with dry-run so it initializes then exits
    rc = alby_agent.main(['--cmd', 'echo hi', '--dry-run'])
    assert rc == 0

    # status.json written
    status_file = out_dir / 'status.json'
    assert status_file.exists()
    st = json.loads(status_file.read_text(encoding='utf-8'))
    assert 'agent_id' in st and 'state' in st

    # notification file
    notif_dir = out_dir / 'notifications'
    files = list(notif_dir.glob('ready_*.json'))
    assert files

    # events file contains agent-ready event
    text = events.read_text(encoding='utf-8')
    objs = [json.loads(l) for l in text.splitlines() if l.strip()]
    found = any(o.get('type') == 'agent-ready' for o in objs)
    assert found
