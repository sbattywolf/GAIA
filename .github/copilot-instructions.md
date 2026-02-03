# Copilot / AI Agent Instructions — GAIA

Purpose
- Help AI coding agents become productive quickly in this repo by documenting the runtime entrypoints, data flows, developer workflows, and repository conventions discovered from source files.

Big picture (what to know first)
- `orchestrator.py`: lightweight service entrypoint that initializes a SQLite audit DB (`gaia.db`). Treat it as the central audit store for actions.
- `agents/`: CLI-first agent scripts. Example: `agents/backlog_agent.py` creates GitHub issues (via `gh`) and appends NDJSON events to `events.ndjson` in the repo root.
- Events stream: `events.ndjson` is the append-only NDJSON event log agents write to. Consumers (UI or prototype SSE server) tail that file.

Key developer workflows
- Setup (Windows PowerShell): create venv and install deps

  ```powershell
  python -m venv .venv
  & .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

- Start a development session (loads `.env` and recommended session setup):

  ```powershell
  .\scripts\start_session.ps1
  ```

- Quick agent run example (creates issue via `gh` and appends event):

  ```powershell
  python agents/backlog_agent.py --title "Example" --body "Created by GAIA"
  ```

- If `gh` is unavailable or you prefer no remote calls, set `PROTOTYPE_USE_LOCAL_EVENTS=1` (handed in README/HANDOFF) to use local-only event handling for development.

Project-specific conventions and patterns
- Agents are CLI wrappers: follow the `backlog_agent.py` pattern — parse args, attempt external action (e.g., `gh`), then append a structured event using `append_event()`.
- Event schema (observed fields): `type`, `source`, `target`, `task_id`, `payload`, `timestamp` (UTC ISO + 'Z'), `trace_id` (UUID). Keep these fields consistent when producing events.
- `target` is typically set as `os.path.basename(os.getcwd())` — use repository working directory to indicate origin.
- Use NDJSON appends (one JSON object per line) to `events.ndjson`. Do not rewrite or reformat that file — always append.
- For audit, `orchestrator.py` creates an `audit` table in SQLite. When implementing actions that change state, also write concise audit records to the DB.

Integration points & external dependencies
- GitHub CLI (`gh`) — used by `agents/backlog_agent.py` to create issues. Agents capture `gh` stdout (issue URL) and include it in event payloads. Avoid assuming a web UI; prefer CLI-first interactions.
- Optional Bitwarden CLI (`bw`) is noted in README for secret storage — do not embed secrets in code; use `.env` or local secret tooling.
- Prototype SSE/monitoring code is referenced in `doc/HANDOFF.md` (paths under `AGENT_TASKS/agent_runtime/...`) if you need to run a local SSE tailer UI for events.

Files to consult when making changes
- `agents/backlog_agent.py` — canonical agent pattern (CLI, external call, NDJSON append).
- `orchestrator.py` — DB/audit initialization and example of persisted audit records.
- `events.ndjson` (repo root) — event sink (tail for debug).
- `doc/HANDOFF.md` and `README.md` — session workflows, environment, and run examples.

Quick debugging tips
- Tail `events.ndjson` to see agent outputs (use any NDJSON tailer or simple `Get-Content -Wait events.ndjson` in PowerShell).
- Run agents locally with `PROTOTYPE_USE_LOCAL_EVENTS=1` to avoid remote side-effects while iterating.
- Re-run `orchestrator.py` to ensure `gaia.db` schema exists before depending on audit writes.

What not to assume
- There is no production deployment configured here — treat the repo as a prototype scaffold.
- Do not assume additional services beyond `gh` or local venv tools unless explicitly added to `requirements.txt` or docs.

If something is unclear
- Ask for the missing runtime detail you need (example: expected event consumer endpoint, or the exact audit columns to populate). Include a one-line summary of the change you plan and a short code diff when asking.

---
Please review and tell me which parts need more examples or exact schemas to be added.
