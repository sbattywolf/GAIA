## GAIA — History & Session Tracing: Best Practices

Purpose
-------
This document is a concise, human-readable guide and reference for tracing work across sessions. It contains routines, checklists, templates, and examples to:

- Resume work cleanly from a previous session.
- Keep a durable, audit-friendly history of todos and decisions.
- Provide a repeatable end-of-session shutdown routine that leaves the workspace ready for restart.

Use this as the canonical "session handbook" for GAIA and related local development.

1. Quick Principles
-------------------

- Single source of truth: keep the active todo list and session notes in files under `Gaia/doc/` or the project root.
- Append-only audit: every new todo or important decision is appended to a rolling log (NDJSON or plain text) so history is never lost.
- Short, repeatable rituals: start/stop procedures should be short checklists you can run without having to remember details.

2. File Layout (suggested)
--------------------------

- `Gaia/doc/HISTORY_TRACING.md` — this handbook.
- `GAIA/events.ndjson` — append-only event stream for agent events and important actions.
- `GAIA/events.log` — human-friendly rolling log (optional).
- `Gaia/doc/session_notes.md` — per-session notes (one per session / or timestamped headings).
- `Gaia/doc/todo-archive.ndjson` — each time a todo is added, append a record here.

3. Starting a Session (Resume Routine)
-------------------------------------

1. Open the project and activate the venv:

```powershell
& .\.venv\Scripts\Activate.ps1
cd E:\Workspaces\Git\GAIA
```

2. Read the last session summary quickly:

- Open `Gaia/doc/session_notes.md` and skim the most recent heading.
- Open `GAIA/events.ndjson` tail (or `Get-Content GAIA\events.ndjson -Tail 50`) to see recent events.

3. Update the todo list following this order (automated or manual):

- Completed tasks: list them by completion time (most recent first).
- Active tasks: list by priority (highest first).
- Remaining todos: list by priority (highest first).

4. For each completed task, check whether it needs rework; if yes, add a new todo and append to `Gaia/doc/todo-archive.ndjson`.

4. Minimal Resume Checklist (1–5 minutes)
----------------------------------------

- Start virtual environment and required services (local DB, dev servers).
- Tail `GAIA/events.ndjson` for recent agent activity.
- Run quick health commands (e.g., `python GAIA/orchestrator.py` to ensure DB exists).
- Reconcile the todo list with on-disk state; update `Gaia/doc/session_notes.md` with an intent paragraph.

5. Adding a Todo (routine)
--------------------------

When a new todo is created (manually or by an agent), follow this routine:

1. Add the task to the active todo list (project-managed list).
2. Append a record to `Gaia/doc/todo-archive.ndjson` with the following JSON shape:

```json
{
  "timestamp": "2026-02-02T12:00:00Z",
  "added_by": "username|agent",
  "title": "Short task title",
  "description": "Longer description",
  "priority": 100,
  "trace_id": "uuid"
}
```

3. If the todo is urgent, tag it in the active list and notify the human operator (console/email/Telegram).

6. End-of-Session Routine (Shutdown Checklist)
---------------------------------------------

Before you stop working for the day or hand off the machine, perform these steps.

1. Finish or checkpoint live work: commit in-progress state to git (or stash), and make a short note in `Gaia/doc/session_notes.md` under a timestamped heading describing what remains.

```powershell
git add -A
git commit -m "WIP: session checkpoint - <short note>" || echo "Nothing to commit"
```

2. Stop local services started for the session (examples):

- Stop dev servers (e.g., Ctrl+C in terminals), stop DB if started locally.
- If you used background processes, run your stop script or list/kill by PID.

3. Aggregate diagnostics and suggestions for next session:

- Append a short summary block to `Gaia/doc/session_notes.md` with:
  - What was done
  - What needs to be done next
  - Any blocking issues or environment notes

4. Update all docs that changed (todos, README snippets, or quick how-tos).

5. Prepare the machine: close applications not managed by agents and remind yourself of anything that must remain open.

