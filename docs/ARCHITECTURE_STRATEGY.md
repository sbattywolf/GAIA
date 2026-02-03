# Architecture & Strategy
This document captures the current GAIA / Alby prototype architecture, runtime expectations, and an Alby 0.3 requirements + install plan for local development.

## Current architecture (summary)
- Monitor: `monitor/app.py` — Flask UI that tails `events.ndjson`, serves `/api/*` endpoints, and renders `monitor/templates/index.html`.
- Supervisor: `scripts/monitor_supervisor.py` — spawns and health-checks the monitor process, writes child PID to `.tmp/monitor_pid.txt`.
- Events: `events.ndjson` — append-only NDJSON event log agents and the UI use as a primary trace stream.
- Agents: CLI-first agents under `agents/` that emit NDJSON events and optionally create GitHub issues via `gh` (prototype pattern in `agents/backlog_agent.py`).
- Audit DB: `gaia.db` — SQLite used to persist small state (now used to persist instruct rate counters).

## Alby 0.3 — Requirements & Local Install Plan
Purpose: define the minimal environment and a reproducible bootstrap to run GAIA/Alby 0.3 locally for development and demos.

Requirements
- OS: Windows (PowerShell recommended) or macOS/Linux (bash). Development tested on Windows.
- Python: 3.11+ (use a venv). Ensure the Python used by the supervisor and monitor has the packages in `requirements.txt` installed.
- GitHub CLI: `gh` (optional but used by `agents/backlog_agent.py`). Authenticate with `gh auth login` if you want issues created remotely.
- PowerShell (pwsh) recommended for agent start/stop scripts. Plain `powershell` works but `pwsh` is preferred.
- SQLite: bundled with Python — used for `gaia.db`.
- Optional: Bitwarden CLI (`bw`) if you plan to store secrets locally during development.

Environment variables
- `GAIA_EVENTS_PATH` — path to `events.ndjson` (default repo root `events.ndjson`).
- `GAIA_DB_PATH` — path to `gaia.db` (default repo root `gaia.db`).
- `GAIA_AGENTS_CONFIG` — path to `agents.json` to control agent aliases/match tokens.
- `PROTOTYPE_USE_LOCAL_EVENTS` — set to `1` to force local-only event handling (avoid remote calls).
- `GAIA_INSTRUCT_API_KEY` — optional API key for `/api/agents/instruct`.
- `GAIA_INSTRUCT_RATE_LIMIT` / `GAIA_INSTRUCT_RATE_WINDOW_SECONDS` — rate limiting config.

Install / bootstrap (PowerShell)
1) Create venv and activate
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2) Install requirements
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3) (Optional) Install `gh` CLI and authenticate
```powershell
# follow platform instructions; then
gh auth login
```
4) Start monitor (dev)
```powershell
# run from repo root
python monitor/app.py --host 127.0.0.1 --port 5000
```
5) Supervise (preferred)
```powershell
# uses the supervisor script
python scripts/monitor_supervisor.py
```

Install / bootstrap (bash)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python monitor/app.py --host 127.0.0.1 --port 5000
```

Quick verification
- UI: open http://127.0.0.1:5000/ in a browser.
- Health check: `curl http://127.0.0.1:5000/api/agents/status` should return JSON.
- Events: append a sample event and confirm the UI shows it:
```bash
echo '{"type":"test","source":"local","payload":{"msg":"hello"},"timestamp":"2026-02-02T00:00:00Z"}' >> events.ndjson
```

Security & hardening notes
- Do not bind the monitor to 0.0.0.0 in an untrusted network. Keep `--host=127.0.0.1` unless explicitly exposing.
- Use `GAIA_INSTRUCT_API_KEY` for simple auth on the instruct endpoint; store keys outside Git and prefer a `.env` or secret manager.
- Avoid committing `agents.json` with secret tokens or credentials.

Operational notes
- Events are append-only NDJSON; agents should append one JSON object per line and avoid rewriting `events.ndjson`.
- `out/status.json` is a convention for agent-provided status; the monitor reads it if present.
- Supervisor should run under an interpreter that has Flask installed; prefer the repo `.venv` Python.

