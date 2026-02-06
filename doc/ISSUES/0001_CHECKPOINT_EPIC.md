Title: CHECKPOINT: Implement approval flow and enforcement

Summary:
Implement the CHECKPOINT approval flow for high-impact changes. This includes a `CHECKPOINT_<id>.md` template, an approval marker mechanism (`CHECKPOINT_<id>.approved`), and enforcement in CI and `orchestrator.py` so agents and merges are blocked until approval.

Why:
High-impact operations (secret purge, wide-scope migrations, destructive remote actions) must be explicitly approved and auditable.

Acceptance criteria:
- `CHECKPOINT_<id>.md` template added and used in PRs.
- CI job fails merges when a PR references a checkpoint without a matching `CHECKPOINT_<id>.approved` marker.
- `orchestrator.py` and agents check for checkpoint approval before executing destructive actions.
- Audit events written into `events.ndjson` and `gaia.db` when checkpointed actions are attempted.

Suggested labels: checkpoint, security, epic

Suggested assignees: security-team
