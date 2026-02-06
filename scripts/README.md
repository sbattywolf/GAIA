# GAIA Scripts Directory

This directory contains utility scripts and agents for the GAIA project.

## Quick Start Scripts

### Setup & Environment

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup_dev_env.py` | **Automated environment setup** - Creates venv, installs deps, configures secrets, validates setup | `python scripts/setup_dev_env.py` |
| `health_check.py` | **Environment validation** - Checks Python, dependencies, Git, config files, project components | `python scripts/health_check.py` |
| `quick_start.ps1` | **Windows quick start** - One-command setup for PowerShell | `.\scripts\quick_start.ps1` |
| `quick_start.sh` | **Unix/Linux quick start** - One-command setup for bash | `./scripts/quick_start.sh` |

### Development Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `load_context.py` | **Context loader** - Loads session state, backlog, events, and generates comprehensive summary | `python scripts/load_context.py` |
| `start_session.ps1` | **Session starter** - Loads .env, activates venv, tails events | `.\scripts\start_session.ps1` |
| `load_env.ps1` | **Environment loader** - Loads .env variables into PowerShell session | `. .\scripts\load_env.ps1` |

### Secrets Management

| Script | Purpose | Usage |
|--------|---------|-------|
| `secrets_cli.py` | **Secrets manager** - Set, get, validate secrets with encryption | `python scripts/secrets_cli.py set KEY value` |
| `secret_demo.ps1` | **Secret demo** - Demonstrates secret export to environment | `.\scripts\secret_demo.ps1` |

### Task & Workflow Management

| Script | Purpose | Usage |
|--------|---------|-------|
| `append_todo.py` | **Todo appender** - Adds items to audit log | `python scripts/append_todo.py "Title" --description "details"` |
| `approval_listener.py` | **Approval listener** - Monitors Telegram for approvals | `python scripts/approval_listener.py --poll` |
| `monitor_server.py` | **Monitor UI** - Lightweight web UI for events and tasks | `python -m scripts.monitor_server --port 8080` |

## Common Workflows

### Initial Setup (First Time)

**Windows PowerShell:**
```powershell
# Quick setup
.\scripts\quick_start.ps1

# Or manual setup
python scripts/setup_dev_env.py
.\.venv\Scripts\Activate.ps1
```

**Unix/Linux:**
```bash
# Quick setup
./scripts/quick_start.sh

# Or manual setup
python3 scripts/setup_dev_env.py
source .venv/bin/activate
```

### Start Development Session

**Every session:**
```powershell
# Load environment and context
.\scripts\start_session.ps1

# Or just activate venv and load context
.\.venv\Scripts\Activate.ps1
python scripts/load_context.py
```

### Check Environment Health

```powershell
python scripts/health_check.py
```

This validates:
- Python version (3.10+)
- Virtual environment
- Dependencies
- Git and GitHub CLI
- Configuration files
- Project structure

### Load Project Context

```powershell
python scripts/load_context.py
```

This generates:
- Current session state
- Project structure analysis
- Backlog items summary
- Recent events
- Recommendations

Output saved to: `.tmp/context_summary_YYYYMMDD_HHMMSS.md`

### Manage Secrets

```powershell
# Set a secret (encrypted storage)
python scripts/secrets_cli.py set GITHUB_TOKEN your_token_here

# Get a secret
python scripts/secrets_cli.py get GITHUB_TOKEN

# Validate a secret
python scripts/secrets_cli.py validate GITHUB_TOKEN

# List all secrets
python scripts/secrets_cli.py list
```

## Agent Scripts

The `agents/` directory contains CLI-first agent scripts that:
- Execute actions (create issues, run commands, etc.)
- Emit NDJSON events to `events.ndjson`
- Follow standard patterns (click CLI, event emission)

Example agent usage:
```powershell
python agents/backlog_agent.py --title "Example" --body "Created by GAIA"
```

See `.github/copilot-instructions.md` for agent development patterns.

## Development with GitHub Copilot

For detailed Copilot setup and usage, see:
- **Setup Guide:** `doc/01_onboarding/copilot-local-setup.md`
- **Workspace Config:** `.github/copilot-workspace.yml`
- **Agent Instructions:** `.github/copilot-instructions.md`

Quick Copilot workflow:
1. Run `python scripts/setup_dev_env.py` (first time)
2. Run `python scripts/load_context.py` (each session)
3. Open project in VSCode with Copilot enabled
4. Start coding with context-aware suggestions

## Troubleshooting

### Environment Issues

Run health check:
```powershell
python scripts/health_check.py
```

Re-run setup if needed:
```powershell
python scripts/setup_dev_env.py
```

### Missing Dependencies

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Secrets Not Loading

Check `.env` file exists and has content:
```powershell
Get-Content .env
```

Or use encrypted secrets manager:
```powershell
python scripts/secrets_cli.py list
```

### GitHub CLI Not Authenticated

```powershell
gh auth login
gh auth status
```

## Script Development

When creating new scripts:

1. **Place in appropriate directory:**
   - `scripts/` for utilities and tools
   - `agents/` for CLI agents that emit events

2. **Follow conventions:**
   - Use `click` for CLI interfaces (agents)
   - Add docstrings and help text
   - Handle errors gracefully
   - Return appropriate exit codes

3. **For agents, follow the pattern:**
   - Parse CLI args
   - Execute action (GitHub, file ops, etc.)
   - Append event to `events.ndjson`
   - Use `append_event()` helper

4. **Add to this README** if it's a utility script

See `agents/backlog_agent.py` for canonical agent pattern.

## Additional Resources

- **Main README:** `../README.md` - Project overview
- **Session Guide:** `../README_SESSION.md` - Session workflows
- **Copilot Guide:** `../doc/01_onboarding/copilot-local-setup.md` - Copilot setup
- **Technical Docs:** `../doc/02_technical/` - Architecture details
- **Secrets Guide:** `../doc/SECRETS_MANAGEMENT_GUIDE.md` - Secrets management

## Getting Help

For issues or questions:
1. Run `python scripts/health_check.py` to diagnose problems
2. Check relevant documentation in `doc/`
3. Review `.github/copilot-instructions.md` for patterns
4. Ask GitHub Copilot for help with specific tasks
