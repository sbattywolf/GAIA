# GAIA — Local CLI-first Agent Orchestration

Quick start notes and run steps for Windows (PowerShell).

<<<<<<< HEAD
## 📊 NEW: Project Dashboard

**Run the GAIA dashboard on your laptop!** View project statistics, tasks, and agent status in your web browser.

### Quick Start (3 commands)
```bash
cd /path/to/GAIA
python scripts/verify_setup.py          # Check your setup
python scripts/dashboard_server.py      # Start the dashboard
# Open browser to: http://localhost:8080/dashboard
```

**Or use the one-click launcher:**
```bash
python scripts/launch_dashboard.py      # Auto-opens browser
```

**For complete laptop setup instructions, see:** [LAPTOP_SETUP.md](LAPTOP_SETUP.md)

**Key Features:**
- ✅ Runs completely on your laptop (Windows, Mac, Linux)
- ✅ No external dependencies (Python 3.10+ only)
- ✅ Shows local project data from `doc/todo-archive.ndjson`
=======
## 📊 NEW: Enhanced Multi-View Dashboard

**Multiple perspectives on your project!** Choose between Standard and Enhanced dashboards with 6 specialized views.

### Quick Start
```bash
cd /path/to/GAIA
# Standard dashboard (simple, fast)
python scripts/dashboard_server.py
# Open: http://localhost:9080/dashboard

# Enhanced dashboard (multiple views)
python scripts/launch_enhanced_dashboard.py
# Auto-opens: http://localhost:9080/enhanced
```

### Available Views

#### Standard Dashboard
- 📊 Overview with metrics
- 📋 Task table with filters
- 🤖 Agent status
- 📈 Basic timeline

#### Enhanced Dashboard (NEW!)
- 📊 **Overview** - Key metrics and progress
- 📋 **Kanban Board** - Visual workflow (Pending → In Progress → Completed)
- 🗺️ **Roadmap** - Sprint/milestone timeline
- 📈 **Gantt Timeline** - Progress bars for tasks
- 📅 **Calendar** - Monthly view with deadlines
- 📊 **Metrics** - Analytics and charts

### Enrich Your Data
```bash
# Add sprint, milestone, and deadline data to tasks
python scripts/enrich_sample_data.py --preview  # Preview changes
python scripts/enrich_sample_data.py            # Apply changes
```

**Key Features:**
- ✅ Runs completely on your laptop (Windows, Mac, Linux)
- ✅ No external dependencies (Python 3.10+ only)
- ✅ 6 specialized views for different workflows
>>>>>>> f9cfb76b837e2e31b0c3e4f6dc4d476459fc8b2f
- ✅ Real-time statistics and progress tracking
- ✅ Mobile-responsive web interface

**Documentation:**
- [LAPTOP_SETUP.md](LAPTOP_SETUP.md) - Detailed laptop setup guide
<<<<<<< HEAD
- [scripts/QUICKSTART.md](scripts/QUICKSTART.md) - 60-second quick start
- [doc/DASHBOARD_README.md](doc/DASHBOARD_README.md) - Complete dashboard docs
=======
- [doc/DASHBOARD_README.md](doc/DASHBOARD_README.md) - Standard dashboard
- [doc/DASHBOARD_ENHANCED_README.md](doc/DASHBOARD_ENHANCED_README.md) - Enhanced dashboard (NEW!)
- [scripts/QUICKSTART.md](scripts/QUICKSTART.md) - 60-second quick start

## 🔗 GitHub Projects Integration

**GAIA integrates with GitHub Projects V2!** Automatically add issues to your project board.

### Quick Setup (3 steps)
1. Create a GitHub Project at https://github.com/users/YOUR_USERNAME/projects
2. Add `PROJECT_V2_NUMBER` secret to repository settings
3. Label issues with `sprint/*` to auto-add them to your project

### Check Integration Status
```bash
python scripts/setup_github_projects.py check
```

### Sync Backlog to GitHub Issues
```bash
# Dry-run (safe preview)
python agents/github_sessions_sync.py --dry-run

# Live sync (requires AUTOMATION_GITHUB_TOKEN)
export AUTOMATION_GITHUB_TOKEN="your_token_here"
export AUTOMATION_GITHUB_REPOSITORY="owner/repo"
python agents/github_sessions_sync.py
```

