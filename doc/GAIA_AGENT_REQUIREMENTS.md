# GAIA Agent Requirements & Work Procedures

Generated: 2026-02-06T13:50:00Z

Purpose: capture required behaviors, constraints, and improvement candidates for the GAIA autonomous agent persona and operator procedures.

Scope: agent runtime actions, persistence, audit, secrets handling, approvals, and remote integrations (GitHub, Telegram, etc.).

1) Safety & Approval Constraints
- The agent MUST NOT perform destructive repository history rewrites or credential rotations without a documented `CHECKPOINT_<n>.md` and explicit human approval recorded in the session state.
- Any remote side-effect (creating GitHub issues, merging PRs, creating or deleting remote resources) must be made via configurable opt-in (environment flag) and require an approval step recorded in `.copilot/session_state.json`.

2) Secrets & Sensitive Data Handling
- Always run `detect-secrets` before any history rewrite. Store scanner output in `.tmp/` and never commit raw secret values.
- Agent must maintain and respect a `secrets.allowlist` and `.secrets.baseline` to reduce false positives for known test fixtures.
- Events appended to `events.ndjson` must never include raw secret values. Mask or reference only artifact IDs and redacted snippets.

3) Session Persistence & Recovery
- Persist agent state after each completed step to `.copilot/session_state.json` including: `current_task_id`, `steps_completed`, `next_immediate_step`, `last_sync` (ISO8601 UTC), and `trace_id`.
- On startup, agent reads `.copilot/session_state.json` and `PLAN.md` and resumes from `next_immediate_step` if present. If inconsistent, agent must open a `CHECKPOINT_<n>.md` and pause.

4) Remote Actions & Credential Use
- Use environment-based credentials (CI secrets or OS-level secret stores). NEVER embed credentials in code or committed files.
- When interacting with `gh` or cloud APIs, capture the command output and write an audit record to `gaia.db` and an event to `events.ndjson` with `type: agent.action` and redacted payload.

5) Detect-Secrets & Baseline Policy
- Run `detect-secrets scan` on commit and weekly full-repo scans. Store baseline in `.secrets.baseline` and commit only the baseline (not secrets).
- Provide a per-repo `detect-secrets` config to allow known test patterns in `external/` and `tests/` while flagging `doc/archive` and `.env` files.

6) Logging, Audit & Traceability
- All agent actions must append a concise audit row to `gaia.db` (table `audit`) with `timestamp`, `action`, `actor`, `target`, and `trace_id`.
- Append a human-readable event to `events.ndjson` with `type`, `source`, `target`, `task_id`, `payload` (redacted), `timestamp`, `trace_id`.

9) Single Source of Truth (Backlog sync)
- Rationale: Agents should read a single canonical source of truth for tasks and state. The canonical runtime store will be `gaia.db` (SQLite) and the repository will keep human-readable snapshots (`doc/todo-archive.ndjson`, `MASTER_BACKLOG.md`).
- Policy: The database is the authoritative runtime source; repo artifacts are human-readable snapshots and audit points. Agents must not treat the repo as the live state store.
- Workflow: On significant state updates (daily snapshots, sprint start/completion), the agent will:
	1. Sync `doc/todo-archive.ndjson` into `gaia.db` table `backlog` (id, title, status, metadata, source_file, timestamp).
	2. Append an audit record to `gaia.db` and an event to `events.ndjson` noting the sync (redacted payload).
	3. Commit the human-readable snapshot to a freeze branch when requested (CHECKPOINT flow).
- Candidate task: `TASK-007 - Centralize backlog in DB` (implemented now) — create sync script and CI check to validate repo snapshots match `gaia.db` exports.

7) Conflicts, Remarks, and Improvement Candidates
Below are items found while running the security inventory and evaluating the GAIA agent workflow. Each is written as a candidate task/epic with detail sufficient to triage.

7.1) Conflict: agent autonomy vs approval-gated destructive operations
- Description: GAIA design prefers autonomous actions, but history-rewrites and credential rotations are high-risk.
- Impact: Risk of accidental data loss or incomplete credential rotation.
- Suggested resolution: Implement `CHECKPOINT` workflow: create `CHECKPOINT_<n>.md` (draft), list impacted files and replacements, require human `APPROVATO` entry in the file and a signed confirmation in `.copilot/session_state.json`.
- Candidate task: `EPIC-001 - Implement CHECKPOINT approval flow` — steps: draft `CHECKPOINT` template, add approval parser, block destructive commands until approval.

7.2) Improvement: stricter secrets leak triage policy
- Description: detect-secrets finds many entries inside `external/` and test fixtures; need a clear triage policy.
- Impact: Wastes operator time and may mask real leaks.
- Suggested resolution: Create per-path allowlist rules, and a triage script to mark `vendor/test` findings as lower priority; escalate `doc/archive/*`, `*.env`, and `*.key` findings automatically.
- Candidate task: `TASK-002 - Implement triage script for detect-secrets output` — produce prioritized CSV for human review.

7.3) Improvement: events.ndjson content policy
- Description: Agent events currently can include payloads that might inadvertently contain secrets.
- Impact: Sensitive data might be stored in append-only event log.
- Suggested resolution: Enforce event payload sanitizer that redacts patterns matching known secret regexes before appending.
- Candidate task: `TASK-003 - Implement event payload sanitizer` — unit tests, CI check, and commit hook.

7.4) Improvement: session-state durability & recovery tests
- Description: `.copilot/session_state.json` is required for recovery but not currently validated by tests.
- Impact: Recovery might fail after crash if format incompatible.
- Suggested resolution: Add integration tests that simulate interruption and validate resume behavior.
- Candidate task: `TASK-004 - Add session_state resume tests` — test harness and CI job.

7.5) Conflict: remote GH actions require secrets & opt-in
- Description: Creating issues or PRs via `gh` requires credentials; autonomous creation should be opt-in and auditable.
- Impact: Unintended remote changes if env misconfigured.
- Suggested resolution: Add `PROTOTYPE_USE_LOCAL_EVENTS=1` default; require `ALLOW_REMOTE_ACTIONS=1` env and explicit approval in `CHECKPOINT` for remote issue creation/PRs.
- Candidate task: `TASK-005 - Harden remote action gating` — implement env gating and audit.

7.6) Improvement: rotation playbooks per provider
- Description: Rotating leaked credentials requires provider-specific steps (GitHub, Telegram, AWS, OpenAI, etc.).
- Impact: Without playbooks, rotations are slow and error-prone.
- Suggested resolution: Create a library of small rotation playbooks and checklists, stored in `doc/rotation_playbooks/`.
- Candidate task: `EPIC-006 - Rotation playbooks and automation` — create templates, automate common provider rotations where safe.

8) Next operational steps (recommended immediate tasks)
- Run triage script on `.tmp/detect_secrets_scan_20260206.json` and produce `reports/detect_secrets_priority_20260206.csv`.
- Draft `CHECKPOINT_1.md` with `doc/sprints/analysis/secrets_inventory_20260206.md` attached and request explicit approval.

Maintainer: GAIA agent / repo maintainers
