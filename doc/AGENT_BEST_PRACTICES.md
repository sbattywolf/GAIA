# Agent Debug & Controller Best Practices

Purpose
- Document a concise set of practices for agents, controller code, and maintainers to follow during interactive debug sessions and when iterating on controller features (Telegram listener, queue, retries).

Core principles
- Persist everything: always write audit traces (`gaia.db`) and append events to `events.ndjson` for every externally-visible action.
- Make actions idempotent: mark-after-success (e.g., callback ids, message ids) to guarantee safe replay.
- Prefer small, testable helpers: file-backed queues, idempotency stores, and tiny admin CLIs so operators can recover manually.
- Surface failures: failed items should be recorded to a failed-queue file (`.tmp/telegram_queue_failed.json`) and not silently dropped.

Workflow for an interactive debug/feature session
1. Create a focused story and add concise TODOs to the repository TODO list (use `doc/` or the maintained todo list file). Keep tasks small and verifiable.
2. Implement a minimal, working change that is safe by default (dry-run, feature-flagged, or gated by `ALLOW_COMMAND_EXECUTION`).
3. Add unit tests for the new behavior and run them with repo-local basetemp on Windows (`pytest --basetemp .tmp/pytest`) to avoid system-temp permission issues.
4. Run the listener or agent in a controlled environment; collect representative Telegram `update` JSON for replay tests.
5. If the change affects message semantics (callbacks/approvals), add idempotency storage and ensure mark-after-success behavior.
6. Add an operator-facing CLI (e.g., `scripts/telegram_queue_admin.py`) for failed-item inspection and manual retries.
7. Update the runbook and create a short PR description that highlights safety considerations and how to recover from failures.

Testing & Replay
- Capture example `update` objects and record them under `tests/fixtures/` for deterministic replay tests.
- Add failure-injection tests that simulate transient HTTP failures and verify requeue/backoff behavior.
- Prefer small unit tests for logic and a few integration-style replays for end-to-end confidence.

Documentation & Story Process
- Every change that affects controller behavior should include a short note in `doc/HANDOFF.md` or a dedicated `doc/STORY_*` file describing: intent, failure modes, how to recover, and any operator commands.
- Use the repository TODO list to track work items; controllers (human role) review and accept or convert items into formal proposals.

Operator recovery checklist
- Inspect `.tmp/telegram_queue_failed.json` with `scripts/telegram_queue_admin.py --list`.
- Requeue items with `--requeue` or `--requeue-all` after verifying the cause is transient.
- If updates were duplicated externally, use the idempotency state file `.tmp/telegram_idempotency.json` to confirm which callback IDs were already processed.

Quick operator commands
- View pending commands (console):

	```powershell
	python -c "from scripts.tg_command_manager import list_pending; import json; print(json.dumps(list_pending(), indent=2))"
	```

- Run the approval listener (background recommended):

	```powershell
	python scripts/approval_listener.py --poll 5 --continue-on-approve
	```

- Start the lightweight monitor UI (local):

	```powershell
	python -m scripts.monitor_server --host 127.0.0.1 --port 8080
	# open http://127.0.0.1:8080
	```

- Inspect failed replies and requeue:

	```powershell
	python scripts/telegram_queue_admin.py --list
	python scripts/telegram_queue_admin.py --requeue ID_OR_INDEX
	```

Metrics and monitoring
- Maintain basic counters (duplicate skips, requeues, failed replies) in logs or the health file (`.tmp/telegram_health.json`).
- Surface health via the existing heartbeat file and include a simple alert rule for stopped heartbeat or growing failed-queue size.

Continuous improvement
- Keep the TODO list focused; break large items into smaller, testable steps.
- Periodically convert common failure patterns seen in `events.ndjson` into regression tests for the controller.

This file is a living runbook — agents and human maintainers should add concrete examples and CLI recipes here as they are discovered.

Working the Todo List (recommended flow)

- Start from the top of the current todo list and work each item to completion using the following loop:

	1. Read the todo item and any linked files; implement the required change(s) and run the unit/integration tests most relevant to that item first.
	2. When all tasks in the todo item appear completed, re-read the finished tasks and evaluate whether they can be **definitively closed**. If so, archive the task into project history (`doc/HISTORY_TRACING.md` or a similar timeline file) with a short note of what changed and a pointer to related commits/PRs.
	3. Decide which tests to run next for validation: per-item tests, all tests for the story, or the full test suite. Use a pragmatic trade-off: prefer fast, focused tests to validate behavior during iteration, and run the full suite before a final close or merge.
	4. If tests fail, iterate on the implementation for that task until the chosen validation set passes; record fixes in the task history entry.
	5. Mark the task closed only after archiving the result, recording any operator-run steps, and confirming relevant tests pass according to your chosen scope.

- After finishing each item, pick the next recommended step from the todo list; choose a next task balancing the cost of further testing vs. moving the backlog forward — default to the recommended next step that minimizes risk while making measurable progress toward the story goal.

- When the current todo list is fully processed, perform a short pass over all archived items to confirm they were properly closed and documented, then build a fresh todo list for the next development cycle.

