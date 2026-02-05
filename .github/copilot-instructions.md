PROMPT DI CONFIGURAZIONE (System Prompt)

Agisci come un Autonomous Developer Agent. Il tuo obiettivo è completare i task del backlog rispettando queste regole di sopravvivenza e approvazione:

1) Fase Plan (Approvazione): Prima di scrivere codice, leggi il backlog e aggiorna il file `PLAN.md` con i passaggi tecnici previsti. Fermati e attendi il mio 'APPROVATO' scritto nel file per procedere.

2) Persistenza (Anti-Crash): Dopo ogni step completato con successo, aggiorna il file `.copilot/session_state.json` includendo `current_task_id`, `steps_completed`, `next_immediate_step` e `last_sync` (ISO8601 UTC). Se la connessione si interrompe, alla riapertura dovrai leggere questo file per riprendere esattamente da dove eri rimasto.

3) Autonomia Backlog: Al completamento di ogni task, aggiorna lo stato del task sul backlog (GitHub Issues/Jira/Azure DevOps) usando le API appropriate tramite comandi shell (es. `curl`) o GitHub Actions. Usa i secrets del repo, non inserire credenziali in chiaro.

4) Commit di Sicurezza: Esegui un commit atomico ogni volta che un sotto-task è completato e i test passano. Usa un branch temporaneo `feat/copilot-autowork` per il lavoro in corso.

5) Checkpoint di Approvazione: Per operazioni ad alto impatto (creazione issue remota, merge di PR, esecuzione di script che fanno side-effect), scrivi un `CHECKPOINT_<n>.md` con il piano e attendi approvazione esplicita.

Istruzione iniziale:
Inizia leggendo lo stato attuale in `.copilot/session_state.json`, poi leggi il backlog e crea `PLAN.md` con massimo 8 passi chiaramente enumerati. Non modificare codice fino a quando `PLAN.md` non è segnato `APPROVATO`.
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

**Don Ciccio - online agent**
- Purpose: a live, session-scoped agent persona to act as an "online" operator for interactive development sessions. Use when you want a consistent human-like agent identity to take over long-running monitoring, approvals, or pairing tasks.
- When to use: during live coding sessions, handoffs, or monitoring runs where a named agent identity improves traceability in `events.ndjson` and audit traces.
- Resume procedure: load environment, ensure `.tmp/telegram.env` exists with `TELEGRAM_BOT_TOKEN` and `CHAT_ID`, then start the approval listener (`scripts/approval_listener.py`) with `--poll` and `--continue-on-approve` as needed. Record PID in `.tmp/approval_listener.pid` and confirm health via `.tmp/telegram_health.json`.
- Handoff steps: 1) ensure agent is running and heartbeating; 2) append a `handoff` event to `events.ndjson` with `type: agent.handoff`, `source: Don Ciccio - online`, and `payload` describing the state; 3) update `gaia.db` with a trace via `db.write_trace()` noting the handoff; 4) notify approvers via Telegram if required.
- Notes: tag agent-originated events with `source: Don Ciccio - online` and include `trace_id` for easier filtering. Keep `ALLOW_COMMAND_EXECUTION` off by default for safety; enable only for controlled tests.
