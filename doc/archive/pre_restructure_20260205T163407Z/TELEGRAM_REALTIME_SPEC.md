**Telegram Realtime Notifications Spec**

- **Purpose**: provide near-real-time notifications about agent progress, including timestamps, live metrics, and sprint status, for monitoring and audit.
- **Delivery**: Telegram messages to the configured chat (TELEGRAM_CHAT_ID) using bot token (TELEGRAM_BOT_TOKEN). Default operation is dry-run (no network) unless `--send` is used.

- **Message contents**:
  - **Timestamp:** UTC ISO8601 (e.g., 2026-02-05T12:34:56Z).
  - **Source:** agent/process name (e.g., `automation_runner`, `approval_listener`).
  - **Status:** short status token (`starting`, `running`, `succeeded`, `failed`, `idle`).
  - **Sprint:** `PROJECT_V2_NUMBER` from environment, or fallback `unknown`.
  - **Live metrics (optional):** CPU/memory, queued approvals, pending tasks count, events processed in last interval.
  - **Context link / short summary:** brief 1–2 line human-friendly summary and a link or path to relevant local file (e.g., `events.ndjson` tail) when available.

- **Formatting**: compact text message with sections and emojis, example:

  Agent: automation_runner 🔁
  Time: 2026-02-05T12:34:56Z
  Sprint: 3
  Status: running ▶️
  Queue: 2 approvals pending
  Events(last 5m): 12
  Summary: processing sprint backlog — running step 4/8

- **Behavior**:
  - Periodic snapshots: configurable interval (default 5m). Controlled by `PERIODIC_NOTIFICATIONS_ENABLED` and `PERIODIC_INTERVAL_SEC` env vars.
  - Event-triggered messages: send on important events (approval.request, approval.received, runner start/stop/error).
  - Dry-run mode by default; `--send` enables actual Telegram send (requires tokens).

- **Security & safety**:
  - Secrets read from `.private/.env` only. Never commit tokens.
  - Messages must avoid including raw secrets or sensitive payloads.

- **Next steps for implementation**:
  1. Add a small notifier script `scripts/telegram_realtime.py` that implements dry-run formatting and optional `--send`.
  2. Wire notifier into `automation_runner.py` and `approval_listener.py` to emit structured summaries.
  3. Add unit tests for formatting and a small integration dry-run.
