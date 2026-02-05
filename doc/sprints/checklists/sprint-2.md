# Sprint 2 Checklist — Stabilize & Harden

- [ ] Finish integration tests: acceptance flows (claim→approve→archive)
- [ ] Add idempotency and replay tests
- [ ] Implement exponential backoff and tests for 429/5xx handling ([#62])
- [ ] Complete alby_agent dry-run integration and basic metrics collection ([#63])
- [ ] Create CI job matrix to run critical integration tests in isolation

Notes: Create issues for long-running items and gate work by passing Sprint 1 CI fixes.
