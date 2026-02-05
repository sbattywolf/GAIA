### CI failures observed for PR #72 (fix/ci-tty-guards)

Runs captured:
- Auto PR If Tests Pass — https://github.com/sbattywolf/GAIA/actions/runs/21722816745 (failure)
- Secret scanning — https://github.com/sbattywolf/GAIA/actions/runs/21722793962 (failure)
- CI — https://github.com/sbattywolf/GAIA/actions/runs/21722793929 (failure)
- CI (fixed) — https://github.com/sbattywolf/GAIA/actions/runs/21722793916 (failure)
- .github/workflows/ci-integration.yml — https://github.com/sbattywolf/GAIA/actions/runs/21722792514 (failure)

Suggested next steps
1. Inspect logs for `Secret scanning` failures (may be unrelated to TTY guards) and address CI-run-specific failures.
2. If `approve_checkpoint` or `approve_ui` TTY guards prevent non-interactive flows, ensure `--yes` usage is allowed where appropriate and documented.
3. Create targeted issues for failing tests discovered in logs.

Reference: PR #72 — https://github.com/sbattywolf/GAIA/pull/72
