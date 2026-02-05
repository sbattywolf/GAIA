# Secrets handling and recommended token workflow

This document describes recommended steps to create, store, and rotate repository tokens used by automation.

## Principles
- Use least privilege: create distinct tokens for distinct purposes (repo-level vs org-level).
- Prefer fine-grained PATs or GitHub Apps over classic PATs when possible.
- Never commit real tokens. Keep `.env.template` in repo and populate a local `.env` or use repo/org secrets.

## Recommended token names (as repo secrets)
- Do NOT use secret names that begin with `GITHUB_` — the Actions secrets API rejects those names (HTTP 422).
- Use these recommended names instead:
   - `AUTOMATION_GITHUB_TOKEN` — token for repo automation (repo-scoped or fine-grained)
   - `AUTOMATION_GITHUB_TOKEN_ORG` — token for org-level operations (only if required)

Mapping to local env (example):
- In your local `.private/.env` or `.env`, set `AUTOMATION_GITHUB_TOKEN` and `AUTOMATION_GITHUB_TOKEN_ORG` values.
- The helper scripts in `scripts/` read `GITHUB_TOKEN_VALUE` and `GITHUB_TOKEN_ORG_VALUE` env vars or prompt interactively; you can export them from your loaded `.env` before running the helper.

## How to create and set secrets (example)

1. Create the tokens on GitHub:
   - Classic personal access token: https://github.com/settings/tokens/new
   - Or use a fine-grained token or GitHub App for better control.

2. Locally set `gh` to use your token (run locally, do NOT paste token into chat):

```powershell
# non-interactive
# echo <YOUR_TOKEN> | gh auth login --with-token
```

gh secret set GITHUB_TOKEN --repo sbattywolf/GAIA --body '<token-value>'
gh secret set GITHUB_TOKEN_ORG --repo sbattywolf/GAIA --body '<org-token-value>'
3. Set repository secrets (PowerShell example):

```powershell
gh secret set AUTOMATION_GITHUB_TOKEN --repo sbattywolf/GAIA --body '<token-value>'
gh secret set AUTOMATION_GITHUB_TOKEN_ORG --repo sbattywolf/GAIA --body '<org-token-value>'
```

Or using the helper scripts in `scripts/`:

```powershell
.\scripts\set_repo_secrets.ps1 -Repo sbattywolf/GAIA
```

Or (bash):

```bash
./scripts/set_repo_secrets.sh sbattywolf/GAIA
```

## Rotation guidance
- Rotate tokens on a regular cadence (e.g., 90 days) or immediately after any suspected leak.
- When rotating: 1) create new token, 2) add new token to secrets (as backup), 3) flip workflows to use new secret, 4) revoke old token.

## Audit & detection
- Keep `detect-secrets` baseline in place and update allowed values in the baseline only after careful review.
- Log rotation events in your audit DB (`gaia.db`) as part of the rotation runbook.

## Security notes
- Avoid giving long-lived wide-scope tokens to CI when the built-in `GITHUB_TOKEN` provided to Actions is sufficient.
- For org-level automation, prefer a GitHub App with narrowly scoped permissions.

***

If you want, I can add a short example workflow that demonstrates swapping between two secrets during rotation.
