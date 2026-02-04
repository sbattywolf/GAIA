import json
from pathlib import Path

import pytest


def test_find_and_make_candidate(tmp_path, monkeypatch):
    # Import inside test to ensure pytest's import hooks and monkeypatching work
    import scripts.alby_agent as agent_module

    # Point the agent's ROOT at our temporary repo
    monkeypatch.setattr(agent_module, 'ROOT', tmp_path)

    # Create .tmp/todolists and sample todolist files for the story
    todolists = tmp_path / '.tmp' / 'todolists'
    todolists.mkdir(parents=True)
    f1 = todolists / 'EPC_Telegram.current.STR_TestGise.current'
    f2 = todolists / 'EPC_Telegram.current.STR_TestGise.draft'
    f1.write_text(json.dumps({'story': 'STR_TestGise', 'tasks': []}), encoding='utf-8')
    f2.write_text(json.dumps({'story': 'STR_TestGise', 'tasks': []}), encoding='utf-8')

    found = agent_module.find_todolists_for_story('STR_TestGise', root=tmp_path)
    assert len(found) == 2

    # Ensure merged candidates dir is created in the repo
    merged = agent_module.ensure_merged_dir(root=tmp_path)
    assert merged.exists() and merged.is_dir()

    # Prevent actual DB writes by stubbing write_audit
    monkeypatch.setattr(agent_module, 'write_audit', lambda actor, action, details: None)

    # Create a merge candidate from one of the files
    cand = agent_module.make_merge_candidate(f1, merged, actor='Gise', dry_run=False)
    assert cand is not None
    assert Path(cand).exists()

    payload = json.loads(Path(cand).read_text(encoding='utf-8'))
    assert payload.get('actor') == 'Gise'
    assert 'content' in payload


def test_make_candidate_with_non_json_content(tmp_path, monkeypatch):
    import scripts.alby_agent as agent_module

    monkeypatch.setattr(agent_module, 'ROOT', tmp_path)
    todolists = tmp_path / '.tmp' / 'todolists'
    todolists.mkdir(parents=True)
    f = todolists / 'EPC_Telegram.current.STR_TestGise.AgentGise.Todo.current'
    f.write_text('plain text content that is not JSON', encoding='utf-8')

    merged = agent_module.ensure_merged_dir(root=tmp_path)
    monkeypatch.setattr(agent_module, 'write_audit', lambda a, b, c: None)

    cand = agent_module.make_merge_candidate(f, merged, actor='Gise', dry_run=False)
    assert cand is not None
    data = json.loads(Path(cand).read_text(encoding='utf-8'))
    # Non-JSON content should be preserved as string in 'content'
    assert isinstance(data.get('content'), str)
