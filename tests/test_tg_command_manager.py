import json
import os
from pathlib import Path

import pytest

import scripts.tg_command_manager as mgr


def write_pending(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, indent=2), encoding='utf-8')


def read_events(path):
    if not path.exists():
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]


@pytest.fixture(autouse=True)
def isolate_fs(tmp_path, monkeypatch):
    # Redirect all file paths in the module to tmp_path to avoid touching repo files
    monkeypatch.setattr(mgr, 'ROOT', tmp_path)
    monkeypatch.setattr(mgr, 'TMP', tmp_path / '.tmp')
    monkeypatch.setattr(mgr, 'PENDING', tmp_path / '.tmp' / 'pending_commands.json')
    monkeypatch.setattr(mgr, 'ENV_FILE', tmp_path / '.tmp' / 'telegram.env')
    monkeypatch.setattr(mgr, 'EVENTS', tmp_path / 'events.ndjson')
    monkeypatch.setattr(mgr, 'DB_PATH', tmp_path / 'gaia.db')
    # ensure module-level functions that rely on paths use new values
    yield


def make_item(id_, command='echo hi', exec_request=True, status='pending'):
    return {
        'id': id_,
        'chat_id': 'test_chat',
        'message_id': 'm1',
        'command': command,
        'from': {'first_name': 'tester'},
        'status': status,
        'created': mgr.now(),
        'options': {'exec_request': exec_request},
    }


def test_approve_and_execute_dryrun(tmp_path):
    pending_path = mgr.PENDING
    events_path = mgr.EVENTS
    # prepare one pending item
    item = make_item('t-approve-1')
    write_pending(pending_path, [item])

    # approve
    res = mgr.approve('t-approve-1', actor='unit-test')
    assert res is not None
    assert res['status'] == 'approved'
    # event recorded
    evs = read_events(events_path)
    assert any(e.get('type') == 'command.approved' and e.get('payload', {}).get('id') == 't-approve-1' for e in evs)

    # ensure ENV disallows real execution by default; execute should produce dryrun
    t, err = mgr.execute('t-approve-1', dry_run=False)
    assert t is not None
    assert t['status'] in ('executed_dryrun', 'executed')
    evs = read_events(events_path)
    assert any(e.get('type', '').endswith('executed') and 't-approve-1' in json.dumps(e) for e in evs)


def test_deny_and_toggle_option(tmp_path):
    pending_path = mgr.PENDING
    events_path = mgr.EVENTS
    # prepare one pending item
    item = make_item('t-deny-1', exec_request=False)
    write_pending(pending_path, [item])

    # deny
    d = mgr.deny('t-deny-1', actor='unit-test')
    assert d is not None
    assert d['status'] == 'denied'
    evs = read_events(events_path)
    assert any(e.get('type') == 'command.denied' and e.get('payload', {}).get('id') == 't-deny-1' for e in evs)

    # toggle option on a new item
    item2 = make_item('t-toggle-1', exec_request=False)
    write_pending(pending_path, [item2])
    opts = mgr.toggle_option('t-toggle-1', 'exec_request', actor='unit-test')
    assert opts is not None
    assert opts.get('exec_request') is True
    evs = read_events(events_path)
    assert any(e.get('type') == 'command.option.toggled' and e.get('payload', {}).get('id') == 't-toggle-1' for e in evs)
