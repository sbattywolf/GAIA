**STR_TODO_stoybl_bl_bl_1_tests**

Purpose
- Provide deterministic unit and integration tests that prove correctness of approval flow, requeue behavior, retryer semantics, and concurrency/idempotency.

Acceptance criteria
- Tests run on Windows and Linux in CI and pass reproducibly.
- At-most-once processing assertions for concurrent claim attempts.

Implementation plan
1. Add unit tests for `scripts/claims.py` covering happy path and TTL takeover.
2. Create concurrency test harness (`tests/test_claims_concurrency.py`) that forks multiple processes to attempt claims concurrently and asserts single winner.
3. Add end-to-end fixture that inserts a queued command, performs approve via `claim_cli.py`, and asserts `gaia.db` traces and final side-effect idempotency.
4. Add replay fixtures under `tests/fixtures/` for idempotency regression tests.

Notes
- Use `pytest-xdist` cautiously; concurrency harness should use processes and file-system timing not internal thread scheduling.
- Record failing traces under `.tmp/test_traces/` for analysis.
