#!/usr/bin/env python3
"""Update doc/todo-archive.ndjson by reading from all backlog entity sources.

This script consolidates backlog entities from:
- sprints/*.json (sprint session files)
- backlogs/*.json (backlog snapshot files)
- tasks.json (task definitions)
- Existing doc/todo-archive.ndjson entries

It normalizes all entities into the todo-archive format and appends new/updated
entries without creating duplicates.

Usage:
    python scripts/update_todo_archive.py [--dry-run] [--verbose]
    
Options:
    --dry-run       Show what would be written without modifying files
    --verbose       Show detailed processing information
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'doc' / 'todo-archive.ndjson'
SPRINTS_DIR = ROOT / 'sprints'
BACKLOGS_DIR = ROOT / 'backlogs'
TASKS_FILE = ROOT / 'tasks.json'


def load_ndjson(path: Path) -> List[Dict]:
    """Load NDJSON file and return list of entries."""
    entries = []
    if not path.exists():
        return entries
    
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                entries.append(obj)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping malformed line in {path}: {e}", file=sys.stderr)
                continue
    return entries


def load_json(path: Path) -> Dict:
    """Load a JSON file."""
    if not path.exists():
        return {}
    
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse {path}: {e}", file=sys.stderr)
        return {}


def normalize_entry(entry: Dict, source: str) -> Dict:
    """Normalize an entry to the standard todo-archive format.
    
    Standard fields:
    - id: unique identifier
    - title: task title
    - description: optional description
    - status: pending|in-progress|completed|done
    - priority: critical|high|medium|low or numeric
    - est_hours: estimated hours (float)
    - added_at: ISO8601 timestamp
    - source: source file path
    """
    normalized = {}
    
    # Required: id
    normalized['id'] = entry.get('id', entry.get('task_id', ''))
    if not normalized['id']:
        return None
    
    # Required: title
    normalized['title'] = entry.get('title', entry.get('name', entry.get('task', '')))
    if not normalized['title']:
        return None
    
    # Optional: description
    desc = entry.get('description', entry.get('desc', entry.get('body', '')))
    if desc:
        normalized['description'] = desc
    
    # Status normalization
    status = entry.get('status', 'pending')
    status_map = {
        'done': 'completed',
        'finished': 'completed',
        'closed': 'completed',
        'started': 'in-progress',
        'active': 'in-progress',
        'not-started': 'pending',
        'todo': 'pending',
    }
    normalized['status'] = status_map.get(status.lower(), status.lower())
    
    # Priority
    priority = entry.get('priority', 'medium')
    if isinstance(priority, (int, float)):
        # Convert numeric priority to label
        if priority >= 100:
            priority = 'critical'
        elif priority >= 50:
            priority = 'high'
        elif priority >= 20:
            priority = 'medium'
        else:
            priority = 'low'
    normalized['priority'] = str(priority).lower()
    
    # Estimated hours
    est = entry.get('est_hours', entry.get('estimate', entry.get('hours', 0)))
    normalized['est_hours'] = float(est) if est else 0.0
    
    # Timestamp
    added = entry.get('added_at', entry.get('created_at', entry.get('timestamp', '')))
    if not added:
        added = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    normalized['added_at'] = added
    
    # Source
    normalized['source'] = entry.get('source', source)
    
    # Copy additional useful fields if present
    for field in ['epic', 'feature', 'story', 'score', 'scrum_points', 'completed_at', 'result', 'trace_id']:
        if field in entry:
            normalized[field] = entry[field]
    
    return normalized


def read_sprints() -> List[Dict]:
    """Read all sprint JSON files and extract items."""
    items = []
    
    if not SPRINTS_DIR.exists():
        return items
    
    for sprint_file in SPRINTS_DIR.glob('*.json'):
        data = load_json(sprint_file)
        if not data:
            continue
        
        # Extract items from sprint
        sprint_items = data.get('items', [])
        for item in sprint_items:
            normalized = normalize_entry(item, f"sprints/{sprint_file.name}")
            if normalized:
                items.append(normalized)
    
    return items


def read_backlogs() -> List[Dict]:
    """Read all backlog JSON files and extract items."""
    items = []
    
    if not BACKLOGS_DIR.exists():
        return items
    
    for backlog_file in BACKLOGS_DIR.glob('*.json'):
        data = load_json(backlog_file)
        if not data:
            continue
        
        # Extract items from backlog
        backlog_items = data.get('items', [])
        for item in backlog_items:
            normalized = normalize_entry(item, f"backlogs/{backlog_file.name}")
            if normalized:
                items.append(normalized)
    
    return items


def read_tasks() -> List[Dict]:
    """Read tasks.json and extract items."""
    items = []
    
    data = load_json(TASKS_FILE)
    if not data:
        return items
    
    # Handle both list and dict formats
    if isinstance(data, list):
        task_items = data
    elif isinstance(data, dict):
        task_items = data.get('tasks', data.get('items', []))
    else:
        return items
    
    for item in task_items:
        normalized = normalize_entry(item, 'tasks.json')
        if normalized:
            items.append(normalized)
    
    return items


def get_existing_entries() -> Dict[str, Dict]:
    """Load existing todo-archive entries, keeping the latest version of each ID."""
    entries = load_ndjson(ARCHIVE)
    
    # Build a dict with latest entry per ID
    by_id = {}
    for entry in entries:
        entry_id = entry.get('id')
        if entry_id:
            by_id[entry_id] = entry
    
    return by_id


def merge_entries(existing: Dict[str, Dict], new_items: List[Dict]) -> List[Dict]:
    """Merge new items with existing ones, preferring newer data."""
    merged = existing.copy()
    
    for item in new_items:
        item_id = item['id']
        
        if item_id not in merged:
            # New item
            merged[item_id] = item
        else:
            # Item exists - update if newer or has more info
            existing_item = merged[item_id]
            
            # Prefer non-pending status updates
            if item['status'] != 'pending' and existing_item.get('status') == 'pending':
                merged[item_id] = item
            # Update if timestamp is newer
            elif item.get('added_at', '') > existing_item.get('added_at', ''):
                merged[item_id] = item
    
    return list(merged.values())


def write_archive(entries: List[Dict], dry_run: bool = False):
    """Write entries to todo-archive.ndjson."""
    # Sort entries by ID for consistency (convert to string for sorting)
    entries.sort(key=lambda x: str(x.get('id', '')))
    
    if dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - Would write to {ARCHIVE}:")
        print(f"{'='*60}")
        for entry in entries:
            print(json.dumps(entry, ensure_ascii=False))
        print(f"{'='*60}")
        print(f"Total entries: {len(entries)}")
    else:
        # Ensure directory exists
        ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
        
        # Write all entries
        with ARCHIVE.open('w', encoding='utf-8') as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"✓ Updated {ARCHIVE}")
        print(f"  Total entries: {len(entries)}")


def main():
    parser = argparse.ArgumentParser(
        description="Update doc/todo-archive.ndjson from all backlog sources"
    )
    parser.add_argument('--dry-run', action='store_true',
                        help="Show what would be written without modifying files")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="Show detailed processing information")
    args = parser.parse_args()
    
    if args.verbose:
        print("Reading backlog sources...")
    
    # Collect all items from various sources
    sprint_items = read_sprints()
    backlog_items = read_backlogs()
    task_items = read_tasks()
    
    if args.verbose:
        print(f"  Sprint items: {len(sprint_items)}")
        print(f"  Backlog items: {len(backlog_items)}")
        print(f"  Task items: {len(task_items)}")
    
    # Combine all new items
    all_new_items = sprint_items + backlog_items + task_items
    
    if args.verbose:
        print(f"\nTotal new items collected: {len(all_new_items)}")
    
    # Get existing entries
    existing = get_existing_entries()
    
    if args.verbose:
        print(f"Existing archive entries: {len(existing)}")
    
    # Merge with existing
    merged = merge_entries(existing, all_new_items)
    
    if args.verbose:
        print(f"Merged total: {len(merged)} entries")
        
        # Count by status
        status_counts = {}
        for entry in merged:
            status = entry.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\nStatus breakdown:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")
    
    # Write to archive
    write_archive(merged, dry_run=args.dry_run)
    
    if not args.dry_run:
        print("\n✓ Archive update complete")
        print(f"\nTo view the archive: cat {ARCHIVE}")
        print(f"To sync to database: python agents/sync_backlog_to_db.py")


if __name__ == '__main__':
    main()
