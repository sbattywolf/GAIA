# EPC_Telegram — Epic Report

Date: 2026-02-03

## Executive summary

This document is a canonical, human-friendly report for the `EPC_Telegram` epic. It summarizes features, stories, and todo tasks migrated into the canonical backlog (`doc/EPC_Telegram.current`) and provides practical workflow guidance for creating, assigning, and organizing backlog items going forward.

Key figures

- Total features: 9
````markdown
# EPC_Telegram — Epic Report

Date: 2026-02-03

## Executive summary

This document is a canonical, human-friendly report for the `EPC_Telegram` epic. It summarizes features, stories, and todo tasks migrated into the canonical backlog (`doc/EPC_Telegram.current`) and provides practical workflow guidance for creating, assigning, and organizing backlog items going forward.

Key figures

- Total features: 9
- Total stories: 9
- Total todo tasks (migrated): 27

---

## 1) Epic summary table

| Metric | Count |
|---|---:|
| Features | 9 |
| Stories | 9 |
| Tasks (migrated) | 27 |

---

## 2) Features — details, counts, priority and estimate

| Feature ID | Name | #Stories | #Tasks | Priority | Est. (dev-days) | Short description |
|---|---|---:|---:|---|---:|---|
| F-security-token | Security & token rotation | 1 | 3 | High | 2 | Secure env & admin token rotation tooling and docs |
| F-command-safety | Command execution safety | 1 | 3 | High | 4 | ALLOW_COMMAND_EXECUTION guard, UI confirmation, safe quoting |
| F-integration-tests | Integration tests | 1 | 3 | High | 5 | Mocked Telegram harness + e2e tests + idempotency checks |
| F-ttl-requeue-policy | Claim TTL & Requeue Policy | 1 | 3 | Medium-High | 3 | Decide TTL defaults and implement tests/config |
| F-retryer | Retryer error classification | 1 | 3 | High | 4 | Map HTTP errors, backoff, and tests for retry worker |
| F-metrics-alerts | Metrics & alerts | 1 | 3 | Medium | 5 | Counters, persistence, and alerting wiring |
| F-permanent-failed-ui | Permanent-failed UI & requeue | 1 | 3 | Medium | 3 | UI pages and one-click requeue with audit traces |
| F-backup-retention | Backup & retention | 1 | 3 | Medium | 2 | Backup tooling for `.tmp` and `gaia.db`, retention rules |
| F-runbook-docs | Runbook & documentation | 1 | 3 | Low-Medium | 2 | CLI examples, workflows and release checklist in docs |

Notes on estimation: estimates are rough, high-level developer-day approximations for planning. Break down each feature into smaller stories/tasks for precise sprint planning and tracking.

---

## 3) Stories table (canonical view)

| Story key | Feature | Agent | #Tasks | Notes |
|---|---|---|---:|---|
| stoy_STR | F-security-token / F-retryer / F-metrics-alerts / F-permanent-failed-ui / F-backup-retention | assistant | 1–3 per feature | Created as canonical container for migrated STR TODOs where feature had no existing story |
| stoy1 | F-command-safety / F-integration-tests / F-ttl-requeue-policy / F-runbook-docs | assistant | varies (3) | Existing story used as the main working story for the original stoy1 tasks |

Practical note: each feature currently holds one story in the canonical epic. If a feature grows, create additional story keys named `stoy<nr>` or `stoy_<short-name>` and record the agent responsible.

---

## 4) Task priority breakdown (migrated tasks)

| Priority | #Tasks |
|---|---:|
| High | 13 |
| Medium | 10 |
| Low | 4 |

Explanation: priorities were inferred from the original playbook content and the nature of each task. Adjust priorities with product/ops owners as needed.

---

## 5) Backlog & workflow rules (recommended)

This section documents a concise, repeatable process for agents and maintainers to create, merge, and manage backlog objects in this repo.

1. Short naming convention
   - Epic files: `doc/EPC_<epic_name>.current` — canonical backlog for the epic.
   - Agent working files: `.tmp/todolists/<Epic>.<Feature>.<Story>.<agent>.<todolist>.(current|draft)` — ephemeral agent-scoped edits.
   - Tasks: `tNN` stable numeric ids inside story objects. Use `t_final` for governance/immutable tail tasks.

2. Agent workflow (how an agent contributes)
   - Create or update an agent-scoped `.tmp/todolists/...draft` file while iterating locally.
   - When ready, a maintainer reviews and merges drafts into `doc/EPC_<epic>.current` by:
     - Mapping tasks to existing features/stories where possible.
     - Creating a `stoy_<agent>` story if feature has no appropriate story.
     - Recording migrated items under `merged_drafts` or `merged_currents` for traceability.
   - Once merged, the agent's draft/current files can be removed to avoid duplication.

3. How to choose story allocation
   - First, find an existing feature that logically owns the work (functional ownership).
   - Within that feature, prefer an existing story that matches scope or phase (e.g., `integration-tests`, `runbook`).
   - If none matches, create a new story with a clear `story_key` and short description. Use the agent name to surface ownership.

4. Priority & estimate guidance
   - Prioritize safety, security, and test-related tasks as High.
   - Use relative estimation (dev-days) for initial planning and split large items into sub-tasks for accurate sprint estimates.

5. Governance rules
   - Maintain `t_final` as the final governance item in each story (immutable marker for archival readiness).
   - Archive consumed drafts by copying content into `merged_drafts` and removing working files.

