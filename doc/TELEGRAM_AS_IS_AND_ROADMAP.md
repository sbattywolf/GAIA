# Telegram: As‑Is Implementation, Gaps, and Roadmap

Generated: 2026-02-04T00:00:00Z

This document summarizes the current Telegram integration in the GAIA repo, evidence of running features from logs/events, an analysis of gaps, and a prioritized roadmap and short actionable tasks to reach the target: a robust Telegram channel agent for home development.

**Scope & Concept**:
- **Purpose:** provide an approval/control channel and operator interface via Telegram for GAIA agents (alerts, approval flows, command enqueue/approve/execute, monitoring). The bot posts status updates, accepts approval messages, and dispatches/records commands.
- **Design boundaries:** CLI-first agents; ephemeral secrets are stored under `.tmp/telegram.env`; canonical backlog lives in `doc/EPC_Telegram.current`.

**Key Implementation Areas (as‑is)**
- `scripts/telegram_client.py`: low-level Bot API helpers (`send_message`, `get_updates`, `edit_message_text`, `answer_callback`) with retries/backoff and helpers to record failed replies (file: `.tmp/telegram_queue_failed.json`).
- `gaia/alerts.py`: higher-level `send_telegram()` wrapper that emits events and writes audit traces to `gaia.db` on success/error.
- `scripts/gise_autonomous_runner.py`: periodic status poster and lightweight helper runner; reads `.tmp/telegram.env`, posts status, runs validators and part‑1 helpers, writes `.tmp/gise_status/*.txt` notes.
- `agents/controller_agent.py`: local orchestrator that can notify via Telegram; reads `.tmp/telegram.env` and calls `scripts.telegram_client.send_message`.
- `events.ndjson`: active event stream showing many Telegram-related events (enqueued/processed messages, approvals, command lifecycle events, alert.sent/alert.error).
- `.env` present in repo with sample token variable (local convenience) and `.tmp/telegram.env` used at runtime.

**Evidence of Working Features (observed in `events.ndjson` and files)**
- Bot can send messages: multiple `alert.sent` events with successful `resp.ok: true` (see events.ndjson timestamps around 2026-02-03). [events.ndjson](events.ndjson)
- Approval flow works: `alert.requested` → user replies → `approval.received` events recorded. (Multiple `approval.received` entries). [events.ndjson](events.ndjson)
- Message ingestion pipeline: `telegram.enqueued` and `telegram.processed` events exist for many inbound messages (IDs and replies recorded). [events.ndjson](events.ndjson)
- Command lifecycle implemented: `command.enqueued`, `approval.requested`, `command.approved`, `command.executed.dryrun`, and occasional `command.executed` events present. [events.ndjson](events.ndjson)
- Periodic status posting: `scripts/gise_autonomous_runner.py` exists and writes `.tmp/gise_status/status_TIMESTAMP.txt`. [scripts/gise_autonomous_runner.py](scripts/gise_autonomous_runner.py)

**Current Feature List (ordered by current plan / feature scores)**
1. F-helper-gise-part2 (epic: prototype & acceptance) — backlog and STR_TestGise acceptance items (high priority). Source: `doc/EPC_Telegram.current`.
2. F-helper-gise-part1 (scan, design, scaffold) — repo scanning and alby agent scaffolding.
3. F-security-token — token handling, rotate, .env.template (todo).
4. F-command-safety — execution safety flags, confirmation UI (todo).
5. F-integration-tests — mocked Telegram harness + integration tests (todo).
6. F-ttl-requeue-policy — claim TTL configuration and tests (todo).
7. F-retryer — improved error classification and backoff (todo).
8. F-permanent-failed-ui — monitor and requeue UI (todo).
9. F-metrics-alerts, F-backup-retention, F-runbook-docs — metrics, backups, docs (todo).

See `doc/EPC_Telegram.current` and `doc/EPC_Telegram_all_todos.md` for all feature/task details. [doc/EPC_Telegram.current](doc/EPC_Telegram.current) [doc/EPC_Telegram_all_todos.md](doc/EPC_Telegram_all_todos.md)

**Completed / Implemented Items (summary & evidence)**
- Basic Telegram client (send/get updates, edit, answer callbacks): `scripts/telegram_client.py` (implemented). [scripts/telegram_client.py](scripts/telegram_client.py)
- Alerts wrapper that records events and traces: `gaia/alerts.py` (implemented). [gaia/alerts.py](gaia/alerts.py)
- Approval observation & recording: `approval.received` events in `events.ndjson` (evidence of human approvals). [events.ndjson](events.ndjson)
- Command enqueue/approval/dryrun: event stream shows enqueued/approved/dryrun/executed flows. [events.ndjson](events.ndjson)
- Periodic status poster and helper runner scaffold: `scripts/gise_autonomous_runner.py` (implemented). [scripts/gise_autonomous_runner.py](scripts/gise_autonomous_runner.py)
- Controller agent can read `.tmp/telegram.env` and send messages (code path present). [agents/controller_agent.py](agents/controller_agent.py)

