Plan for making Copilot workflow stateful, safe, and integrated

Goal: Ensure autonomous sessions are persistent, require checkpoints for high-impact actions,
and integrate approval/checkpoint flows into the existing GAIA project.

Steps (max 8):
1. Create session-state template and system prompt (completed).
   - Files: `.copilot/session_state.json`, `.github/copilot-instructions.md`
2. Review backlog & current sprint state and produce `PLAN.md` (this document).
3. Add `PLAN.md` approval checkpoint step: require `APPROVATO` marker before code edits.
4. Wire agents/runners to update `.copilot/session_state.json` after each micro-step.
   - Update runners (`scripts/automation_runner.py`, `scripts/gise_autonomous_runner.py`) to write compact state records after each completed action.
5. Add deterministic trace IDs to all approval events and persist them to `gaia.db` (audit).
6. Implement small unit tests for approval extractor and autonomy guard; add CI dry-run workflow that runs tests without external calls.
7. Add micro-commit logic: create branch `feat/copilot-autowork`, commit after each micro-step when tests pass.
8. Add a manual checkpoint flow: a `CHECKPOINT_<n>.md` creator and a gating step that halts execution until the approved checkpoint is present.

Next immediate step: Review this `PLAN.md` and mark APPROVATO in the file to allow execution of the steps that modify code.
