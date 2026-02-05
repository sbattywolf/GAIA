CHECKPOINT 2 — Telegram realtime activation

Scope
-----

Enable Telegram realtime notifications that send periodic live updates about sprint status, alerts, and aggregated metrics.

Planned side-effects
--------------------

- Periodic POSTs to Telegram via `scripts/telegram_realtime.py` or `scripts/notify.py`.
- Creation of small status artifacts in `.tmp/gise_status/` with timestamps.

Gating & Requirements
---------------------

1. Approval recorded in this file (approver writes APPROVATO and timestamp or uses `scripts/approve_checkpoint.py`).
2. `config/agent_mode_allowlist.json` must include `send_telegram` in `allowed_commands`.
3. `.tmp/autonomous_mode.json` must be set to `{ "autonomous": true }` prior to enabling periodic sends.
4. Environment variable `PERIODIC_NOTIFICATIONS_ENABLED` must be `1`.

Dry-run
-------

Before enabling, run the notifier in DryRun mode and confirm outputs are only written to `.tmp/` and `events.ndjson` (no outbound network calls). Example:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run-notifier.ps1 -DryRun
```

Approval record
---------------

Approver: 
Timestamp:

APPROVATO by sbatt at 2026-02-05T11:42:27.639578Z
Message: 
