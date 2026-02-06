# Agent Backlog Guidelines

This document explains how a GAIA agent should navigate, evaluate, and update the project backlog. It is written for automated agents and for developers who implement or operate agents.

1. Core Principles
- Hierarchy: Project -> Epics -> Sprints -> Mini‑sprints -> Tasks -> Subtasks.
- Single Source of Truth: the canonical backlog state is recorded in the audit DB (`gaia.db`) and events are appended to `events.ndjson` (append‑only).
- Atomic changes: every backlog state change (create / split / assign / complete) must produce:
  - an audit row in `gaia.db` (use `orchestrator.write_audit`), and
  - an appended event in `events.ndjson` with `type: backlog.update` and a descriptive payload.
- Idempotence: repeated operations must not produce duplicate or inconsistent state.

2. Work structure and priority
- Priority levels (example): P0 (critical), P1 (high), P2 (medium), P3 (low).
- Prioritize based on customer impact, security risk, release dependencies, and contractual deadlines.
- Agents should compute a numeric score (e.g., 0–100) by weighting factors; score > 80 → P0.

3. Sprints and mini‑sprints
- Definitions:
  - Sprint: a collection of work items targeted for a timebox (e.g., 1–2 weeks).
  - Mini‑sprint: a smaller work unit (1–3 days) useful for quick breakdowns.
- Splitting rules:
  1. If a task estimate exceeds a configurable threshold (default: 8 story points or ~3 days), the agent should propose a split.
  2. A split must produce at least two clear subtasks, assign priorities, and add them to the current sprint (or create a mini‑sprint if appropriate).
  3. All changes must update the sprint master document and append a `backlog.split` event.

4. Agent decision cycle (simplified algorithm)
1. Load context: active sprint, task list, priorities, and available capacity (resource slots).
2. Select candidate: sort tasks by (priority, dependencies satisfied, age) and pick the first that fits capacity.
3. Size check: if task size > threshold → split into subtasks or mini‑sprints and update backlog.
4. Safety check: if the task has high impact (secrets, token revocation, infra changes) create a `CHECKPOINT` and request approval.
5. Execute or assign: if the agent has execution permissions it may proceed; otherwise assign to an owner and notify stakeholders.
6. After changes, record audit + append event + update the sprint master document.

5. Splitting and iterative restructuring policy
- A sprint may be restructured multiple times; each restructure must:
  - keep traceability (link new subtasks to the original task),
  - update timestamp and actor, and
  - aim to reduce single task sizes below the threshold where reasonable.
- If total sprint points exceed estimated capacity by >150% for more than two iterations, the agent should propose a new release/sprint split and notify the owner.

6. Operational rules (safety first)
- For high‑impact operations (secret changes, token revocation, running scripts via merged PRs) follow the CHECKPOINT flow: create `doc/CHECKPOINTS/CHECKPOINT_<n>.md`, append event `checkpoint.request`, and wait for explicit approval.
- Avoid unauthorized side effects: every remote write (GitHub, CI) must use least‑privilege tokens and be recorded.

7. Documentation and automation updates
- Whenever the agent modifies backlog or sprint structure, update these artifacts:
  - append an event to `events.ndjson` with UTC timestamp,
  - write an audit row to `gaia.db` via `orchestrator.write_audit`, and
  - update `doc/sprints/SPRINT_<current>.md` or `doc/sprints/checklists/created-issues.md` with links and notes.
- If the change affects the runbook, update `PLAN.md` or create `PLAN_<timestamp>.md` with rationale.

8. Recommended event schema (example)
```
{
  "type": "backlog.update",
  "source": "agent.token-cache",
  "timestamp": "2026-02-06T12:00:00Z",
  "payload": {
    "action": "split",
    "original_task": "TASK-123",
    "new_tasks": ["TASK-124","TASK-125"],
    "reason": "too_large",
    "by": "agent.token-cache",
    "details": { }
  }
}
```

9. Example decomposition: Project -> Epic -> Sprint -> Mini‑sprint -> Task
- Project: "GAIA secrets migration"
  - Epic: "Token rotation"
    - Sprint 2026-02-06: "Rotation runbook + publish issues"
      - Mini‑sprint A (2d): "Prepare helpers and docs"
        - Task 1: "Add secrets aliasing"
        - Task 2: "Add rotate helper script"
      - Mini‑sprint B (3d): "Create GitHub App helper + token cache"
        - Task 3: "Implement token-cache service"
        - Task 4: "Add tests and CI"

10. Metrics and self‑assessment
- Agents should produce a daily assessment (end‑of‑day) summarized in `sprint_daily.md` containing:
  - completed work (links to events/commits/issues),
  - open risks,
  - recommendations for the next day.

11. Quick checklist for choosing the next task
1. Read current sprint and available capacity.
2. Sort backlog by priority and dependencies.
3. Check if the task requires a CHECKPOINT.
4. If too large → split and append event.
5. If ready and authorized → execute; otherwise assign and notify.
6. Record audit + event + update sprint document and `PLAN.md` if needed.

12. Final notes
- These guidelines describe recommended agent behavior. Agents must always prefer safety and traceability over speed. When in doubt, create a CHECKPOINT and request human approval.
