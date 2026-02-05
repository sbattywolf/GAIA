# Release notes — Sprint snapshot (2026-02-05)

Summary:
- Normalized high/critical todos into `doc/todo-archive.ndjson` and created issue drafts.
- Opened issues for key high/critical tasks and linked them in `05_02_project_overview.md`.
- Patched CI workflows to ensure `PYTHONPATH` or editable install before running tests.

PRs and issues:
- PR merged: feat/normalize-todos → master (includes `doc/todo-archive.ndjson`, issue drafts)
- Issues created: #59, #60, #61, #62, #63

CI summary:
- Recent CI run after merge completed successfully; earlier failures traced to missing test temp directories, DB schema mismatch (`audit.timestamp`), and terminal IO in scripts (causing OSError in CI environment). See CI logs for details.

Next recommended actions:
1. Add CI step to create `.tmp/pytest` directory before tests or ensure pytest `--basetemp` is set to a writable path.
2. Ensure `orchestrator.py` / DB migrations create `audit.timestamp` column (or migrate schema) before tests that expect it.
3. Update scripts that read/write TTY to avoid `ioctl` calls in CI (use non-interactive fallbacks).

Authored-by: GitHub Copilot (automated agent)
