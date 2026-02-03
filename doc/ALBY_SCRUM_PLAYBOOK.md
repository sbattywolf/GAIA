# Alby Scrum Playbook (Minimal Starter)

Purpose
- Provide a minimal, repeatable template for using Alby agents to manage backlog, sprints, and tasks.

Principles
- Agents are CLI-first and emit NDJSON events to `events.ndjson`.
- Keep stories small: split epics into stories, stories into tasks.
- Prefer idempotent operations and include `trace_id`/`task_id` in events.
- Use `orchestrator` queue for actionable tasks that require a worker.

Core Components
- `agents/alby_agent_template.py`: Minimal agent template for story lifecycle events.
- `agents/scrum_backlog.py`: (planned) watch and normalize incoming backlog items.
- `agents/sprint_planner.py`: (planned) create sprint manifests and schedule tasks.
- `agents/task_assigner.py`: (planned) assign tasks and create orchestrator work items.
- `agents/worker.py`: claims work from `orchestrator` and runs handlers.
- `events.ndjson`: canonical event stream.
- `gaia.db`: SQLite audit and queue created by `orchestrator.py`.

Event Examples
- story.created
  - payload: { title, description, created_at, meta }
- story.split
  - payload: { story_id, parts }
- sprint.planned
  - payload: { name, start, end }
- task.assigned
  - payload: { task_id, assignee }

Suggested Workflow
1. Author creates a story via `agents/alby_agent_template.py create-story` or by importing JSON.
2. `scrum_backlog` normalizes the story and emits a `story.normalized` event.
3. `sprint_planner` listens for prioritized items and emits `sprint.planned` and task events.
4. `task_assigner` creates orchestrator tasks via `orchestrator.enqueue_task(...)` for heavy operations.
5. `worker` claims and completes tasks; `reclaimer` handles stale claims.
6. `scripts/scrum_dashboard.py` renders the board from `events.ndjson` and `gaia.db`.

Extending
- Use `agents.agent_utils.build_event()` and `append_event_atomic()` to ensure consistent events.
- Add unit tests under `tests/` that assert event emission and queue interactions.
- Add CI workflow to run tests and start integration agents in ephemeral mode.

Next Steps (quick)
- Implement `scrum_backlog`, `sprint_planner`, and `task_assigner` as separate agents.
- Add `examples/sample_backlog.json` and import script.
- Wire up a GitHub Actions workflow to run tests on PRs.

Online Integration (Alby 0.3 nextagent prototype)
- Create an online-capable agent that bridges local events to remote issue trackers (example: GitHub via `gh`).
- Use `agents/alby_online_agent.py` as the scaffold: it attempts to create remote issues and falls back to emitting local events when remote access is unavailable or for dry-runs.
- Environment: document `GH`/`GITHUB_TOKEN` and `gh` CLI usage; prefer `--dry-run` for CI and ephemeral runs.
- Keep remote ops idempotent: include `trace_id`, suggested `task_id`, and original payload in the event to allow reconciliation.

This file pairs with `agents/alby_agent_template.py` for local-first workflows and `agents/alby_online_agent.py` for online interactions.

