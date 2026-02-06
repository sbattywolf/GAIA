## Token Rotation & Admin Privilege Evaluation

Purpose
- Evaluate whether `AUTOMATION_GITHUB_TOKEN_PAI` (admin-privileged) is required for current GAIA automation tasks, and produce a short plan to minimize privileges and add rotation steps.

Scope
- Review usages of automation tokens in `agents/` and `scripts/` (create PR, sessions sync, delegated updater).
- Determine minimal required OAuth scopes / fine-grained token permissions for each task.
- Produce rotation playbook and decide whether admin-level token is necessary temporarily or can be avoided.

Checklist
1. Inventory code references to automation tokens (done; see `scripts/create_pr_api.py`, `agents/github_sessions_sync.py`, other scripts).
2. For each action (create PR, create/update issue, org-level actions, secrets upload), list required scopes.
3. Propose least-privilege token mapping (e.g., `AUTOMATION_GITHUB_TOKEN` for repo writes, `PAI` only for one-off history edits).
4. Prepare a rotation procedure (generate new token, replace in encrypted store via `scripts/secrets_cli.py set`, test, revoke old token).
5. If admin privileges are proposed, require `CHECKPOINT_<n>.md` approval prior to enabling in non-dry-run.

Deliverables
- Short report: recommended minimal scopes for each automation token.
- Rotation playbook: commands to rotate stored token and record audit in `gaia.db`.
- Recommendation: keep `PAI` token disabled/absent until explicit approval; prefer scoped tokens for normal automation.

Next actions (I will proceed)
- Draft the short report and rotation playbook as `doc/SECRETS_ROTATION_PLAN.md` and attach commands to perform rotation via `scripts/secrets_cli.py`.
- After your confirmation, I will generate `doc/SECRETS_ROTATION_PLAN.md` and optionally run dry-run token replacement tests (no live writes) if you provide tokens via the encrypted store.

Generated 2026-02-06 by agent.