**Full Documentation:** [doc/GITHUB_PROJECTS_INTEGRATION.md](doc/GITHUB_PROJECTS_INTEGRATION.md)
>>>>>>> f9cfb76b837e2e31b0c3e4f6dc4d476459fc8b2f

---

## Requirements
- Git
- GitHub CLI (`gh`) — optional but used by agents
- Python 3.10+ and `venv`
- Bitwarden CLI (`bw`) — optional for secret storage

## Setup
1. Create and activate a venv (from the repository root):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure secrets using the GAIA secrets manager (recommended):

```powershell
# Set your automation GitHub token (for API access with 2FA)
python scripts/secrets_cli.py set AUTOMATION_GITHUB_TOKEN your_token_here

# Set Telegram credentials (if using Telegram integration)
python scripts/secrets_cli.py set TELEGRAM_BOT_TOKEN your_bot_token
python scripts/secrets_cli.py set TELEGRAM_CHAT_ID your_chat_id

# Validate setup
python scripts/secrets_cli.py validate AUTOMATION_GITHUB_TOKEN
```

**OR** copy `.env.example` to `.env` and add your secrets (less secure):

```powershell
copy .env.example .env
# Edit .env to add tokens (keep this file out of git!)
```

See [Secrets Management Guide](doc/SECRETS_MANAGEMENT_GUIDE.md) for details.

3. Recommended: add `.venv` and `.env` to `.gitignore` (if not present).

## Session workflow (typical)

Start a development session (loads `.env`, activates venv):

Free-software install sequence (recommended)
-------------------------------------------

The project prefers only free/open-source software. If a required tool is
non-free, a proposal will be raised before using it.

Recommended install order (Windows PowerShell):

1. Install Git (free, open-source): https://git-scm.com/
2. Install Python 3.10+ (free, open-source): https://www.python.org/
3. Create and activate a virtualenv:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

4. Install runtime deps:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Install developer tools (free):

```powershell
pip install -r requirements-dev.txt
```

6. Install GitHub CLI (free) if you want `gh` integration:

Windows MSI: https://github.com/cli/cli/releases

7. (Optional) Install Docker (free) for reproducible runs: https://www.docker.com/

Environment setup:

```powershell
copy .env.example .env
# edit .env to add API tokens (only when needed)
```

If any step requires non-free software, the project will surface a short
proposal describing the need and alternative free options.
```powershell
.\scripts\start_session.ps1
```

If you only need to load environment variables without the full start routine:

```powershell
. .\scripts\load_env.ps1
```

Run the secret demo (exports a secret into session environment):

```powershell
.\scripts\secret_demo.ps1
```

Check or install required desktop tooling:

```powershell
.\scripts\install_workbook.ps1
```

Append a todo to the audit log:

```powershell
python .\scripts\append_todo.py "Title" --description "details"
```

## Publishing / remote
The repository remote has been created and pushed to:

https://github.com/sbattywolf/GAIA

If you need me to change visibility or create an organization-owned remote, tell me the owner and visibility and I can run `gh repo create`.

## Notes
- Agents use `gh` to create issues; if you don't want that, run in `PROTOTYPE_USE_LOCAL_EVENTS=1` mode or remove the `gh` calls.
- Secrets are managed using the GAIA secrets manager (see [Secrets Management Guide](doc/SECRETS_MANAGEMENT_GUIDE.md))
  - Encrypted storage by default
  - Supports token rotation with automatic backup
  - Works with environment variables, `.env` files, and Bitwarden
- For GitHub 2FA users: see [GitHub 2FA Guide](doc/GITHUB_2FA_GUIDE.md) for token management

Periodic Telegram summary
-------------------------

This repository includes a scheduled GitHub Action that posts a short status summary to Telegram every 30 minutes. The workflow is `.github/workflows/notify-telegram-summary.yml` and expects repository secrets named `GAIA_TELEGRAM_BOT_TOKEN` and `GAIA_TELEGRAM_CHAT_ID` (preferred). The action falls back to the legacy `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` names if present.

Testing note (local):

- A small test case `FAKE_ONREPLY_TEST_2026` was added on 2026-02-03 to `.tmp/pending_commands.json` (id: `fa1cde9e-1234-4bcd-8f1a-0fa1cde00001`). It's marked as a test (`options.is_test = true`) and can be used to validate that on-reply handlers, the monitor UI `Mark as Test` flag, and Telegram inline-button flows keep the original task name when routing approvals and subsequent actions.

To view pending commands quickly:

