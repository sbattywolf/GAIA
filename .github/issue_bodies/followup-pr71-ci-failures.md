### CI failures observed for PR #71 (fix/ci-basetemp)

Runs captured:
- Auto PR If Tests Pass — https://github.com/sbattywolf/GAIA/actions/runs/21722807937 (failure)
- Secret scanning — https://github.com/sbattywolf/GAIA/actions/runs/21722563272 (failure)
- CI — https://github.com/sbattywolf/GAIA/actions/runs/21722563269 (failure)
- CI (fixed) — https://github.com/sbattywolf/GAIA/actions/runs/21722563263 (failure)
- .github/workflows/ci-integration.yml — https://github.com/sbattywolf/GAIA/actions/runs/21722559828 (failure)

Suggested next steps
1. Inspect the `CI` and `ci-integration.yml` run logs for first-failure stack traces (import errors, DB schema, pytest basetemp).
2. If failures are unrelated to basetemp (e.g., DB schema), open targeted fixes (small migrations/fixtures) or mark as blockers.
3. If basetemp change fixed the FileNotFoundError but other tests fail, capture failing test names and create specific issues.

Reference: PR #71 — https://github.com/sbattywolf/GAIA/pull/71
