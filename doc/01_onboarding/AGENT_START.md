# Agent Start: Quick onboarding for a new agent

This is the first document a new automated agent or human should read to start contributing.

1. Environment
   - Python 3.11 recommended. Use virtualenv: `python -m venv .venv` then activate.
   - Install dev deps: `pip install -r requirements-dev.txt`.
2. Repository layout
   - `agents/` — agent scripts and CLI helpers.
   - `doc/` — canonical docs (this folder). Archived originals are under `doc/archive/`.
   - `orchestrator.py` & `gaia.db` — local audit DB used by agents for traceability.
3. Quick run: discover backlog (dry-run)

```powershell
python agents/telegram_backlog_agent.py --dry-run --limit 20
```

4. Creating issues from NDJSON (manual step requires review)

```powershell
python .tmp/create_issues.py .tmp/issues.ndjson --confirm
```

5. Where to look for more detail
   - Detailed playbooks and runbooks: `doc/03_procedural/` (or archived originals under `doc/archive/`)
