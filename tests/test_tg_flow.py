import json
from pathlib import Path
import importlib


def make_pending_item(id_='t1', command='echo hi', exec_request=True, status='pending', created=None):
    return {
        'id': id_,
        'chat_id': 'test_chat',
        'message_id': 'm1',
        'command': command,
        'from': {'first_name': 'UnitTester'},
        'status': status,
        'created': created or '2026-02-03T00:00:00Z',
        'options': {'exec_request': bool(exec_request)}
    }


def test_approve_and_execute_dryrun(tmp_path, monkeypatch):
    # prepare a temp pending file
    pending_path = tmp_path / 'pending_commands.json'
    item = make_pending_item(id_='t-approve-1')
    pending_path.write_text(json.dumps([item], indent=2), encoding='utf-8')

    tcm = importlib.import_module('scripts.tg_command_manager')
    # monkeypatch module PENDING to our temp path
    monkeypatch.setattr(tcm, 'PENDING', pending_path)

    # approve
    res = tcm.approve('t-approve-1', actor='unit-test')
    assert res is not None
    assert res.get('status') == 'approved'

    # execute (dry-run)
    target, err = tcm.execute('t-approve-1', dry_run=True)
    assert err is None
    assert target is not None
    assert target.get('status') == 'executed_dryrun'


def test_toggle_option(tmp_path, monkeypatch):
    pending_path = tmp_path / 'pending_commands.json'
    item = make_pending_item(id_='t-toggle-1', exec_request=False)
    pending_path.write_text(json.dumps([item], indent=2), encoding='utf-8')

    tcm = importlib.import_module('scripts.tg_command_manager')
    monkeypatch.setattr(tcm, 'PENDING', pending_path)

    opts = tcm.toggle_option('t-toggle-1', 'is_test', actor='unit')
    assert opts is not None
    assert opts.get('is_test') is True
