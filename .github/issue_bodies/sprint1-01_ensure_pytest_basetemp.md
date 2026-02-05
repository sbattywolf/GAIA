### Ensure pytest basetemp/writable path in CI

Problem
- CI runs fail with FileNotFoundError for `.tmp/pytest` or have no writable basetemp. This causes intermittent test errors.

Goal
- Ensure CI creates a writable basetemp directory before running `pytest`, or pass an explicit `--basetemp` to pytest.

Acceptance criteria
- CI workflow includes a step that creates a writable directory used for pytest basetemp.
- Tests run without the FileNotFoundError shown in recent runs.

Notes
- Minimal change preferred: add `mkdir -p ./.tmp/pytest` (or Windows equivalent) and export `PYTEST_ADDOPTS='--basetemp=./.tmp/pytest'` before running tests.
- Label: `ci`, `high`