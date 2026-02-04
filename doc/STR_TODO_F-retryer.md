# TODO — F-retryer (Retryer error classification)

Status: planned

Tasks
- [ ] t23 — Map HTTP error codes for retryer (5xx/429/4xx) and tests
- [ ] t24 — Implement exponential backoff with jitter in retryer
- [ ] t25 — Add tests simulating 429 and 5xx responses

Notes
- Retryer work will follow integration test and command-safety stabilization; I'll implement error mapping helpers first.
