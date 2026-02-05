This document lists the approval checkpoints used to gate autonomous actions in the repository.

Checkpoints
---------

- **CHECKPOINT_1**: Global autonomy enablement. Purpose: allow runners to perform a broad set of actions (micro-commits, creating issues, sending notifications). Status: created.

- **CHECKPOINT_2**: Telegram realtime activation. Purpose: enable periodic live Telegram notifications and live-streaming sprint status. Required gating:
  - Add `send_telegram` to `config/agent_mode_allowlist.json` (already present in draft).
  - Set `.tmp/autonomous_mode.json` to `{ "autonomous": true }` only after approval.
  - Ensure `PERIODIC_NOTIFICATIONS_ENABLED=1` in environment when enabling.

- **CHECKPOINT_3**: Archive cleanup. Purpose: remove or relocate prototype scheduler files. Required gating: approval file describing files to move/delete and a DryRun verification.

Approval Flow
-------------

1. Create a `CHECKPOINT_<n>.md` with a precise list of side-effects and the author of the change.
2. Request approval by running `scripts/approve_checkpoint.py` or by leaving the `CHECKPOINT_<n>.md` file for reviewers to approve.
3. After approval, runners will consult `.tmp/autonomous_mode.json` and the allowlist before taking the enabled actions.

Notes
-----

- Keep approvals small and narrowly scoped. Prefer per-feature checkpoints (e.g., Telegram realtime) rather than one large global approval.
- Use `events.ndjson` as the auditable trail for approvals.
