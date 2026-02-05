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


---

<!-- Merged from docs/SECRETS_HANDLING.md on 20260205T160615Z UTC -->

# Secrets Handling and Safe Storage

Goal: avoid losing secrets while keeping them secure and recoverable when you "switch on" a development environment.

Recommended approaches (ordered by security + convenience):

1) GitHub Secrets & Environments (recommended)
   - Store runtime secrets in GitHub: `Settings → Secrets` (repository or Environment-level).
   - Use `scripts/set_repo_secrets.ps1` to automate setting secrets with `gh secret set`.
   - CI and Actions will read secrets from `secrets.*` automatically; never commit raw values.

2) Encrypted secrets in-repo (auditable, safe to commit)
   - Use `sops` (Mozilla SOPS) with a KMS or `age` key to encrypt YAML/JSON files and commit the ciphertext to the repo.
   - Only the people/CI with the key can decrypt; great for infra/ops secrets that must be versioned.

3) Local-only secrets (developer convenience)
   - Keep an untracked `.env` file locally (we provide `.env.template` in repo).
   - Add `.env` to `.gitignore` to prevent accidental commits.

Local workflows we added to this repo
- `scripts/set_repo_secrets.ps1` — helper to set GitHub repo secrets via `gh` (already present).
- `scripts/load_env.ps1` — convenience helper to populate a local `.env` from environment variables or a protected store.
- `.secrets.baseline` + `docs/SECRETS.md` + `secret-scan.yml` — detect-secrets baseline and CI job to catch accidental secrets.

Quick setup (recommended):

1. Store production secrets in GitHub Secrets / Environments.
2. For developer-local secrets, copy the template:

```powershell
copy .env.template .env
# edit .env locally with your values
```

3. Prevent accidental commits: run `pre-commit install` (we added a `pre-commit` config to run `detect-secrets`).

If you want to keep encrypted secrets in the repo (SOPS):

1. Encrypt a file:

```bash
sops --encrypt --age <age-key> secrets.yaml > secrets.yaml.enc
git add secrets.yaml.enc
```

2. In CI, decrypt with the key made available to the runner.

If you'd like, I can implement a SOPS workflow or enable `git-crypt` for the repository — tell me which you prefer.