Default operational behavior
- Proceed autonomously using the above loop: implement, test (focused), archive, and close. When in doubt, prefer incremental progress with small, fully-verified tasks that can be quickly rolled back or patched.

Goal
- Close the current story by producing a stable prototype (for example, the Telegram feature) and record the work in project history so the next story can begin from a clean state.

**Last Task Finalization (best practice)**

- Always reserve a single, explicit "finalization" task as the last item in a story's todo list. This task's purpose is to:
	- Archive runtime snapshots (move `.tmp` to an archive folder with timestamp).
	- Add a short closure note to `doc/HANDOFF.md` describing any open questions or conflicts and the next recommended story.
	- Run the full test-suite or the agreed validation set, and confirm CI passes (or record known CI workarounds).
	- Mark the story "closed" only after the above are completed. This prevents partial closures and makes audit traces consistent.

When creating or closing a story, add a `story extra` task describing candidate follow-up work; place it last so it is evaluated and not accidentally executed during the current iteration.

**Todo Task Classification (recommended fields)**

When adding items to the repo TODO list, include a short classification to help triage and prioritization. Use one of the following types and include a single-line acceptance criteria when possible:

- `bug`: a reproducible defect requiring a fix. Priority: high/med/low. Acceptance: failing test case added and passing after fix.
- `chore`: maintenance work (linting, dependency updates, CI). Priority: low/med. Acceptance: CI green and no regressions.
- `improvement`: incremental enhancement (better logging, metrics). Priority: med. Acceptance: measurable improvement (counter added, UI visible).
- `research`: spike or investigation. Priority: low. Acceptance: concise findings in `doc/` and recommended next steps.
- `story`: feature work that may include several subtasks. Priority: med/high. Acceptance: feature demo + tests + runbook updates.

Suggested metadata to include in the TODO item text: `type`, `priority`, `acceptance`, `owner` (optional), and `estimated_time` (optional). This enables faster triage and clearer automation in CI or release notes.

**Child-doc naming convention & multi-agent workflow**

When creating follow-up artifacts or dividing work between agents, use a predictable child-doc filename pattern so multiple agents can work on the same story concurrently and you can trace origin easily:

- Format: `<StoryName>.<AgentName>.<TodoTaskName>.extra.md` (example: `ImproveObservability.Alby.auto_requeue.extra.md`)
- Place child docs under `doc/` and reference the parent story in the first line using `Parent: <StoryName>` so automated tooling can collect related extras.
- Child docs should contain: short description, acceptance criteria, owner (agent/user), estimated time, and any small patches or CLI commands to run.

Workflow:

1. When a story needs follow-up ideas or split work, create one or more child docs using the naming convention above.
2. Add a one-line entry to the parent TODO describing the child doc and mark it `story.extra` for review in the next iteration.
3. During the next iteration, collect all `<StoryName>.*.extra.md` files and triage them into the main TODO list as separate tickets.

This makes it easy for different agents to propose small, scoped follow-ups without changing the parent story content directly.

**Claim lock semantics (short)**

For multi-agent claim operations we use a filesystem lock-file next to each claim file to serialize read-modify-write (RMW) operations and avoid duplicate claims:

- Lock file: `<claim-file>.lock` (example: `.tmp/claims/my_story.default.json.lock`).
- Acquisition: exclusive-create (`os.O_CREAT | os.O_EXCL`) with a short retry timeout (default 5s). If acquisition fails the operation returns `lock-timeout` so the caller can retry or surface an error.
- Scope: the lock covers the entire RMW sequence (read existing claim, evaluate TTL/takeover rules, write new claim) and is released in a `finally` block.
- Writes: claims are written via temp-file + `os.replace()` with an fsync to ensure durability before rename.

Operator notes: inspect claim files under `.tmp/claims/`, remove stale `*.lock` files only after confirming no agent is currently operating, and run `tests/test_claims_concurrency.py` to validate behavior locally.

**Applied example: `stoybl bl bl 1` classifications**

Below is an example showing how classification fields were applied to the active story's `.current` todo list (used as a template for future stories):

- `t2` — Evaluate TODO classification and apply
	- `classification`: `governance, documentation`
	- `priority`: `high`
	- `acceptance`: classifications applied to all current todo items and recorded in the story `.current` file

- `t3` — End-to-end functional test (phase 1)
	- `classification`: `test, integration`
	- `priority`: `high`
	- `acceptance`: focused unit-first tests added for admin requeue → retryer → audit traces

- `t4` — Tests: multi-agent concurrency & idempotency
	- `classification`: `test, concurrency`
	- `priority`: `high`
	- `acceptance`: unit/integration tests simulate concurrent claims and assert at-most-once semantics

- `t5` — Update runbook: agent-task workflow & token usage
	- `classification`: `documentation, runbook`
	- `priority`: `medium`
	- `acceptance`: runbook updated with naming, token guidance, and CLI examples

- `t6` — Prepare follow-up part2 (CLI/UI + runbook)
	- `classification`: `planning, cli-ui`
	- `priority`: `medium`
	- `acceptance`: part2 draft created under `doc/` and referenced from the parent story

Include a one-line acceptance criteria when adding these fields so reviewers and automated tools can quickly triage the work and the CI/test scope for each task.