Acceptance checklist for local Alby 0.3 dev
- [ ] `python monitor/app.py` serves UI and `/api/agents/summary`
- [ ] `scripts/monitor_supervisor.py` can start/monitor the child and writes `.tmp/monitor_pid.txt`
- [ ] `agents/backlog_agent.py` can run in `--dry-run` and append local events without remote calls when `PROTOTYPE_USE_LOCAL_EVENTS=1`
- [ ] `GAIA_INSTRUCT_API_KEY` rate-limited instruct endpoint works; counters persist across restarts
- [ ] `agents.json` examples cover common agent aliases and allow reliable event->agent attribution

Where to go next
- Finalize `scripts/install_env.ps1` and `scripts/install_env.sh` to automate steps above.
- Create `docs/ALBY_0.3_REQUIREMENTS.md` if you want a dedicated file; otherwise this section lives in `docs/ARCHITECTURE_STRATEGY.md`.
- Finish GUI deliverables (wire `Start Agents`, agent drilldowns, `agents.json` editor) and add a short runbook `README.rundown.md` describing common developer tasks.

---
Updated: automated draft of Alby 0.3 requirements and bootstrap plan added to this document.

# Architecture Strategy & Migration Plan

This document captures the recommended incremental strategy for GAIA: start
simple with standalone CLI-first agents, harden agents for future
orchestration, and only introduce a central controller (`orchestrator`) when
coordination needs exceed the benefits of decentralized operation.

Goals
- Deliver useful automation quickly with minimal operational overhead.
- Keep agents small, testable, and easy to run locally.
- Enable an eventual low-ops controller without rewriting agents.

High-level approach
1. Start-simple (no controller):
   - Agents are CLI scripts under `agents/` that perform work and append
     structured events to `events.ndjson` using `agent_utils.build_event()`.
   - Agents must support `--dry-run` and `PROTOTYPE_USE_LOCAL_EVENTS=1` to
     avoid external side-effects during development and CI.

2. Harden agents for orchestration:
   - Ensure idempotency: include an `idempotency_key` for actions derived from
     event content.
   - Add retry helpers and clear non-zero exit codes for transient failures.
   - Emit concise audit rows to SQLite when actions change state.

3. Monitor & apply switch criteria:
   - If agents begin to require distributed locking, global rate-limits,
     multi-step transactional workflows, or centralized retry/deduplication,
     introduce an `orchestrator`.

4. Minimal orchestrator (when needed):
   - A low-ops Python process that consumes `events.ndjson` (or a webhook),
     stores tasks in SQLite, and runs handlers with retries and dedup logic.
   - Controller exposes a small health endpoint and reads config from `.env`.
   - Keep agent CLIs unchanged; controller should invoke CLIs or call
     handlers that reuse agent libraries.

Trade-offs
- Starting simple: faster iteration, lower maintenance cost, but harder to
  coordinate complex cross-agent flows later.
- Controller-first: more upfront work and ops cost but simplifies complex
  orchestration early.

Switch Criteria (introduce controller when any applies)
- Need for distributed locking or global concurrency limits.
- Cross-agent transactional workflows where partial failures require
  coordinated rollbacks or compensating actions.
- High rate of duplicate or conflicting events that require deduplication.

Stepwise migration plan
1. Immediately: Harden agents (idempotency helpers, retry helper, clear
   dry-run semantics). Update tests.
2. Short-term (next sprint): Add a lightweight 'monitor' script that scans
   `events.ndjson` and reports metrics (event rate, error rate, duplicates).
3. Medium-term: Scaffold a minimal `orchestrator` that consumes events into a
   SQLite-backed queue with simple retry/dedup logic.
4. Long-term: If scale or performance warrants, migrate persistence to
   Redis/Postgres and add robust observability (metrics, traces).

Future todos (suggested)
- Add a `monitor_events.py` to compute event metrics and thresholds.
- Add a small `orchestrator` scaffold (SQLite-backed) with a pluggable handler
  registry.
- Add per-agent integration tests that run an end-to-end flow within a temp
  workspace.

Conclusion
Start simple and harden agents first — low effort, immediate value, and a
clear migration path to a minimal orchestrator when real coordination needs
arise.
