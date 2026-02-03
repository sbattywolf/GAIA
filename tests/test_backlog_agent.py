import json
import sys
import tempfile
from pathlib import Path
from agents import backlog_agent


def test_backlog_agent_appends_event(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        events = Path(td) / 'events.ndjson'
        monkeypatch.setattr(backlog_agent, 'EVENTS_PATH', str(events))
        # avoid calling external CLI
        monkeypatch.setattr(backlog_agent, 'gh_create_issue', lambda t, b: 'http://example/1')
        monkeypatch.setattr(sys, 'argv', ['backlog_agent.py', '--title', 'T', '--body', 'B'])

        backlog_agent.main()

        content = events.read_text(encoding='utf-8').strip()
        assert content
        obj = json.loads(content.splitlines()[-1])
        assert obj['type'] == 'issue.create'
        assert obj['payload']['title'] == 'T'
        assert obj['payload']['issue_url'] == 'http://example/1'
