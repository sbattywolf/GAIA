# Telegram integration: requirements, design, and implementation plan

Purpose
- Make Telegram the primary remote control and notification channel for GAIA.
- Requirements cover reliability, observability, security, and operator workflows.

Core requirements
- Durable inbound queue: messages must be appended to an on-disk queue (`.tmp/telegram_queue.json`) with deduplication by `message_id`.
- Long-polling reader: a `telegram_service` process must long-poll `getUpdates` with an adjustable timeout and persist the progress offset in `.tmp/telegram_state.json`.
- Friendly immediate ACKs: short immediate replies to users acknowledging receipt (randomized templates) to provide UX feedback.
- Dispatcher: a separate `dispatcher` component reads the queue and routes intents to `gaia.agent_manager` APIs and other handlers.
- Retry and backoff for outbound replies: when `dispatcher` sends messages, failures should be retried with exponential backoff and failed items recorded to `.tmp/telegram_queue_failed.json`.
- Single-chat enforcement (optional): allow restricting processing to a configured `CHAT_ID` to reduce spam and mitigate risk.

Persistence and traces
- All inbound and outbound actions must be traced into `events.ndjson` using `events.make_event(...)` for audit.
- Operational state: `gaia.db` stores small audit/traces used by the monitor UI.
- Health artifacts: `telegram_health.json` (current processed count, last_seen, started), `telegram_connectivity.json` (getMe/getChat/send checks), and PID files under `.tmp/*.pid`.

Operational behaviors
- Deduplication: queue append should skip messages already present by `message_id`.
- Offset persistence: after processing updates from Telegram, save `offset = update_id + 1` to `telegram_state.json` atomically.
- Rate-limiting: apply rate limiting on instruct-like endpoints (already in `monitor`) and protect `dispatcher` from flood.
- Supervisor integration: provide systemd unit and a simple launcher to ensure single-instance and restart on failure; for devices without systemd, provide a launcher script and cron @reboot guidance.

Security & secrets
- Keep the bot token out of VCS: use `.tmp/telegram.env` and ensure `.gitignore` excludes `.tmp` (repo already follows this pattern).
- Limit accepted chats by `CHAT_ID` when configured.
- Log only non-sensitive metadata in `events.ndjson` and health files; do not log full tokens or sensitive payloads.

Monitoring & UI
- Expose `monitor` SSE endpoints already implemented: `/api/telegram/health` and `/api/telegram/stream`.
- Add a Dashboard card showing: bot running (pid), last_seen, processed count, queue length, last enqueued message text (first 120 chars).

Failure modes and recovery
- If `telegram_service` loses connectivity, it should back off and write a health status with `running=false` and `last_error`.
- If `dispatcher` fails to send replies, items move to `telegram_queue_failed.json` and can be retried by `process_telegram_queue.py`.
- When offsets are missing or corrupted, the operator can reset `telegram_state.json` to null and rely on `getUpdates` to return recent messages (use caution to avoid reprocessing many old updates).

Events produced (examples)
- `telegram.enqueued` — when a message is appended to the queue.
- `telegram.processed` — when a dispatcher processes a queue item (include result/ok).
- `telegram.reply.sent` — successful reply to chat (include message_id of reply).

Implementation plan (ordered)
1. Verify `telegram_service.py` long-polling and offset persistence (exists in repo). Smoke-run and ensure `.tmp/telegram_queue.json` is created on inbound.
2. Ensure `scripts/dispatcher.py` is wired to read the queue and post replies; add tests for `status`, `list`, `start`, `stop` intents.
3. Add `process_telegram_queue.py` to retry failed replies and log failures.
4. Add systemd unit and launcher (`scripts/run_session.sh`, `scripts/gaia_session.service`) for supervisor behavior.
5. Wire monitor UI to show queue length and health (endpoints exist; add UI cards as needed).
6. Add documentation and a small installer script for systemd-enabled NAS devices.

Files of interest
- `scripts/telegram_service.py` — long-poll service.
- `scripts/telegram_client.py` — helper for API calls with retry.
- `scripts/dispatcher.py` — intent parser and executor.
- `scripts/process_telegram_queue.py` — retry helper for failed sends.
- `monitor/app.py` — UI and SSE endpoints for health and queue.

Notes
- This design minimizes external dependencies and favors simple file-based persistence to be NAS-friendly.
- For higher scale or multi-user setups, replace the on-disk queue with a small message broker (Redis/SQLite row-based queue) and add authentication for the dispatcher API.
