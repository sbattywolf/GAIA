**GAIA Onboarding: Tools, env, and reusable helpers**

Purpose
-------
This document lists the generic, reusable utilities and procedures onboarded into this `GAIA` repo from the larger workspace. It focuses on non-agent functionality needed to run, resume, and maintain sessions locally.

Included tools
--------------

- `scripts/append_todo.py` — small Python helper to atomically append todo records to `Gaia/doc/todo-archive.ndjson`.
- `scripts/start_session.ps1` — Windows PowerShell helper to activate the venv and tail `events.ndjson`.
- `scripts/end_session.ps1` — Windows PowerShell helper to checkpoint (git commit), backup `events.ndjson`, and append a session note.
- `.env.example` — example environment variables file; store secrets in local `.env` (not committed).
- `doc/HISTORY_TRACING.md` — session tracing handbook (already present).

Why these were chosen
---------------------

- Generic: suitable for any local GAIA usage (not agent-specific).
- Low-risk: no secrets or external service integrations included.
- Helpful: improve reproducibility for session start/stop and maintain an audit trail of todos.

Environment & identity notes (workarounds)
-----------------------------------------

- Secrets: use a local `.env` (copy `.env.example`) or Windows Credential Manager; never commit tokens.
- `gh` auth: prefer `gh auth login` and Git Credential Manager for Windows; document the requirement in `README.md`.
- PATH: if CLI tools (e.g., `gh`, `glab`, custom CLIs) aren't on PATH, add them locally or use explicit full paths in scripts. Use `.env` var `PATH_APPEND` to list additions and a small loader script to prepend them to the process PATH during session start.

Recommended next steps
----------------------

1. Create `.env` from `.env.example` and populate `GH_TOKEN` if you want automated `gh` operations.
2. Make `scripts/append_todo.py` executable in your venv and test adding a todo:

```powershell
& .\.venv\Scripts\Activate.ps1
python scripts/append_todo.py --title "Test task" --description "Verify todo logging" --priority 50
```

3. Use `scripts/start_session.ps1` at session start and `scripts/end_session.ps1` at the end to standardize the workflow.

What I did not copy
-------------------

- Agent-specific code and internal Alby integrations (per your request).
- Large prototype-only servers unless you ask me to bring them in as optional dev tools.

If you want
----------

- I can add a small `scripts/load_env.ps1` that reads `.env` and applies `PATH_APPEND` and other variables for the session.
- I can add an automated `Makefile`/PowerShell task runner to standardize commands across Windows and *nix.
- I can copy the `monitoring_prototype/serve_prototype_with_data.py` into a `tools/` folder as an optional dev server (not enabled by default).

Added now
---------

- `scripts/load_env.ps1` — loads `.env` into PowerShell session and applies `PATH_APPEND`.
- `scripts/secret_helper.py` — Python helper: uses Bitwarden CLI (`bw`) if present, otherwise falls back to environment or `.env`.
- `scripts/install_workbook.ps1` — checks for common tools (`gh`, `bw`, `python`) and prints suggested install commands (winget). Does not auto-install by default.

Secrets recommendation
----------------------

I recommend using the Bitwarden CLI (`bw`) as the primary secrets store for GAIA because:

- Cross-platform and free tier available.
- CLI is scriptable and suitable for local developer flows.
- Works well with GitHub CLI workflows (store `GH_TOKEN` securely).

Workflow example
----------------

1. Install and login to Bitwarden locally (`bw login`) and unlock with `bw unlock`.
2. Store secrets under a clear name (e.g., `GAIA_GH_TOKEN`) and in scripts call `scripts/secret_helper.py GAIA_GH_TOKEN` to retrieve it.
3. Keep `.env` as emergency fallback only (copy `.env.example` to `.env`), and never commit real secrets.

Workbook automation idea
-----------------------

- `scripts/install_workbook.ps1` helps enumerate missing tools and suggests `winget` commands. Later we can extend it to perform unattended installs and to capture approvals automatically using a local approvals file.

Next steps I can implement
-------------------------

- Add `scripts/load_env.ps1` invocation to `scripts/start_session.ps1` so `.env` is applied automatically when starting a session.
- Add a small `scripts/secret_demo.ps1` that demonstrates retrieving `GH_TOKEN` via `scripts/secret_helper.py` and exporting it for the session.
- Extend `install_workbook.ps1` to optionally perform installs after user confirmation and to record installed versions in a `tools_manifest.json`.


Tell me which of the above you'd like next, and I'll implement it.
