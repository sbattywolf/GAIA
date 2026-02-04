**STR_TODO_stoybl_bl_bl_1_claims**

Purpose
- Implement and validate the claim primitives integration so operator approvals are durable, idempotent, and auditable.

Acceptance criteria
- `scripts/claims.py` is invoked by monitor server and `claim_cli.py` for `claim`, `release`, and `refresh` actions.
- Audit: `gaia.db` receives a compact trace for each claim lifecycle: `claim.requested`, `claim.acquired`, `claim.refreshed`, `claim.released`, `claim.taken_over` (if TTL expired).
- Windows-safe atomic semantics: temp-file write + fsync + `os.replace()` and an exclusive-create lock around RMW.

Minimum implementation steps
1. Add wrapper functions in `scripts/claim_cli.py` to call `scripts/claims.claim()` and emit `gaia.db` traces.
2. Wire monitor server approve/deny endpoints to call `claim_cli.py` rather than directly mutating files.
3. Add TTL and takeover logging: default configurable TTL (candidate: 300s) and ownership takeover policy.

Tests
- Unit tests for `claims.claim()` covering create, refresh, release, takeover.
- Concurrency test on Windows (simulate many parallel claim attempts) asserting only one successful claim at a time.

Rollout notes
- Feature-flag via env `ENABLE_CLAIMS_INTEGRATION=1` while monitoring traces.
- Short TTL for early testing (60s) to exercise takeover behavior; increase after stability proven.
