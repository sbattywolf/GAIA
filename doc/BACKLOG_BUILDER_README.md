# Backlog Builder for GAIA

A minimal, configuration-driven solution for creating GitHub backlogs from Telegram messages.

## Features

- 🤖 **Telegram Integration**: Send requirements via `/backlog` command
- 📋 **GitHub Issues**: Auto-create issues with proper labeling
- 🏷️ **Smart Classification**: Stories, tasks, spikes, features
- 🐳 **Dockerized**: Run on any machine (PC, NAS)
- 💰 **100% Free Tools**: No paid services required
- 🔄 **Scrum-Ready**: Labels for sprints, story points

## Quick Start

### 1. Configure Environment

```bash
cp .env.example .env
# Add your tokens:
# TELEGRAM_BOT_TOKEN=...
# GH_TOKEN=... (or use `gh auth login`)
```

### 2. Test Locally

```bash
# Create an issue using existing agent
python -m agents.backlog_agent \
  --title "[FEATURE] User authentication" \
  --body "Implement user login system"

# Check result
gh issue list --label gaia-generated
```

### 3. Run via Docker

```bash
docker-compose -f docker-compose.backlog.yml up -d
```

## Usage Examples

### Command Line

```bash
# Process example requirements
cat examples/backlog_todo_app.txt
# Use existing agent for each item

# Queue via orchestrator
python -c "
from orchestrator import enqueue_task
enqueue_task('backlog_item', {
  'title': 'Setup CI/CD', 
  'body': 'Configure GitHub Actions'
})
"
```

### Via Telegram

Send message to bot:
```
/backlog Build an e-commerce platform:
- User registration
- Product catalog
- Shopping cart
- Payment integration
- Setup hosting infrastructure
- Research payment providers
```

Results in GitHub issues:
- `[STORY] User registration`
- `[FEATURE] Product catalog`
- `[FEATURE] Shopping cart`
- `[FEATURE] Payment integration`
- `[TASK] Setup hosting infrastructure`
- `[SPIKE] Research payment providers`

## Architecture

```
┌─────────────┐
│  Telegram   │
│   Message   │
└──────┬──────┘
       │
       ├─── scripts/telegram_client.py (exists)
       │
       ▼
┌─────────────────┐
│ Command Queue   │ (.tmp/pending_commands.json)
└────────┬────────┘
         │
         ├─── scripts/tg_command_manager.py (exists)
         │
         ▼
┌─────────────────┐
│  Orchestrator   │ (orchestrator.py - SQLite queue)
└────────┬────────┘
         │
         ├─── Pattern matching (backlogs/pattern_to_category.txt)
         │
         ▼
┌─────────────────┐
│ Backlog Agent   │ (agents/backlog_agent.py - exists)
└────────┬────────┘
         │
         ├─── gh CLI (GitHub CLI - free tool)
         │
         ▼
┌─────────────────┐
│ GitHub Issues   │
└─────────────────┘
```

## Files

### Configuration
- `backlogs/pattern_to_category.txt` - Classification rules
- `docker-compose.backlog.yml` - Container setup

### Examples
- `examples/backlog_todo_app.txt` - Sample requirements

### Documentation
- `doc/BACKLOG_BUILDER_QUICKSTART.md` - Getting started
- `doc/BACKLOG_BUILDER_WIRING_GUIDE.md` - Integration details
- `doc/BACKLOG_BUILDER_IMPLEMENTATION_SUMMARY.md` - Full summary

## Pattern Matching

The system classifies items using keywords:

| Pattern | Issue Type |
|---------|------------|
| `as a...i want` | Story |
| `user can` | Story |
| `setup`, `configure`, `deploy` | Task |
| `research`, `investigate` | Spike |
| Everything else | Feature |

## Home Infrastructure

Perfect for:
- Single PC setup
- Home NAS (Synology, QNAP, etc.)
- Raspberry Pi
- Local development machine

Requirements:
- Docker or Python 3.10+
- GitHub CLI (`gh`)
- 100MB RAM
- Minimal CPU

## Free Tools Stack

- **GitHub CLI (gh)**: Issue creation - FREE
- **Docker**: Containerization - FREE
- **Python + SQLite**: Processing & queue - FREE
- **GitHub Projects**: Visualization - FREE tier
- **Telegram Bot API**: Input interface - FREE

## Integration Status

✅ **Working Now**:
- Orchestrator queue
- Backlog agent (creates issues)
- Pattern mapping
- Docker configuration
- Documentation

🔲 **To Complete** (~20 lines):
- Wire `/backlog` command in `tg_command_manager.py`
- Parse text using pattern file
- Loop over items calling backlog agent

## Testing

```bash
# Test orchestrator
python -c "from orchestrator import enqueue_task; \
  tid = enqueue_task('test', {}); \
  print(f'Task {tid} created')"

# Test backlog agent
python -m agents.backlog_agent \
  --title "Test issue" \
  --body "Test body" \
  --dry-run

# Test docker compose
docker-compose -f docker-compose.backlog.yml config
```

## Troubleshooting

```bash
# Check queue status
python -c "from orchestrator import list_tasks; \
  print(list_tasks('pending'))"

# Check events
tail -20 events.ndjson

# Test telegram
python scripts/check_telegram_connectivity.py

# View docker logs
docker-compose -f docker-compose.backlog.yml logs
```

## License

Part of GAIA project - MIT License

## See Also

- [GAIA Main README](../README.md)
- [Orchestrator Documentation](../orchestrator.py)
- [Telegram Integration](../scripts/telegram_client.py)
