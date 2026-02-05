## Telegram Integration — Improvements Trace

This document summarizes the Telegram-related improvements implemented in the GAIA prototype, the files changed, and recommended testing steps.

Summary of features
- Long-poll approval listener with callback handling (`scripts/approval_listener.py`)
- Enqueue & approval workflow with file-backed queue: `.tmp/pending_commands.json` (`scripts/tg_command_manager.py`)
- Inline keyboard messages with Approve/Deny/Info/Postpone/Toggle/Proceed actions
- Typing indicators while composing replies (`send_chat_action` usage)
- Monitor UI integration (SSE) and `/api/pending_commands` endpoints (`monitor/app.py`, `monitor/templates/index.html`)
- SQLite audit table `command_audit` for traceability
- Expiry policy for pending commands (`expire_old`) and maintenance scheduler

Files changed (high level)
- `scripts/tg_command_manager.py`: enqueue, interactive inline keyboard generation, `toggle_option`, `approve`, `deny`, `execute` (dry-run), audit writes, `append_event` calls.
- `scripts/telegram_client.py`: added `reply_markup` support, `answer_callback`, `send_chat_action`, `edit_message_text` helpers.
- `scripts/approval_listener.py`: callback handling for approve/deny/info/toggle/proceed/postpone, typing indicator thread, persisted offset handling.
- `monitor/app.py`: Added `/api/pending_commands`, stream endpoint, and approve/deny/postpone/info endpoints.
- `monitor/templates/index.html`: UI card for pending commands with Approve/Deny/Info/Postpone/Proceed buttons wired to monitor APIs.
- `scripts/run_readiness_test.py`: programmatic readiness test used during development.

Testing guidance
- Local dry-run: use `scripts/run_readiness_test.py` (no network) to validate enqueue, approve, events, and audit rows.
- Live test: set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_NOTIFY_CHAT` in `.env` or env, then run `python scripts/approval_listener.py --poll 5` and interact with the bot.
- Unhappy-path tests: see `doc/SECRETS_TESTING.md` and `.tmp/test_secrets/invalid_tokens.env.template`.

Operational notes
- Execution is gated: `ALLOW_COMMAND_EXECUTION=1` is required for real execution; by default `execute()` performs a dry-run and records `executed_dryrun` in the pending file and audit table.
- UI approve endpoint requires `GAIA_MONITOR_API_KEY` for basic protection.
- Audit and events are appended to `gaia.db` (`command_audit`) and `events.ndjson` respectively; these should be monitored during tests.

Next improvements (optional)
- Webhook mode for callback queries (requires public URL + webhook setup) to avoid long-poll.
- Role-based approval: constrain approve/proceed to specific Telegram user IDs or monitor-authenticated users.
- Add automated integration tests that run unhappy-path scenarios and validate `events.ndjson` entries.

Implemented enforcement
- The approval listener now supports restricting who can approve/deny/proceed via the `TELEGRAM_APPROVER_IDS` environment variable (comma-separated Telegram user IDs). When set, callback actions are only accepted from IDs in this list and unauthorized attempts receive an explicit Telegram reply.

Test harness
- A small test harness `scripts/test_harness.py` was added to exercise invalid token and related scenarios. See `doc/SECRETS_TESTING.md` for usage.
