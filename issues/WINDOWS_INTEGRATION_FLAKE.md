# Windows integration test: intermittent subprocess handle failure

Summary
-------
An intermittent integration test failure has been observed on Windows related to subprocess/handle behavior. The failure appeared earlier during runs in this workspace, but the full test suite later passed. This file records observations, reproduction steps, and suggested next steps.

Observed behavior
-----------------
- Earlier test run (local) showed: 1 failing integration test due to a subprocess handle error on Windows (non-deterministic).
- Subsequent full test run completed successfully: `78 passed, 1 skipped`.
- Pytest additionally emitted an `Unknown pytest.mark.e2e` warning which was later fixed by registering the marker in `pytest.ini`.

Context / likely cause
----------------------
- The integration test interacts with subprocesses or platform-dependent handles (PowerShell or child process management). On Windows, handle inheritance and process termination semantics can cause flaky failures when tests assume POSIX-like behavior.
- Environment constraints (antivirus, long-running background processes, or other tests) may affect timing and handles.

Reproduction steps
------------------
1. Ensure a clean workspace and virtualenv. Example (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest tests -q
```

2. If the failure reproduces intermittently, re-run the failing test with increased verbosity and capture stdout/stderr:

```powershell
python -m pytest tests/path/to/failing_test.py::test_name -q -r a -s
```

Collected logs
--------------
- See `events.ndjson` for audit traces around test runs. The pytest output in the session recorded `78 passed, 1 skipped` when the suite passed; earlier session notes indicated a single failing integration test caused by a subprocess handle issue.

Suggested next steps
--------------------
- Re-run the failing integration test exclusively several times in CI on Windows to measure flakiness frequency.
- If reproducible, add logging around subprocess invocation to capture command, stdout/stderr, exit code, and exception traceback.
- Consider refactoring the test to avoid relying on ephemeral process handle semantics, or add robust retries/timeouts and explicit process termination.
- Optionally open a GitHub Issue linking to this file and include CI job logs when available.

Who can help
------------
- Developers familiar with the test harness: `agents/`, `scripts/automation_runner.py`, and the integration tests under `tests/e2e/`.

Reference
---------
- `pytest.ini` — marker registration
- `events.ndjson` — audit/event timeline
- `tests/e2e/` — likely location for the integration test
