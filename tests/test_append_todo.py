import json
import sys
import tempfile
from pathlib import Path
from scripts import append_todo


def test_append_todo_writes(monkeypatch):
    with tempfile.TemporaryDirectory() as td:
        archive = Path(td) / 'todo-archive.ndjson'
        monkeypatch.setattr(append_todo, 'ARCHIVE', str(archive))
        monkeypatch.setattr(sys, 'argv', ['append_todo.py', '--title', 'Fix', '--description', 'd', '--priority', '10', '--added_by', 'tester'])

        append_todo.main()

        text = archive.read_text(encoding='utf-8').strip()
        assert text
        obj = json.loads(text.splitlines()[-1])
        assert obj['title'] == 'Fix'
        assert obj['added_by'] == 'tester'
