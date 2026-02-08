import json
import sys
import tempfile
from pathlib import Path
import pytest


def test_update_todo_archive_basic(monkeypatch):
    """Test basic functionality of update_todo_archive script."""
    # Import the script module
    sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
    import update_todo_archive
    
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        
        # Create test directory structure
        sprints_dir = td_path / 'sprints'
        backlogs_dir = td_path / 'backlogs'
        sprints_dir.mkdir()
        backlogs_dir.mkdir()
        
        # Create test sprint file
        sprint_data = {
            "id": "test-sprint-1",
            "items": [
                {"id": "S001", "title": "Sprint Task 1", "status": "pending", "priority": "high", "est_hours": 2},
                {"id": "S002", "title": "Sprint Task 2", "status": "in-progress", "priority": "medium", "est_hours": 3}
            ]
        }
        (sprints_dir / 'sprint1.json').write_text(json.dumps(sprint_data))
        
        # Create test backlog file
        backlog_data = {
            "id": "test-backlog-1",
            "items": [
                {"id": "B001", "title": "Backlog Task 1", "status": "pending", "priority": "low", "est_hours": 1}
            ]
        }
        (backlogs_dir / 'backlog1.json').write_text(json.dumps(backlog_data))
        
        # Create existing archive with one entry
        archive = td_path / 'doc' / 'todo-archive.ndjson'
        archive.parent.mkdir()
        existing_entry = {"id": "E001", "title": "Existing Task", "status": "completed", "priority": "high", "est_hours": 5, "added_at": "2026-01-01T00:00:00Z", "source": "test"}
        archive.write_text(json.dumps(existing_entry) + '\n')
        
        # Mock the paths
        monkeypatch.setattr(update_todo_archive, 'ARCHIVE', archive)
        monkeypatch.setattr(update_todo_archive, 'SPRINTS_DIR', sprints_dir)
        monkeypatch.setattr(update_todo_archive, 'BACKLOGS_DIR', backlogs_dir)
        monkeypatch.setattr(update_todo_archive, 'TASKS_FILE', td_path / 'tasks.json')
        
        # Run the script
        monkeypatch.setattr(sys, 'argv', ['update_todo_archive.py'])
        update_todo_archive.main()
        
        # Verify the archive was updated
        assert archive.exists()
        lines = archive.read_text().strip().split('\n')
        
        # Should have 4 entries (1 existing + 3 new)
        assert len(lines) == 4
        
        # Parse and verify entries
        entries = [json.loads(line) for line in lines]
        ids = {e['id'] for e in entries}
        
        assert 'E001' in ids  # Existing kept
        assert 'S001' in ids  # Sprint task 1
        assert 'S002' in ids  # Sprint task 2
        assert 'B001' in ids  # Backlog task 1
        
        # Verify normalization
        s001 = next(e for e in entries if e['id'] == 'S001')
        assert s001['title'] == 'Sprint Task 1'
        assert s001['priority'] == 'high'
        assert s001['est_hours'] == 2


def test_update_todo_archive_deduplication(monkeypatch):
    """Test that duplicate IDs are handled correctly."""
    sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
    import update_todo_archive
    
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        
        sprints_dir = td_path / 'sprints'
        sprints_dir.mkdir()
        
        # Create sprint with duplicate ID but different status
        sprint_data = {
            "items": [
                {"id": "T001", "title": "Task Updated", "status": "completed", "priority": "high", "est_hours": 2}
            ]
        }
        (sprints_dir / 'sprint1.json').write_text(json.dumps(sprint_data))
        
        # Create existing archive with same ID but pending status
        archive = td_path / 'doc' / 'todo-archive.ndjson'
        archive.parent.mkdir()
        existing = {"id": "T001", "title": "Task Original", "status": "pending", "priority": "high", "est_hours": 2, "added_at": "2026-01-01T00:00:00Z", "source": "test"}
        archive.write_text(json.dumps(existing) + '\n')
        
        monkeypatch.setattr(update_todo_archive, 'ARCHIVE', archive)
        monkeypatch.setattr(update_todo_archive, 'SPRINTS_DIR', sprints_dir)
        monkeypatch.setattr(update_todo_archive, 'BACKLOGS_DIR', td_path / 'backlogs')
        monkeypatch.setattr(update_todo_archive, 'TASKS_FILE', td_path / 'tasks.json')
        
        monkeypatch.setattr(sys, 'argv', ['update_todo_archive.py'])
        update_todo_archive.main()
        
        # Verify only one entry with the ID exists
        lines = archive.read_text().strip().split('\n')
        assert len(lines) == 1
        
        entry = json.loads(lines[0])
        assert entry['id'] == 'T001'
        # Should prefer the completed status over pending
        assert entry['status'] == 'completed'
        assert entry['title'] == 'Task Updated'


def test_normalize_entry():
    """Test entry normalization logic."""
    sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
    import update_todo_archive
    
    # Test basic normalization
    entry = {
        'id': 'T001',
        'title': 'Test Task',
        'desc': 'Description here',
        'status': 'done',
        'priority': 100,
        'hours': 5
    }
    
    normalized = update_todo_archive.normalize_entry(entry, 'test.json')
    
    assert normalized['id'] == 'T001'
    assert normalized['title'] == 'Test Task'
    assert normalized['description'] == 'Description here'
    assert normalized['status'] == 'completed'  # 'done' -> 'completed'
    assert normalized['priority'] == 'critical'  # 100 -> 'critical'
    assert normalized['est_hours'] == 5.0
    assert normalized['source'] == 'test.json'
    
    # Test missing required fields
    entry_no_id = {'title': 'Test'}
    assert update_todo_archive.normalize_entry(entry_no_id, 'test.json') is None
    
    entry_no_title = {'id': 'T001'}
    assert update_todo_archive.normalize_entry(entry_no_title, 'test.json') is None


def test_priority_conversion():
    """Test numeric to text priority conversion."""
    sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
    import update_todo_archive
    
    test_cases = [
        (100, 'critical'),
        (150, 'critical'),
        (50, 'high'),
        (75, 'high'),
        (20, 'medium'),
        (30, 'medium'),
        (10, 'low'),
        (5, 'low'),
    ]
    
    for numeric, expected in test_cases:
        entry = {'id': 'T1', 'title': 'Test', 'priority': numeric}
        normalized = update_todo_archive.normalize_entry(entry, 'test.json')
        assert normalized['priority'] == expected, f"Priority {numeric} should map to {expected}"


def test_status_normalization():
    """Test status normalization."""
    sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
    import update_todo_archive
    
    status_map = [
        ('done', 'completed'),
        ('finished', 'completed'),
        ('closed', 'completed'),
        ('started', 'in-progress'),
        ('active', 'in-progress'),
        ('not-started', 'pending'),
        ('todo', 'pending'),
        ('pending', 'pending'),
    ]
    
    for original, expected in status_map:
        entry = {'id': 'T1', 'title': 'Test', 'status': original}
        normalized = update_todo_archive.normalize_entry(entry, 'test.json')
        assert normalized['status'] == expected, f"Status {original} should map to {expected}"
