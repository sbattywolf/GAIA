# Agent Mode Runbook

Purpose
- Describe how Agent Mode (autonomy) is gated, how checkpoints work, and operational steps for enabling/disabling autonomous actions.

Key components
- `scripts/autonomy_guard.py`: reads `.tmp/autonomous_mode.json` and exposes `is_autonomous_enabled()` and `require_autonomy_or_exit()` used by runners to avoid side-effects when autonomy is disabled.
- `CHECKPOINT_<n>.md` + `scripts/checkpoint.py` + `scripts/approve_checkpoint.py`: manual gating for high-impact operations. `approve_checkpoint.py` appends `APPROVATO` and emits a `checkpoint.approved` event to `events.ndjson`.
- `events.ndjson` and `orchestrator.write_audit()`: used for audit trails when approvals occur.

Operator workflow
1. Prepare: review `PLAN_AGENT_MODE.md` and ensure stakeholders agree on the scope of allowed autonomous actions.
2. To enable autonomy temporarily:

   - Create `.tmp/autonomous_mode.json` with content: `{ "autonomous": true }`

   - Confirm runners that call `require_autonomy_or_exit()` will proceed.

3. To require human approval for a high-impact change:

   - Create or open `CHECKPOINT_1.md` and add the plan.
   - Run: `python scripts/approve_checkpoint.py --checkpoint 1 --signer "Your Name" --message "Approved for dry-run"` and type `APPROVATO` when prompted (or use `--yes` to skip interactive).

4. Verify: check `events.ndjson` for a `checkpoint.approved` event and `gaia.db` for an audit row.

Allowlist recommendation
- Define an explicit allowlist for Agent Mode to limit side-effecting commands. Suggested path: `config/agent_mode_allowlist.json` with format:

  {
    "allowed_commands": ["open_issue","append_event","send_telegram"],
    "allowed_paths": [".tmp/","logs/"]
  }

- Runners should read this file at startup and refuse to execute commands not on the allowlist when autonomy is enabled.

Testing and CI
- Add unit tests for `autonomy_guard.py` (already present) and tests that exercise `require_checkpoint()` behavior.
- Add a CI job that verifies `approve_checkpoint.py` can create the checkpoint file and appends the event to a temporary `events.ndjson` artifact (dry-run mode in CI).

Emergency disable
- To immediately disable autonomous actions, remove or set `.tmp/autonomous_mode.json` to `{ "autonomous": false }` or set `ALLOW_COMMAND_EXECUTION=0` in env.

Notes
- The repo already uses these primitives in `scripts/automation_runner.py` and `scripts/gise_autonomous_runner.py`. Use the runbook to standardize behavior and add allowlist enforcement progressively.
