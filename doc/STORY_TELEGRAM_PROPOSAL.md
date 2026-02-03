**Telegram + Controllers — Proposal & Prioritized Workplan**

Purpose:
- Consolidate Telegram-related todos, evaluate current status, and propose a prioritized, categorized plan to stabilize the integration and complete controller responsibilities.

Current status (as-is):
- Long-poll listener (`scripts/approval_listener.py`) is implemented and running under supervisor. Health, heartbeat, and debug logs exist.
- `tg_command_manager.py` manages pending commands and emits `events.ndjson` and audit rows.
- `telegram_client.py` implements `_with_retries` used by send/get/edit actions.
- Many operational behaviors implemented (approve/deny, expiry, dry-run execution gating).

Gaps & risks:
- Durable inbound queue with dedupe not fully implemented (design described in `doc/TELEGRAM_STORY.md`).
- Some idempotency cases (duplicate callback deliveries) need unit tests and code guards.
- Retry and failure recording for outbound replies needs a dedicated process (`telegram_queue_failed.json`).

Prioritized work (Must / Should / Nice):
- Must (short-term, 1–2 days each):
  1. Durable queue append & dedupe helper (prevent duplicate enqueues). File: `scripts/telegram_queue.py`.
  2. Idempotency checks around callback handling (guard against double-approve). Update: `scripts/approval_listener.py` + tests `tests/test_approval_idempotency.py`.
  3. Expand `telegram_client._with_retries` usage to all outbound paths and expose configurable attempts/backoff via env.
- Should (medium-term):
  4. Implement `process_telegram_queue.py` for failed reply retries and admin retry CLI.
  5. Create `scripts/dispatcher.py` to decouple intent parsing and agent routing.
  6. Add monitor UI cards for queue length & last messages.
- Nice-to-have (later):
  7. Webhook mode and systemd integration for production.
  8. Role-based approvals and per-chat language preferences persisted.

Task owners & artifacts:
- Queue helper: small module `scripts/telegram_queue.py` exposing `append_dedup(update)` and `pop_next()`.
- Tests: `tests/test_telegram_queue.py`, `tests/test_approval_idempotency.py`.
- Config: environment variables `TELEGRAM_RETRIES`, `TELEGRAM_BACKOFF_MS`, `TELEGRAM_APPROVER_IDS`.

Acceptance criteria (proposal):
- No duplicate events in `events.ndjson` when the same update or callback is delivered twice.
- Listener can be stopped and restarted without reprocessing already-processed updates (offset/resume).
- Failed outbound replies are recordable and retryable via `process_telegram_queue.py`.

Deployment & validation plan:
1. Implement queue helper and add tests. Merge to main branch after passing tests.
2. Deploy listener with queue helper enabled in a local run; exercise duplicate deliveries (unit + integration test).
3. Add failed-reply retryer and run smoke tests sending to a local dummy server (or mock Telegram).

Estimated effort: 3–7 days of engineering to reach stable behavior and tests.
