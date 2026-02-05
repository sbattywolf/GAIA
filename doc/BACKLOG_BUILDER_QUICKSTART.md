# Backlog Builder - Quick Start

## Prerequisites

- Docker installed
- GitHub CLI (`gh`) authenticated
- Telegram bot token

## Setup

1. Copy environment variables:
```bash
cp .env.example .env
# Edit .env and add:
# TELEGRAM_BOT_TOKEN=your_token
# TELEGRAM_CHAT_ID=your_chat_id
```

2. Start the worker:
```bash
docker-compose -f docker-compose.backlog.yml up -d
```

## Usage

### Via Telegram

Send message to your bot:
```
/backlog Build a blog platform:
- User authentication
- Create blog posts
- Comment system
- Setup hosting
- Research CDN options
```

### Via Command Line

```bash
# Test parsing example file
cat examples/backlog_todo_app.txt

# Create issues manually using existing agent
python agents/backlog_agent.py \
  --title "[FEATURE] User authentication" \
  --body "From requirements doc"
```

### Check GitHub

```bash
# List created issues
gh issue list --label gaia-generated

# View project board
gh project list
```

## Troubleshooting

```bash
# Check orchestrator queue
python -c "from orchestrator import list_tasks; print(list_tasks())"

# Check events
tail -20 events.ndjson

# Check telegram connectivity
python scripts/check_telegram_connectivity.py
```

## Docker Commands

```bash
# View logs
docker-compose -f docker-compose.backlog.yml logs -f

# Restart
docker-compose -f docker-compose.backlog.yml restart

# Stop
docker-compose -f docker-compose.backlog.yml down
```
