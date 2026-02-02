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