6. Optional: write a `shutdown_manifest.txt` that lists processes intentionally left running (so next session you know what to start).

7. Sample End-of-Session Template (paste into session_notes.md)

```
## Session: 2026-02-02T12:10Z
- Completed: Implemented backlog_agent prototype (created GAIA/events.ndjson entry)
- Next: Initialize local git repo and push to remote
- Blockers: Need `gh` auth to create remote
```

7. Automation and Tooling Suggestions
------------------------------------

- Small scripts to support the routines:
  - `scripts/append_todo.py`: append todos to `Gaia/doc/todo-archive.ndjson` (atomic write).
  - `scripts/start_session.ps1`: activate venv, start required dev services, tail events.
  - `scripts/end_session.ps1`: commit WIP, stop services, and roll up session notes.

- Events vs. human text:
  - Use `GAIA/events.ndjson` for structured events that agents emit.
  - Use `Gaia/doc/session_notes.md` for readable human narrative and decisions.

8. Git Initialization (one-off: when you're ready)
------------------------------------------------

If you want me to initialize the `GAIA` repo locally and make the first commit, run:

```powershell
cd GAIA
git init
git add -A
git commit -m "Initial scaffold: GAIA repo"
```

To create a remote repo using `gh` and push (requires `gh auth login` already done):

```powershell
gh repo create <your-username>/GAIA --public --source=. --remote=origin --push
```

9. Quick Templates
------------------

- Todo JSON (for `todo-archive.ndjson`): see section 5.
- Session note heading:

```
## Session: 2026-02-02T<HHMM>Z
- Start: <time>
- End: <time>
- Summary: <one-line>
- Details: <free text>
```

10. How to Use This Document
---------------------------

- Read the "Starting a Session" section at session start; follow the 1–5 minute checklist to orient yourself.
- At session end, run the shutdown checklist and add the session note summary.
- Keep `Gaia/doc/todo-archive.ndjson` append-only and machine-friendly so agents can safely add items.

12. Archival policy: keep recent closed todos
-------------------------------------------

To keep the active todo view concise while preserving history, follow this
procedure:

- Retain the 7 most recent closed todo items in the active `todo-archive.ndjson`.
- Move older closed todo records into a separate archival file `Gaia/doc/todo-archive-older.ndjson`.
- Non-closed (open/active) todos remain in `todo-archive.ndjson`.

A helper script `scripts/prune_closed_todos.py` is provided to perform this
operation safely. Run it as part of the end-of-session routine or as a
scheduled maintenance job.

Example (keep 7 closed items):

```powershell
python scripts/prune_closed_todos.py --ndjson Gaia/doc/todo-archive.ndjson --keep 7
```

Notes:

- This preserves full history in the `todo-archive-older.ndjson` file while
  keeping the active archive compact for human review.
- The script looks for `status: "closed"` or `closed: true` fields to
  identify closed todos. If your workflow records closures differently,
  adapt the script or add a `status` field when closing a todo.

13. Monitoring events
---------------------

Use `scripts/monitor_events.py` to produce a quick metrics summary of the
`GAIA/events.ndjson` stream (counts by event type, duplicate traces, error
counts). Useful as a quick health check before deciding to enable a
controller.

Example:

```powershell
python scripts/monitor_events.py --events GAIA/events.ndjson
```

11. Appendices (Ideas for extensions)
------------------------------------

- Add a `session_index.json` that maps session timestamps to filenames for quick lookup.
- Add a tiny web UI that reads `GAIA/events.ndjson` and `Gaia/doc/todo-archive.ndjson` to show timeline and search.
- Integrate a lightweight agent that, on session start, runs the resume checklist and posts a short summary to a configured chat (Telegram/Matrix).

---

If you'd like, I can:

- Initialize the local git repo in `GAIA` and make the first commit now.
- Add the `scripts/start_session.ps1` and `scripts/end_session.ps1` helpers.
- Implement `scripts/append_todo.py` to atomically append to `Gaia/doc/todo-archive.ndjson`.

Tell me which of these you'd like next.
