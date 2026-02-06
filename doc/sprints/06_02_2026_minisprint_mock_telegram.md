## Mini-sprint: Mock Telegram harness (2026-02-06)

- Duration: 1–2 hours
- Owner: infra / automation
- Priority: High

Goal:
- Provide a minimal, dependency-free mock of the Telegram HTTP API for local testing and CI.

Deliverables:
- `agents/mock_telegram.py` — minimal HTTP server that accepts `POST /sendMessage` and appends NDJSON events to an output file.
- `tests/test_mock_telegram.py` — pytest test that starts the server and verifies a POST results in one NDJSON event.
- Example run instructions in this document for developers.

Steps (timeboxed):
1. Run unit test locally (30m):

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q tests/test_mock_telegram.py
```

2. Dry-run integration (30–60m): start server and exercise via curl or script, verify `mock_telegram_events.ndjson` contents.

3. Create follow-up tasks (15m): add CI job to run the mock server test and document how to use it in `README_RUNBOOK.md`.

Notes:
- The mock harness is intentionally minimal so it can run in CI without external packages.
- If you need richer Telegram semantics (inline keyboards, updates), extend the handler incrementally and add focused tests.
