# GAIA Token Rotation — Action Plan (8 steps)
Date: 2026-02-06

Goal: complete safe rotation of automation tokens and update CI/agents to use least-privilege credentials.

Steps (short, actionable)

1) Inventory tokens & usages
- Run automated discovery and manual review to list all tokens, secrets, and where they are used (CI, workflows, agents, scripts, external services).
- Output: `rotation/inventory.json` and a short CSV mapping token -> consumers.

2) Choose automation method & create GitHub App
- Decision: prefer GitHub App (recommended) for short-lived, install-scoped tokens. If not possible, create fine-grained PATs per purpose.
- Create App, generate private key, record `APP_ID` and `INSTALLATION_ID`.

3) Generate least-privilege tokens per consumer
- For each consumer (actions, publisher, agents), create an installation token or fine‑grained PAT with minimal scopes.

4) Persist tokens to canonical secret store
- Use `scripts/rotate_tokens_helper.py` or `scripts/github_app_token.py --persist` to write tokens into encrypted store under canonical names (`GAIA_GITHUB_TOKEN`, `GAIA_CI_TOKEN`, etc.).

5) Validate consumers (smoke tests)
- Run `scripts/validate_consumers.py` to run tests, request a token from token-cache, and optionally run a dry-run publish.
- Fix any consumer that fails with least-privilege token; iterate until green.

6) Update CI/workflows and repo secrets
- Replace legacy `GITHUB_TOKEN` reliance and repo-wide secrets with scoped repo secrets / environment secrets that reference the new token names.
- Update `.github/workflows/*` to use the new secrets; add a CI job to exercise token-cache if needed.

7) Revoke temporary admin PAT and cleanup
- Once all consumers are validated and CI updated, revoke the short-lived admin PAT used for orchestration. Record the revocation in `gaia.db` and `events.ndjson`.

8) Audit, finalize runbook, and create CHECKPOINT PR
- Run audit scripts, collect evidence, update `doc/TOKEN_ROTATION_PLAYBOOK.md` with exact commands performed, and open a CHECKPOINT PR for review before merging changes permanently.

Notes & safety
- Create a `CHECKPOINT` artifact before steps 5-7 so reviewers can approve critical actions.
- Keep `GAIA_TEST_MODE` for local testing but never use it for production automation.

Files & tools referenced
- `scripts/github_app_token.py`, `scripts/rotate_tokens_helper.py`, `gaia/token_cache.py`, `scripts/token_cache_server.py`, `scripts/validate_consumers.py`.

<!-- Audit: Merged from 2026-02-06 — see doc/SPRINT_MERGED_2026-02-06.md -->

## Progress Snapshot (from MASTER_BACKLOG)

Applied sprint progress highlights:

| ID | Status | Scrum Pt | Score |
|---:|---|---:|---:|
| T002 | completed | 8 | 50 |
| T003 | completed | 8 | 50 |
| T004 | completed | 8 | 50 |
| T005 | completed | 5 | 20 |
| T007 | completed | 2 | 10 |
