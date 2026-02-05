import json
from pathlib import Path
import tempfile
import importlib.util


def load_guard_module():
    spec = importlib.util.spec_from_file_location('ag', 'scripts/autonomy_guard.py')
    ag = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ag)
    return ag


def test_is_autonomous_enabled_false(tmp_path: Path):
    ag = load_guard_module()
    # write a session file with false in <ROOT>/.tmp
    root = tmp_path / 'repo'
    tmpdir = root / '.tmp'
    tmpdir.mkdir(parents=True)
    p = tmpdir / 'autonomous_mode.json'
    p.write_text(json.dumps({"autonomous": False}), encoding='utf-8')
    ag.ROOT = root
    assert ag.is_autonomous_enabled() is False


def test_is_autonomous_enabled_true(tmp_path: Path):
    ag = load_guard_module()
    root = tmp_path / 'repo'
    tmpdir = root / '.tmp'
    tmpdir.mkdir(parents=True)
    p = tmpdir / 'autonomous_mode.json'
    p.write_text(json.dumps({"autonomous": True}), encoding='utf-8')
    ag.ROOT = root
    assert ag.is_autonomous_enabled() is True
