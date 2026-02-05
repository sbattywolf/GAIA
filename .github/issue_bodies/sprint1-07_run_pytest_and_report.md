### Run full local `pytest -q` and produce failing-tests report

Problem
- CI shows multiple failures and errors; a focused local test run with a diagnostic report will help triage.

Goal
- Run `pytest -q` locally (with `PYTHONPATH` set as needed), capture failing tests and errors, and produce a short report with stack traces and suggested next actions.

Acceptance criteria
- A failing-tests report is produced (file: `doc/test-reports/failing-tests-<date>.md`) listing failing tests and key stack traces.
- Follow-up issues are created for the most actionable flakes.

Notes
- Use `pytest -q --maxfail=1` for quick iteration, then a full run for a full report.
- Label: `testing`, `high`