# Session TODOs & Next Steps

This document summarizes the work done during the recent session, the full TODO list derived from the session history, and immediate next actions. Use this as the single-source actionable checklist for follow-ups.

## Summary
- Core work completed: Alby agent templates, Scrum agents (backlog/planner/assigner), orchestrator reclaim/report, reclaimer CLI update, start/stop automation, timestamped logs, rotation + archiving, CI scheduled dry-run workflow, unit tests, sample flow smoke runs.
- Repo housekeeping: renamed `AILocalModelLibrary` → `TOBEDELETE__AILocalModelLibrary` and updated `.gitignore` (index cleanup may still be required).

## Full TODO List (actionable)

1. Update docs summary: Create this file summarizing session work and TODOs. (in-progress)
   - File: docs/SESSION_TODOs.md — contains session summary and todo list.

2. Add archive pruning: delete archived zips older than N days. (not-started)
   - Implement `-ArchiveRetentionDays` in `scripts/rotate_logs.ps1`.
   - Honor `-DryRun` and default to safe value (recommended: 90 days).

3. Verify git index cleanup for renamed folder. (not-started)
   - Run `git ls-files | Select-String AILocalModelLibrary` and `git rm --cached` for any remaining tracked files.

4. Add log rotation and retention. (completed)
   - Implemented in `scripts/start_agents.ps1` and `scripts/rotate_logs.ps1`.

5. Enhance rotate_logs: timestamped archives + cutoff. (completed)
   - Old logs are archived to `.tmp/logs/archive` with original timestamps in zip names.

6. Implement Alby agent templates. (completed)
   - `agents/alby_agent_template.py`, `agents/alby_online_agent.py`.

7. Implement Scrum agents. (completed)
   - `agents/scrum_backlog.py`, `agents/sprint_planner.py`, `agents/task_assigner.py`.

8. Orchestrator reclaim & report. (completed)
   - `orchestrator.py` includes `reclaim_and_report()`.

9. Update reclaimer CLI. (completed)
   - `agents/reclaimer.py` accepts `--status-file`.

10. Start/stop automation scripts. (completed)
    - `scripts/start_agents.ps1`, `scripts/stop_agents.ps1` manage agent processes and logs.

11. CI rotate-logs dry-run workflow. (completed)
    - `.github/workflows/rotate-logs.yml` runs rotation in dry-run on schedule.

12. Add unit tests for agents. (completed)
    - Tests added under `tests/` for backlog, planner, assigner, and reclaimer status file.

13. Run sample flow smoke tests. (completed)
    - `scripts/run_sample_flow.py` validated the import→plan→assign flow.

14. PowerShell cross-platform checks. (not-started)
    - Verify scripts on CI runners and Linux/macOS PowerShell Core; add platform fallbacks if needed.

15. Add safe delete flag. (not-started)
    - Add explicit `--force`/`--Confirm` to `rotate_logs.ps1` to require confirmation for deletions when not in dry-run.

## Immediate Next Actions (recommended)

- Implement and test archive pruning (item 2) in dry-run mode locally:

  ```powershell
  # dry-run: list what would be deleted
  ./scripts/rotate_logs.ps1 -Keep 3 -ArchiveAfterDays 7 -ArchiveRetentionDays 90 -DryRun
  ```

- Verify Git index for previously tracked AILocalModelLibrary files:

  ```powershell
  git ls-files | Select-String -Pattern 'AILocalModelLibrary' -CaseSensitive
  # if results found:
  git rm --cached <path/to/tracked/file>
  git commit -m "chore: stop tracking AILocalModelLibrary files"
  ```

- Once dry-run output looks correct, run rotation without `-DryRun` on a controlled machine or CI job with `--Confirm`/`--Force` guarded.

## Notes and Safety
- All deletion steps are guarded by `-DryRun` output in current scripts; prefer dry-run first.
- Consider adding a `--Force` flag to `rotate_logs.ps1` for non-interactive CI deletion; do not enable automatic destructive deletes in scheduled workflows without audit.

---
Generated from session history on 2026-02-02.
# Session Todo Snapshot

This file was generated from the agent session todo list. Use `scripts/session_todo.py` to regenerate from an NDJSON archive.

- [x] Read full repository — Enumerate repo files and read key files to extract patterns, workflows, and integration points.
- [x] Draft generic documentation template — Create a reusable, detailed template guide for future software projects.
- [x] Draft GAIA-specific documentation — Create a GAIA-focused detailed doc mapping architecture, event schemas, agent patterns, run/debug steps, and suggested improvements.
- [x] Add docs to repo — Write the two docs into `docs/` and commit via apply_patch.
- [x] Validate and finalize — Re-open created files for review, update todo statuses to completed, and ask for feedback.
- [x] Add tests — Add pytest unit tests for `agents/backlog_agent.py` and `scripts/append_todo.py`.
- [x] Add CI workflow — Add GitHub Actions workflow `.github/workflows/python-tests.yml` to run tests on push/PR.

New / follow-up tasks:

- [ ] Import external best-practice docs from `E:\Workspaces\Git\AILocalModelLibrary` (manual or copy-in) and map useful sections into `docs/TEMPLATE_SOFTWARE_DOC.md`.
- [ ] Implement `--dry-run` and `agent_utils.py` stubs to make agents testable and centralize event construction.
- [ ] Add `requirements-dev.txt` (include `pytest`) and update `README.md` with test commands.
- [ ] Automate periodic docs review: add a scheduled GitHub Action or a scripted reminder in `scripts/`.

To regenerate this file from an NDJSON archive:

```powershell
python scripts/session_todo.py --ndjson path\to\todo-archive.ndjson --out docs/SESSION_TODOS.md
```