**Pending / Missing or TODO (gap analysis)**
- Secrets & token hygiene
  - `.env.template` is missing; `.tmp/telegram.env` usage exists but no canonical template or README describing secure storage and file permissions. (task: `t12`, `t11`)
  - Token rotation scaffold (`scripts/rotate_admin_token.py`) not present. (task: `t13`)
- Testing & CI
  - No mocked Telegram API harness for CI; integration tests currently missing (task: `t17`, `t18`, `t19`).
  - Unit tests for `telegram_client` and retry semantics are missing.
- Retryer & error classification
  - `telegram_client` has retries but global retryer classification for HTTP codes and exponential backoff with jitter is TODO (tasks `t23`–`t25`).
- Command safety
  - Need to enforce `ALLOW_COMMAND_EXECUTION=0` by default and add explicit approval UI/confirmations (tasks `t14`–`t16`).
- Claim TTL and takeover
  - `CLAIM_DEFAULT_TTL` not implemented across claim scripts and tests (tasks `t20`–`t22`).
- Permanent-failed UI & requeue
  - Monitor pages and token-protected requeue actions missing (tasks `t29`–`t31`).
- Backups, metrics, runbook
  - Backups and retention scripts are not present; metrics persistence and alert wiring require work (tasks `t26`–`t28`, `t32`–`t34`, `t35`–`t37`).

**Prioritized Short Roadmap (home development target)**
Goal: build a robust Telegram channel agent for home development — safe, testable, and easy to operate locally.

Phase 0 — Safety & secrets (1–2 days)
- Create `.env.template` and update README: explain `.tmp/telegram.env` usage, file permissions, and recommended local storage. (Implement task `t12`, `t11`.)
- Ensure `ALLOW_COMMAND_EXECUTION` defaults to `0` and document safe dev workflow. (`t14`)

Phase 1 — Test harness & CI (2–4 days)
- Implement a local mocked Telegram API (small Flask or FastAPI app that supports `/bot<token>/sendMessage` and `/bot<token>/getUpdates`) and tests that point `telegram_client` to the mock via host override. Implement `t17`.
- Add unit tests for `scripts/telegram_client.py` using the mock or `responses` library for deterministic coverage. Implement `t18` and `t19`.

Phase 2 — Reliability & retryer (1–2 days)
- Implement HTTP error classification and exponential backoff with jitter; add tests simulating 429/5xx. (`t23`–`t25`)

Phase 3 — Token rotation & secure ops (1 day)
- Add `scripts/rotate_admin_token.py` scaffold that validates token, updates `.tmp/telegram.env` (or store encrypted secret), and appends audit trace to `gaia.db`. (`t13`)

Phase 4 — Workflow features (2–4 days)
- Implement `CLAIM_DEFAULT_TTL` env configuration and tests for takeover semantics. (`t20`–`t22`)
- Add permanent-failed monitor and one-click requeue with token protection. (`t29`–`t31`)

Phase 5 — Runbook & polish (1–2 days)
- Add CLI examples, runbook entries, backup scripts, and metrics wiring. (`t32`–`t37`)

Total rough dev time: 1–2 weeks (home dev pace) depending on how many items you implement concurrently.

**Concrete first tasks I can implement now (low-friction)**
1. Add `.env.template` and short README snippet for `.tmp/telegram.env` storage and permissions. (small patch)
2. Add a minimal mocked Telegram harness under `tests/support/mock_telegram.py` plus one unit test for `telegram_client.send_message` using the harness. (small/medium)
3. Scaffold `scripts/rotate_admin_token.py` to perform a dry-run token validation and write audit trace to `gaia.db` (scaffold only).

If you want, I can implement task (1) immediately and run a quick local validation; say "implement .env.template" and I'll proceed.

---

Files referenced in this summary:
- [doc/EPC_Telegram.current](doc/EPC_Telegram.current)
- [doc/EPC_Telegram_all_todos.md](doc/EPC_Telegram_all_todos.md)
- [scripts/telegram_client.py](scripts/telegram_client.py)
- [gaia/alerts.py](gaia/alerts.py)
- [scripts/gise_autonomous_runner.py](scripts/gise_autonomous_runner.py)
- [agents/controller_agent.py](agents/controller_agent.py)
- [events.ndjson](events.ndjson)
