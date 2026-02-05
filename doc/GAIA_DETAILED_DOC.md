# GAIA — Project-Specific Documentation

Purpose
- Companion doc for GAIA that maps the generic template into concrete, actionable guidance for contributors and AI agents.

Big picture architecture
- CLI-first agent scaffold: agents are small scripts under `agents/` that perform an external action (optional) then emit an NDJSON event to `events.ndjson`.
- Orchestrator / audit: `orchestrator.py` initializes a SQLite DB (`gaia.db`) with a simple `audit` table. Use this DB to store authoritative, idempotent records for actions that change state.

Key files & responsibilities
- `agents/backlog_agent.py`: canonical agent pattern — parse args, call `gh` if available, construct event with `type: issue.create`, append to `events.ndjson`.
- `orchestrator.py`: DB initialization. Re-run to ensure schema present before audit writes.
- `scripts/append_todo.py`: demonstrates NDJSON append patterns and atomic writes.
- `doc/HANDOFF.md`: contains run steps for prototype SSE server and useful resume commands.

Event schema (concrete)
- Example event (canonical):

  ```json
  {
    "type": "issue.create",
    "source": "backlog_agent",
    "target": "<repo-dir-name>",
    "task_id": null,
    "payload": {"title": "...","body":"...","issue_url": "..."},
    "timestamp": "2026-02-02T...Z",
    "trace_id": "<uuid>"
  }
  ```

Run & debug (Windows)
- Setup venv and install deps (see `README.md`).
- Start session loader: `.\scripts\start_session.ps1`.
- To test agents with no remote side-effects:

  ```powershell
  set PROTOTYPE_USE_LOCAL_EVENTS=1
  python agents/backlog_agent.py --title "Test" --body "local"
  ```

Audit writes (suggested pattern)
- When an agent performs a state-changing action, also insert a concise audit row in `gaia.db`:

  ```sql
  INSERT INTO audit (timestamp, actor, action, details) VALUES (?, ?, ?, ?)
  ```

- Use `orchestrator.py`'s `init_db()` to ensure table exists.

Testing recommendations for GAIA
- Unit-test agent logic by mocking subprocess calls to `gh` and validating `append_event()` output.
- Add a small integration test that runs the agent in a temp dir and asserts an NDJSON line appended with valid JSON and expected keys.

Small improvements to consider
- Add a `--dry-run` flag to agents to emit the event locally without calling external CLIs.
- Add an `agent_utils` module to centralize event construction, timestamping, and atomic append helpers.
- Provide a simple test helper that sets `PROTOTYPE_USE_LOCAL_EVENTS=1` and cleans up `events.ndjson` after tests.

Docs & maintenance
- Keep `docs/GAIA_DETAILED_DOC.md` as the living GAIA doc derived from the template. Run a periodic review and append a changelog section.

Next steps I can take
- Add unit/integration test stubs; implement `agent_utils.py`; add `--dry-run` to `backlog_agent.py`.

## Free-software policy & install sequence (GAIA)

GAIA restricts tooling to free/open-source software by default. Any proposal
to introduce a non-free tool must include a short justification and available
free alternatives.

Recommended GAIA install sequence (Windows PowerShell / POSIX):

- Install Git
- Install Python 3.10+
- Create and activate venv: `python -m venv .venv` and activate per OS
- Install runtime deps: `pip install -r requirements.txt`
- Install dev deps: `pip install -r requirements-dev.txt`
- Install `gh` (GitHub CLI) for issue automation when permitted

Set environment variables in `.env` (do not commit secrets). For local-only
testing, set `PROTOTYPE_USE_LOCAL_EVENTS=1` or run agents with `--dry-run`.
