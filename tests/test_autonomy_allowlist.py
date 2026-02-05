import json
import os
from pathlib import Path

import pytest

import importlib.util


spec = importlib.util.spec_from_file_location('autonomy_guard', 'scripts/autonomy_guard.py')
ag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ag)


def write_allowlist(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding='utf-8')


def reset_cache():
    # clear cached allowlist
    try:
        ag._ALLOWLIST = None
    except Exception:
        pass


def test_command_allowed_from_file(tmp_path):
    cfg = tmp_path / 'agent_mode_allowlist.json'
    write_allowlist(cfg, {'allowed_commands': ['send_telegram', 'create_issue'], 'allowed_paths': []})
    # point loader to our temp file
    orig = ag._allowlist_path
    ag._allowlist_path = lambda: cfg
    reset_cache()
    assert ag.is_command_allowed('send_telegram') is True
    assert ag.is_command_allowed('create_issue') is True
    assert ag.is_command_allowed('nonexistent') is False
    ag._allowlist_path = orig


def test_empty_allowlist_uses_env(tmp_path, monkeypatch):
    cfg = tmp_path / 'agent_mode_allowlist.json'
    write_allowlist(cfg, {'allowed_commands': [], 'allowed_paths': []})
    orig = ag._allowlist_path
    ag._allowlist_path = lambda: cfg
    reset_cache()
    monkeypatch.setenv('ALLOW_COMMAND_EXECUTION', '1')
    assert ag.is_command_allowed('anything') is True
    monkeypatch.setenv('ALLOW_COMMAND_EXECUTION', '0')
    reset_cache()
    assert ag.is_command_allowed('anything') is False
    ag._allowlist_path = orig


def test_path_allowed(tmp_path):
    cfg = tmp_path / 'agent_mode_allowlist.json'
    write_allowlist(cfg, {'allowed_commands': [], 'allowed_paths': ['.tmp/']})
    orig = ag._allowlist_path
    ag._allowlist_path = lambda: cfg
    reset_cache()
    # create a path under repo root .tmp/example
    repo_root = Path(__file__).resolve().parent.parent
    target = repo_root / '.tmp' / 'example.txt'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('x')
    assert ag.is_path_allowed(str(target)) is True
    # a path outside .tmp should be False
    assert ag.is_path_allowed(str(repo_root / 'README.md')) is False
    ag._allowlist_path = orig
