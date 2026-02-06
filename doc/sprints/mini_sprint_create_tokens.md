# Mini-sprint: Create least-privilege tokens

Duration: 2 days (estimate)

Purpose
- Create and persist least-privilege tokens required by GAIA services: repo operations, actions, issue creation.
- Prefer GitHub App installation tokens; fallback to fine-grained PATs when necessary.

Tasks
- Task A: Document required token scopes per consumer (CI, agents, publisher)
- Task B: Create GitHub App (manual) and record App ID + installation ID + private key path
- Task C: Use `scripts/github_app_token.py` to generate installation tokens and persist them with `scripts/rotate_tokens_helper.py`
- Task D: Update `SecretsManager` (store `GAIA_GITHUB_TOKEN` and role‑scoped names)
- Task E: Validate consumers (run `publish_issues.py`, run CI jobs locally)
- Task F: Revoke temporary admin PAT and record revocation in audit

Acceptance criteria
- Tokens for each consumer are stored in the encrypted store under canonical names.
- CI workflows reference the new token names and complete a smoke test.
- Audit entries exist for token generation and revocation.
