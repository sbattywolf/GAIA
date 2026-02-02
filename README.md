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
