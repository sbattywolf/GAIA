# Backlog Builder - Minimum Requirements

## Problem Statement
Create a local agent that:
- Takes input from Telegram
- Creates/finds GitHub projects
- Generates backlog items (tasks, stories, features)
- Dockerized, uses free tools
- Suitable for home infrastructure (1 PC + NAS)

## Existing GAIA Components That Already Do This

### Telegram Input (ALREADY EXISTS)
- `scripts/telegram_client.py` - Telegram API wrapper
- `scripts/tg_command_manager.py` - Command parsing and queueing
- `.tmp/pending_commands.json` - Command queue

### GitHub Integration (ALREADY EXISTS)
- `agents/backlog_agent.py` - Creates GitHub issues via `gh` CLI
- Uses `gh issue create` - FREE TOOL, already installed

### Task Queue (ALREADY EXISTS)
- `orchestrator.py` - SQLite-based task queue
- `enqueue_task()`, `claim_task()`, `complete_task()`

### Event System (ALREADY EXISTS)
- `events.ndjson` - Event log
- `agents/agent_utils.py` - Event builders

## What's Missing

1. **Command handler** for `/backlog` in tg_command_manager
2. **Pattern file** to parse requirements text
3. **Worker script** to process queue items
4. **Dockerfile** for containerization

## Proposed Solution (Configuration-Driven)

### File 1: `backlogs/parse_rules.json`
```json
{
  "extract_items": [
    {"pattern": "^\\s*[-*•]\\s+(.+)$", "type": "bullet"},
    {"pattern": "^\\s*\\d+[.)]\\s+(.+)$", "type": "numbered"}
  ],
  "classify": {
    "story": ["as a", "user can", "i want"],
    "task": ["setup", "configure", "deploy"],
    "spike": ["research", "investigate"]
  }
}
```

### File 2: `scripts/process_backlog_queue.sh`
Reads queue, applies rules, calls existing `agents/backlog_agent.py`

### File 3: `docker-compose.backlog.yml`
Standard docker-compose using python:3.12 + gh CLI

## Integration Points

```
User → Telegram
  ↓ (existing: telegram_client.py)
tg_command_manager.py detects "/backlog"
  ↓ (add 10 lines to command registry)
orchestrator.enqueue_task()
  ↓ (existing queue)
process_backlog_queue.sh (NEW, 20 lines)
  ↓ reads parse_rules.json
  ↓ calls existing backlog_agent.py for each item
GitHub Issues created
```

## Complexity: MINIMAL

- Config file: ~20 lines JSON
- Shell script: ~20 lines bash
- Dockerfile: ~10 lines
- Integration hook: ~10 lines added to tg_command_manager.py

Total new code: ~60 lines
Reuses: 90% of GAIA's existing infrastructure

## Free Tools Used

- gh (GitHub CLI) - FREE
- docker - FREE
- python + sqlite - FREE  
- GitHub Projects - FREE tier sufficient
- Telegram Bot API - FREE

## Home Infrastructure Suitability

- Runs on single machine
- No external services required
- SQLite for persistence (local file)
- Can run on NAS via docker-compose
- Low memory footprint (<100MB)

## Next Step

Should I:
A) Create the 4 minimal files described above?
B) Just add integration points to existing files?
C) Something else?
