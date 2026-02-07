# Updating todo-archive.ndjson from Multiple Sources

## Overview

The `scripts/update_todo_archive.py` script consolidates backlog entities from multiple JSON sources into the canonical `doc/todo-archive.ndjson` file. This ensures all task and sprint information is properly tracked in the archive.

## Purpose

As documented in `LAPTOP_SETUP.md` (lines 14, 158, 169), the dashboard and other tools read from `doc/todo-archive.ndjson`. However, backlog entities can be scattered across multiple files:

- **Sprint files**: `sprints/*.json` - Sprint session planning files
- **Backlog files**: `backlogs/*.json` - Backlog snapshot files  
- **Task files**: `tasks.json` - Task definitions
- **Archive**: `doc/todo-archive.ndjson` - The canonical archive (NDJSON format)

This script reads all these sources, normalizes the data, and updates the archive without creating duplicates.

## Usage

### Basic Usage

```bash
# Update the archive from all sources
python scripts/update_todo_archive.py
```

### Dry-Run Mode

Preview what would be updated without modifying files:

```bash
# See what would be written
python scripts/update_todo_archive.py --dry-run
```

### Verbose Mode

Get detailed information about the processing:

```bash
# Show detailed statistics
python scripts/update_todo_archive.py --verbose

# Combine with dry-run
python scripts/update_todo_archive.py --dry-run --verbose
```

## What the Script Does

1. **Reads Multiple Sources**:
   - Scans all `sprints/*.json` files for sprint items
   - Scans all `backlogs/*.json` files for backlog items
   - Reads `tasks.json` for task definitions
   - Loads existing entries from `doc/todo-archive.ndjson`

2. **Normalizes Data**:
   - Converts all entries to a standard format with required fields:
     - `id`: unique identifier
     - `title`: task title
     - `status`: pending|in-progress|completed
     - `priority`: critical|high|medium|low
     - `est_hours`: estimated hours (float)
     - `added_at`: ISO8601 timestamp
     - `source`: source file path
   - Handles various field name variations (e.g., `desc` vs `description`)
   - Converts numeric priorities to text labels

3. **Merges Intelligently**:
   - Keeps latest version of each unique ID
   - Prefers non-pending status updates over pending ones
   - Preserves additional fields (epic, feature, story, etc.)

4. **Writes Clean Output**:
   - Sorts entries by ID for consistency
   - Writes one JSON object per line (NDJSON format)
   - Validates all JSON before writing

## Field Mapping

The script normalizes various field names from source files:

| Standard Field | Possible Source Fields |
|----------------|------------------------|
| `id` | `id`, `task_id` |
| `title` | `title`, `name`, `task` |
| `description` | `description`, `desc`, `body` |
| `status` | `status` (normalized: done→completed, started→in-progress, etc.) |
| `priority` | `priority` (text or numeric, converted to critical/high/medium/low) |
| `est_hours` | `est_hours`, `estimate`, `hours` |
| `added_at` | `added_at`, `created_at`, `timestamp` |

## Data Flow

```
sprints/*.json ───┐
                  │
backlogs/*.json ──┼──> normalize_entry() ──> merge_entries() ──> doc/todo-archive.ndjson
                  │
tasks.json ───────┘
```

After updating the archive, you can sync it to the database:

```bash
python agents/sync_backlog_to_db.py
```

## Integration with Other Tools

### Dashboard
The GAIA dashboard (`scripts/dashboard_server.py`) reads from `doc/todo-archive.ndjson` as described in `LAPTOP_SETUP.md`:

```bash
python scripts/dashboard_server.py --port 9080
# Open http://localhost:9080/dashboard
```

### Database Sync
After updating the archive, sync to the SQLite database:

```bash
python agents/sync_backlog_to_db.py
```

This updates the `backlog` table in `gaia.db` which agents use for runtime decisions (see `doc/agent_session_recovery.md`).

### Adding New Items
To add individual items, use the append script:

```bash
python scripts/append_todo.py --title "New Task" --description "Details" --priority high
```

## When to Run This Script

Run `update_todo_archive.py` when:

1. **After Sprint Planning**: New sprint JSON files have been created
2. **After Backlog Updates**: Backlog JSON files have been modified
3. **Before Dashboard Review**: To ensure dashboard shows latest data
4. **Before Database Sync**: To consolidate changes before syncing to `gaia.db`
5. **During Session Recovery**: As part of agent recovery workflow

## Automation

You can add this script to automated workflows:

```bash
# Example: Update archive and sync to DB
python scripts/update_todo_archive.py --verbose && \
python agents/sync_backlog_to_db.py
```

## Example Output

```
Reading backlog sources...
  Sprint items: 27
  Backlog items: 12
  Task items: 0

Total new items collected: 39
Existing archive entries: 34
Merged total: 44 entries

Status breakdown:
  completed: 9
  in-progress: 10
  pending: 23
  started: 1

✓ Updated /home/runner/work/GAIA/GAIA/doc/todo-archive.ndjson
  Total entries: 44

✓ Archive update complete

To view the archive: cat /home/runner/work/GAIA/GAIA/doc/todo-archive.ndjson
To sync to database: python agents/sync_backlog_to_db.py
```

## Troubleshooting

### "Warning: Skipping malformed line"
The script automatically skips invalid JSON lines in existing files. This is safe and the script will write clean output.

### Duplicate entries
The script uses `id` as the unique key. If the same `id` appears in multiple sources, the script keeps the version with:
1. More recent timestamp
2. Non-pending status (preferred over pending)

### Missing fields
Entries without `id` or `title` are skipped. Check source files for these required fields.

## Related Documentation

- **LAPTOP_SETUP.md**: Dashboard setup and data file locations
- **doc/agent_session_recovery.md**: Agent lifecycle and backlog usage
- **MASTER_BACKLOG.md**: Human-readable backlog consolidation
- **scripts/append_todo.py**: Add individual todo items
- **agents/sync_backlog_to_db.py**: Sync archive to database

## Schema Reference

Standard todo-archive entry format:

```json
{
  "id": "T001",
  "title": "Task title",
  "description": "Optional detailed description",
  "status": "pending",
  "priority": "high",
  "est_hours": 2.0,
  "added_at": "2026-02-06T12:00:00Z",
  "source": "sprints/session_sprint_20260206.json",
  "epic": "Optional epic name",
  "feature": "Optional feature name",
  "story": "Optional story description"
}
```

Required fields: `id`, `title`, `status`, `priority`, `est_hours`, `added_at`, `source`
