# External Reference: AILocalModelLibrary (imported)

This index summarizes useful files and suggested actions after importing `AILocalModelLibrary` into this workspace as a reference for GAIA implementation.

Key locations to review
- `AILocalModelLibrary/PROTOTYPE_WORKING_GUIDE.md` — shutdown/resume checklist and diagnostic steps for prototype servers (useful for GAIA SSE/proxy patterns).
- `AILocalModelLibrary/AGENT_TASKS/agent_runtime/` — runtime helpers, SSE monitoring, and tailer examples.
- `AILocalModelLibrary/services/` — service implementations and RoleArbiter pattern (see `README.md` top-level examples).
- `AILocalModelLibrary/tests/` — unit and integration test patterns to reuse (mocks, temp dirs).
- `AILocalModelLibrary/requirements-dev.txt` — dev dependency suggestions (pytest, linting tools).

Suggested actions to integrate useful bits into GAIA
- Extract small snippets into `docs/` (e.g., shutdown checklist, SSE troubleshooting) rather than copying large binary artifacts.
- Reuse RoleArbiter examples to design any scheduled job runner for GAIA; copy a minimal `RoleArbiter` example into `agents/README.md` if helpful.
- Add test helpers from `AILocalModelLibrary/tests/` to GAIA `tests/` (mocks for subprocess, tempdir fixtures).

Cleanup notes
- Heavy directories and envs have been added to `.gitignore` to avoid tracking `.venv`, `dist/`, and temp artifacts.
- If you want to permanently prune large files (tar.gz, backups), list them and I can remove them from the workspace.

How to use this reference
- Search `AILocalModelLibrary` for patterns you want to adopt, then copy only the minimal code and tests into GAIA under a suitable namespace (e.g., `agents/utils/` or `tests/helpers/`).
- Prefer small, reviewable snippets rather than entire folders to keep repository size manageable.
