# PLAN: Agent Mode Review and Finalization

Goal
- Finalize Agent Mode design: autonomy gating, checkpoints, allowed command surface, approval workflow, and documentation.

Steps
1. Read `.copilot/session_state.json` and `PLAN.md` to capture current session state and approvals.
2. Verify `scripts/autonomy_guard.py` behavior and ensure `ALLOW_COMMAND_EXECUTION` and `.tmp/autonomous_mode.json` gating are enforced across runners.
3. Enumerate checkpoint files (`CHECKPOINT_*.md`) and confirm approval CLI (`approve_checkpoint.py`) writes expected ack events to `events.ndjson` and `gaia.db` audit.
4. Define allowed command list for Agent Mode (explicit whitelist) and where to store it (e.g., `config/agent_mode_allowlist.json`).
5. Add unit tests and a CI job that exercises Agent Mode gating (DryRun + approved path).
6. Update docs: add `docs/AGENT_MODE_RUNBOOK.md` with instructions for operators and emergency disable steps.
7. Deliverables: `PLAN_AGENT_MODE.md` (this file), `docs/AGENT_MODE_RUNBOOK.md` (draft), test matrix, and a short PR with changes.

Next immediate action
- I will read `.copilot/session_state.json` and any `CHECKPOINT_*.md` files to collect current approvals and incorporate them into step 2. Proceeding now.
