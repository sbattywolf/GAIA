# GAIA — Local CLI-first Agent Orchestration

Quick start notes and run steps for Windows (PowerShell).

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

2. Copy or create a `.env` from `.env.example` and keep local secrets out of git.

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
- Keep secrets in Bitwarden or `.env`; avoid committing secrets.

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

Secrets testing and unhappy-paths
--------------------------------

The repository includes guidance and templates for testing secret-related failure modes locally. See `doc/SECRETS_TESTING.md` for recommended workflows (invalid/revoked tokens, wrong chat id, network outages). Use `.tmp/test_secrets/invalid_tokens.env.template` as a starting point for reproducible demos.

Telegram improvements trace
--------------------------

For a full trace of the Telegram integration work (enqueue/approval/inline buttons/monitor UI), see `doc/TELEGRAM_IMPROVEMENTS.md`.