```powershell
python -c "from scripts.tg_command_manager import list_pending; import json; print(json.dumps(list_pending(), indent=2)[:2000])"
```

Run the lightweight monitor UI (one-liner):

```powershell
python -m scripts.monitor_server --host 127.0.0.1 --port 8080
# then open http://127.0.0.1:8080 in your browser
```

---
Small, focused README — expand when you want more usage examples or diagrams.
# GAIA — Agent-First Backlog Orchestrator (scaffold)

This repo is a CLI-first scaffold for the GAIA project: agents that manage backlog items via CLIs and emit NDJSON events for a realtime UI.

Quickstart (Windows):

1. Create and activate venv:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure `gh` (GitHub CLI) or `glab` (GitLab CLI) for your account.

3. Run the backlog agent (example):

```powershell
python agents/backlog_agent.py --title "Example story" --body "Created by GAIA"
```

Files of interest:
- `agents/backlog_agent.py` — CLI wrapper to create issues via `gh` and write NDJSON events to `events.ndjson`.
- `orchestrator.py` — small service entrypoint (stub).
- `events.ndjson` — event log appended by agents.
 - `scripts/claim_cli.py` — small operator CLI to inspect/claim/release/refresh file-backed claims used by agents.

Claim CLI examples
- Inspect a claim (prints JSON):

```powershell
python scripts/claim_cli.py inspect my_story default
```

- Acquire a claim:

```powershell
python scripts/claim_cli.py claim my_story default operator-joe agent-1 fp-123
```

## Plans & Approval workflow

See [PLAN.md](PLAN.md) for the short-term minisprint plan and next steps.
See [doc/AGENT_APPROVAL_WORKFLOW.md](doc/AGENT_APPROVAL_WORKFLOW.md) for the formal CHECKPOINT approval procedure.

- Release a claim:

```powershell
python scripts/claim_cli.py release my_story default --agent agent-1
```

The CLI returns JSON to stdout and uses exit code 0 for success, non-zero for failures. See `tests/test_claim_cli.py` for a small example test.

License: MIT (add if desired)

## Development & Testing

Quick dev setup (Windows PowerShell):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run tests:

```powershell
pytest -q
```

Run a single agent in dry-run mode to avoid side effects:

```powershell
set PROTOTYPE_USE_LOCAL_EVENTS=1
python agents/backlog_agent.py --title "Test" --body "dry" --dry-run
python agents/alby_agent.py --cmd "echo hi" --concurrency 2 --dry-run
```

Use `.env` (see `.env.example`) for operator-provided secrets; prefer `ALBY_INTERNET_TOKEN` or project-specific `CI_TOKEN` names. Do not commit secrets.

### Pre-commit (recommended)

We use `pre-commit` locally to run quick checks and `detect-secrets` before commits.

Install and enable the hooks:

```bash
pip install pre-commit detect-secrets
pre-commit install
```

Once installed, `pre-commit` will run on each commit and prevent accidental secret commits (based on `.secrets.baseline`). If you update the baseline intentionally, run:

```bash
detect-secrets scan > .secrets.baseline
git add .secrets.baseline && git commit -m "chore: update detect-secrets baseline"
```


Secrets testing and unhappy-paths
--------------------------------

The repository includes guidance and templates for testing secret-related failure modes locally. See `doc/SECRETS_TESTING.md` for recommended workflows (invalid/revoked tokens, wrong chat id, network outages). Use `.tmp/test_secrets/invalid_tokens.env.template` as a starting point for reproducible demos.

Telegram summary setup: see [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md) for testing and repository secret steps.

Telegram improvements trace
--------------------------

For a full trace of the Telegram integration work (enqueue/approval/inline buttons/monitor UI), see `doc/TELEGRAM_IMPROVEMENTS.md`.

Auto-merge opt-in (convenience)
--------------------------------

The repository supports an opt-in auto-merge flow to speed merges for small, reviewed PRs. To opt a PR into auto-merge:

- Add the label `automerge` to the PR.
- Ensure at least one reviewer (who is not the PR author) approves the PR.
- Wait for all CI checks and check-runs to pass.

When those conditions are met the GitHub Actions workflow `.github/workflows/auto-merge.yml` will automatically squash-merge the PR.

If you prefer stricter controls (two approvals, team approvals, or label gating), update `.github/workflows/auto-merge.yml` or contact maintainers.

See `docs/AUTOMERGE.md` for full details and branch-protection recommendations.
