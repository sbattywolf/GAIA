**Controllers — Story**

Overview:
- Purpose: small controller modules that map external triggers (Telegram, webhooks, cron) to agent invocations and event emission.

Backlog mapping:
- `scripts/approval_listener.py` is a controller for Telegram callbacks.
- Controllers should be thin, testable, and emit structured events for consumers.

Telegram integration:
- The Telegram approval and callback flow is a primary inbound controller for GAIA and should be considered part of the Controllers chapter. See `doc/TELEGRAM_STORY.md` and `doc/TELEGRAM_IMPROVEMENTS.md` for full design and implemented features.
- Controllers must implement durable queueing, idempotent processing, offset persistence, and clear audit events for every callback/intent.

Acceptance criteria:
- Controllers implement idempotent handling of updates, clear error handling, and emit `events.ndjson` entries for each meaningful action.
- Controllers are unit-tested with simulated updates (no external network required).

Next steps:
- Add unit tests for `approval_listener` and `tg_command_manager` callback handling.
- Create a small `controller_test_utils.py` for constructing update payloads.
