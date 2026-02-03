import json
import os
import subprocess
import tempfile
from types import SimpleNamespace

import pytest

from agents import ci_issue_collector
from agents import agent_utils


def make_failures(n=2):
    return [{'id': f'fail-{i}', 'title': f'Failure {i}', 'body': f'Log for failure {i}'} for i in range(n)]


def test_dry_run_appends_events(tmp_path, monkeypatch):
    events_file = tmp_path / 'events.ndjson'
    os.environ['GAIA_EVENTS_PATH'] = str(events_file)
    # inject a fake report file
    report = tmp_path / 'report.json'
    failures = make_failures(3)
    report.write_text(json.dumps(failures), encoding='utf-8')
    os.environ['FILE_CI_REPORT'] = str(report)

    # ensure dry-run
    rc = ci_issue_collector.main(['--repo', 'owner/repo', '--since', '2026-01-01', '--dry-run'])
    assert rc == 0
    text = events_file.read_text(encoding='utf-8')
    lines = [l for l in text.splitlines() if l.strip()]
    assert len(lines) == 3
    for i, line in enumerate(lines):
        obj = json.loads(line)
        assert obj['type'] == 'ci.issue'
        assert obj['payload']['failure']['id'] == f'fail-{i}'


def test_live_invokes_gh(monkeypatch, tmp_path):
    events_file = tmp_path / 'events.ndjson'
    os.environ['GAIA_EVENTS_PATH'] = str(events_file)
    failures = make_failures(1)
    report = tmp_path / 'report2.json'
    report.write_text(json.dumps(failures), encoding='utf-8')
    os.environ['FILE_CI_REPORT'] = str(report)

    # mock subprocess.run for gh
    def fake_run(cmd, capture_output, text, check):
        class P:
            stdout = 'https://github.com/owner/repo/issues/123\n'

        return P()

    monkeypatch.setattr(subprocess, 'run', fake_run)

    rc = ci_issue_collector.main(['--repo', 'owner/repo', '--since', '2026-01-01'])
    assert rc == 0
    text = events_file.read_text(encoding='utf-8')
    lines = [l for l in text.splitlines() if l.strip()]
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert obj['payload']['issue_url'].startswith('https://')
