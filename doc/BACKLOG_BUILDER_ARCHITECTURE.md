# Telegram-to-GitHub Backlog Builder for GAIA

## Overview

This document describes how to build a local agent that:
1. Receives requirements via Telegram
2. Creates/finds GitHub projects  
3. Generates backlog items (stories, tasks, features)
4. Can run dockerized on home infrastructure

## Architecture - Using Existing GAIA Components

```
Telegram Bot → scripts/tg_command_manager.py (EXISTS)
                    ↓
            .tmp/pending_commands.json (EXISTS)
                    ↓
            orchestrator.py queue (EXISTS)
                    ↓
            Custom worker (NEW: reads requirements)
                    ↓
            gh CLI → GitHub Issues (FREE TOOL)
```

## Step 1: Configure Telegram Bot (Already in GAIA)

GAIA already has Telegram infrastructure in `scripts/`:
- `telegram_client.py` - API client
- `tg_command_manager.py` - Command processor
- `approval_listener.py` - Approval system

Add new command to `tg_command_manager.py` command registry.

## Step 2: Requirements Parser (Simple Text Processing)

Create `backlogs/requirements_parser.txt` with patterns:
```
BULLET_PATTERN: ^\s*[-*•]\s+(.+)$
NUMBER_PATTERN: ^\s*\d+[.)]\s+(.+)$
STORY_PATTERN: (?i)as a.+i want.+
TASK_KEYWORDS: setup,configure,install,deploy
SPIKE_KEYWORDS: research,investigate,explore
```

Worker script reads these patterns, applies to input text.

## Step 3: GitHub Issue Creator (Use gh CLI - FREE)

Simple loop calling existing `gh` CLI:
```bash
gh issue create --title "[STORY] $item" --body "$details" --label "backlog"
```

GAIA's `agents/backlog_agent.py` already shows this pattern.

## Step 4: Orchestrator Integration

Use existing `orchestrator.py`:
- `enqueue_task('backlog_from_telegram', payload)`
- Worker claims task
- Processes requirements
- Calls gh CLI
- Marks task complete

## Step 5: Docker Setup (FREE)

Create `Dockerfile.backlog`:
```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y gh git
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["python", "scripts/backlog_worker.py"]
```

docker-compose.yml:
```yaml
version: '3.8'
services:
  backlog-worker:
    build:
      context: .
      dockerfile: Dockerfile.backlog
    env_file: .env
    volumes:
      - ./backlogs:/app/backlogs
```

## Step 6: Visualization (FREE - Use GitHub Projects)

GitHub has free project boards:
```bash
gh project create --owner $ORG --title "Backlog"
gh project item-add $PROJECT_ID --url $ISSUE_URL
```

Alternative: Use existing GAIA event stream + simple HTML dashboard reading `events.ndjson`.

## Implementation Files Needed

### 1. `backlogs/patterns.conf` (Pattern matching config)
### 2. `scripts/backlog_worker.py` (Worker that processes queue)
### 3. `Dockerfile.backlog` (Container definition)
### 4. `doc/BACKLOG_BUILDER_GUIDE.md` (This document + usage examples)

## Usage Example

```bash
# User sends to Telegram bot:
/backlog Build todo app:
- User login
- Create todos
- REST API

# Bot saves to .tmp/pending_commands.json
# Orchestrator enqueues task
# Worker processes:
#   1. Parse text → 3 items
#   2. Call: gh issue create [FEATURE] "User login"
#   3. Call: gh issue create [FEATURE] "Create todos"  
#   4. Call: gh issue create [TASK] "REST API"
# Responds: "Created 3 issues in project 'todo-app'"
```

## Advantages of This Approach

- **Minimal code**: Mostly config and bash
- **Uses FREE tools**: gh, docker, GitHub Projects
- **Leverages GAIA**: orchestrator, telegram, events
- **Home-friendly**: Runs on single PC/NAS
- **Scrum-ready**: Label issues with story-points, sprints

## Next Steps

See implementation in:
- `backlogs/patterns.conf` - Pattern definitions
- `scripts/backlog_worker.py` - Queue processor
- `examples/backlog_example.txt` - Sample input
