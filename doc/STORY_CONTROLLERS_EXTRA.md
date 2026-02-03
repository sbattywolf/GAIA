**Controllers — Extra: backlog, mapping, and prioritized tasks**

Summary:
- This document collects concrete backlog items, code/file mappings, tests, and a prioritized task plan for the Controllers chapter (including Telegram integration).

Files of interest (controller surface):
- `scripts/approval_listener.py` — Telegram long-poll listener and callback handler.
- `scripts/tg_command_manager.py` — enqueue/list/approve/deny/execute lifecycle and file-backed pending queue.
- `scripts/telegram_client.py` — HTTP helpers with retry/backoff.
- `scripts/run_with_env.py` — safe runner for env-loaded command execution.
- `monitor/app.py` — monitor API endpoints for pending commands (UI controller surface).

Implemented features (observed):
- Inline keyboard approve/deny/info/proceed flows.
- File-backed pending queue: `.tmp/pending_commands.json` and expiry policy.
- SQLite audit table `command_audit` and `events.ndjson` append-only traces.
- Heartbeat and health JSON (`.tmp/telegram_health.json`) and debug log rotation.

Backlog items (concrete):
- Durable inbound queue with dedupe by `message_id` (`.tmp/telegram_queue.json`).
- Dispatcher component to read queue and route to agent manager.
- Failed-reply retry processor (`process_telegram_queue.py`).
- Idempotency and offset persistence guards in `approval_listener`.
- Unit tests for callback handling and idempotency.

Prioritized tasks (Must / Should / Nice):
- Must:
  - Ensure durable queueing and deduplication (idempotency): implement queue append with message_id guard. (maps to: `scripts/approval_listener.py` + new `scripts/telegram_queue.py`)
  - Add unit tests simulating callback updates and repeated deliveries to verify idempotency. (maps to: `tests/test_approval_idempotency.py`)
  - Harden `get_updates` handling with backoff and full error logging (use `telegram_client._with_retries` and expand to configurable attempts). (maps to: `scripts/telegram_client.py`)
- Should:
  - Implement `process_telegram_queue.py` to retry failed outbound replies and record to `.tmp/telegram_queue_failed.json`.
  - Add a dispatcher that routes parsed intents to `agents/` and uses `events.make_event` for tracing.
  - Enforce `TELEGRAM_APPROVER_IDS` consistently and document admin flows.
- Nice-to-have:
  - Webhook mode option and systemd service templates for production.
  - Monitor UI cards showing queue length and last messages.

Acceptance test checklist (controller / Telegram):
- Enqueue a message (simulate `getUpdates`) -> queue file created with `message_id` and `update_id` stored.
- Re-deliver the same update -> queue not duplicated and handler marks it as seen.
- Press the same callback twice -> only one approve action is recorded in `events.ndjson` and `command_audit`.
- Listener restart after crash -> resumes from `telegram_state.json` offset and does not reprocess processed updates.

Next immediate work (recommended):
1. Implement durable queue append with dedupe helper and wire into `approval_listener`.
2. Add idempotency unit tests and small test utils to create fake update payloads.
3. Harden retry/backoff and add configurable limits in `telegram_client`.
