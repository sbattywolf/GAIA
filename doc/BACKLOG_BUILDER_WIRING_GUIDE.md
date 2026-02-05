# Backlog Builder - Using Existing GAIA Tools

## What Already Exists in GAIA

1. **Telegram integration**: `scripts/telegram_client.py`, `scripts/tg_command_manager.py`
2. **GitHub integration**: `agents/backlog_agent.py` (creates issues via `gh` CLI)
3. **Task queue**: `orchestrator.py` 
4. **Event logging**: `events.ndjson` system

## Solution: Wire Existing Tools Together

### Step 1: User sends Telegram message

```
/backlog Build a todo app:
- User login
- Create todos
- REST API
```

### Step 2: Message lands in existing queue

File: `.tmp/pending_commands.json` (already exists in GAIA)

### Step 3: Process with existing tools

```bash
# Use existing backlog_agent.py (already in GAIA)
python agents/backlog_agent.py --title "[FEATURE] User login" --body "From backlog request"
python agents/backlog_agent.py --title "[FEATURE] Create todos" --body "From backlog request"
python agents/backlog_agent.py --title "[TASK] REST API" --body "From backlog request"
```

### Step 4: Check results

```bash
# Use existing gh CLI
gh issue list --label gaia-generated

# Check events
tail events.ndjson
```

## Files to Create (Data Only)

1. `examples/backlog_todo_app.txt` - Example requirements ✓
2. `backlogs/command_mapping.txt` - Maps patterns to issue types
3. `docker-compose.backlog.yml` - Standard docker compose

## Testing

```bash
# Test existing backlog agent
python agents/backlog_agent.py --title "Test issue" --body "Test" --dry-run

# Test telegram client  
python scripts/telegram_client.py

# Test orchestrator
python -c "from orchestrator import enqueue_task; enqueue_task('test', {})"
```

## Conclusion

**No new code needed** - just wire existing GAIA components:
- Telegram → Command queue (exists)
- Queue → Backlog agent (exists)
- Backlog agent → GitHub (exists)

Only needed: Small glue to detect `/backlog` command and loop over items.