---

## 6) How to create backlog objects (step-by-step)

1. Create a new task locally in a draft file under `.tmp/todolists/` with schema:

```json
{
  "story": "Short story title",
  "story_key": "stoy<id>",
  "agent": "assistant",
  "todolist": "stoylist",
  "type": "draft",
  "tasks": [ { "id": "tNN", "title": "...", "description": "...", "status": "todo", "priority": "medium" } ]
}
```

2. Create a short PR or hand the draft to a maintainer for merging into the canonical `doc/EPC_<epic>.current`.

3. During merge, the maintainer assigns the task to the appropriate feature/story or creates one if necessary. The maintainer adds the draft's path and a short content summary into `merged_drafts` for traceability.

---

## 7) Allocation logic (how to pick a story/feature)

- Functional ownership first: pick the feature that best matches the code area or ops responsibility (e.g., retryer work → `F-retryer`).
- Scope match next: prefer existing story matching the work phase (tests, docs, infra, UI).
- Agent/owner: tag the story with the agent responsible to make future merges easier.
- If unable to find a match, create a short-lived `stoy_<agent>` under the chosen feature and merge; plan to refactor into more precise stories later.

---

## 8) Next steps and recommendations

- Run `scripts/validate_todolists.py` to validate the JSON schema for all `.tmp/todolists` and canonical `doc/EPC_Telegram.current`.
- Review the assigned priorities with product/ops owners and adjust as needed.
- Break larger features into smaller stories before sprint planning to get accurate estimates.

---

## File locations

- Canonical epic: `doc/EPC_Telegram.current`
- Agent drafts/current: `.tmp/todolists/*.current` and `.tmp/todolists/*.draft`

If you want, I can now run the validator (`scripts/validate_todolists.py`) and attach the validation output.

---

## Versioning & archival

Recommended approach:

- Primary source of truth: keep canonical backlog files in Git (`doc/EPC_<epic>.current`). Use Git history and tags for release-level snapshots.
- Short-lived agent working files (under `.tmp/todolists`) can be archived automatically before merging. Use `scripts/version_docs.py --archive` to snapshot these files into `doc/archive/` with UTC timestamps.
- For JSON-backed canonical files (e.g. `doc/EPC_Telegram.current`), `scripts/version_docs.py --bump vX.Y.Z` will set a `version` field and `versioned_at` timestamp in the JSON to help trace merges.

How to operate:

1. Before merging many drafts, run:

```bash
python scripts/version_docs.py --archive
```

2. After a canonical merge for a planned release, bump the canonical version:

```bash
python scripts/version_docs.py --bump v1.0.0
```

3. Use Git tags for release milestones and include the `doc/archive` artifacts in release assets if needed.

This minimal approach combines Git for long-term history with file snapshots for operator-friendly archive points.

---

## Preview update — STR_TestGise (added 2026-02-03)

- Added a new story `STR_TestGise` (agent `Gise`) and four agent-scoped todolist files under `.tmp/todolists/`:
  - `.tmp/todolists/EPC_Telegram.current.STR_TestGise.current`
  - `.tmp/todolists/EPC_Telegram.current.STR_TestGise.draft`
  - `.tmp/todolists/EPC_Telegram.current.STR_TestGise.AgentGise.Todo.current` (contains mandatory `t_final` task)
  - `.tmp/todolists/EPC_Telegram.current.STR_TestGise.AgentGise.Todo.draft`

These files follow the project's naming conventions: agents put work in `*.draft` while `*.current` holds in-progress items. The canonical epic (`doc/EPC_Telegram.current`) remains the source of truth; maintainers can merge tasks from these files into the appropriate feature/story when ready.

If you want, I can (a) merge these tasks into `doc/EPC_Telegram.current`, (b) run `scripts/validate_todolists.py` to validate JSON, or (c) run a dry-run of `scripts/alby_agent.py` to archive+validate. Which should I do next?

---

## Estimate adjustment (prototype runs)

I ran a small targeted test matrix to gather runtime signals used to refine the epic-level dev-day estimates. Measured single-run durations (local developer machine):

- `tests/test_claim_cli.py::test_claim_cli_roundtrip` — 10.34s
- `tests/test_claims_concurrency.py::test_concurrent_claims` — 5.01s
- `tests/test_end_to_end_requeue.py::test_admin_requeue_and_retry` — 0.31s

Using these quick prototypes and the existing backlog scope, I reduced several estimates conservatively (see table above). These are still high-level dev-day approximations — break large items into subtasks for precise sprint planning.

---

**Detailed variants added**

- **File**: [doc/EPC_Telegram_detail_variants.md](doc/EPC_Telegram_detail_variants.md)

Summary: A new decision-aid document was added that presents two concrete variants for handling `STR_TestGise`:

- **With Gise**: agent-assisted merge/validation flow where `Gise` automates validation, archival, audit trace writes to `gaia.db`, and prepares merge candidates for maintainers. (est. ~3.0 dev-days)
- **Without Gise**: maintainer-driven manual workflow using a short checklist and a helper script to validate/archive and print recommended `git` steps. (est. ~1.75 dev-days)

Decision guidance and step-by-step tasks for both variants are available in the linked file above. Choose the agent-assisted path when drafts are frequent and automation ROI is high; choose the manual path for tighter human control or when drafts are rare.
