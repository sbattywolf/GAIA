### Add DB test fixture / migration to provide `audit.timestamp`

Problem
- Tests fail with `sqlite3.OperationalError: table audit has no column named timestamp` due to schema mismatch in test DB.

Goal
- Add a small migration or pytest fixture that ensures test DB has `audit.timestamp` column available for tests.

Acceptance criteria
- A pytest fixture or migration runs before tests and creates/updates the `audit` table to include `timestamp`.
- CI and local test runs proceed past the previous schema error.

Notes
- Prefer a lightweight fixture that creates the needed column in the test DB rather than a full production migration, unless a proper migration scheme exists.
- Label: `testing`, `high`