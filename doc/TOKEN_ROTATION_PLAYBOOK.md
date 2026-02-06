# Token Rotation Playbook — automated-safe approach

Overview
- Creating Personal Access Tokens (PATs) via API is not supported for GitHub.com for security reasons. Recommended automation pattern: use a GitHub App to provide short-lived installation tokens programmatically.

Options
- Manual PATs (existing): create fine-grained tokens in the web UI and store them in `SecretsManager` (works but manual).
- Recommended: GitHub App
  - Create a GitHub App (one-time manual step). Assign minimal permissions per-role (issues, contents, actions, etc.).
  - Install the App on the target organization/repo to obtain an installation ID.
  - Use the App private key to create a JWT and exchange it for an installation access token (short-lived). The `scripts/github_app_token.py` helper automates this exchange and can persist the token to the encrypted store.

Why GitHub App?
- Installation tokens are short-lived (recommended for automation).
- App permissions are fine-grained and scoped to the exact resources.
- Tokens can be generated programmatically without storing long-lived PATs.

One-time manual steps (operator)
1. Create a GitHub App in your organization account: https://github.com/settings/apps
2. Record the `App ID`, download the private key (PEM), and install the App into the repositories (note the installation ID shown during install).

Automated sequence (agent/job)
1. Agent runs `scripts/github_app_token.py --app-id <APP_ID> --key-path .private/app.pem --installation-id <INSTALL_ID> --persist` to obtain and persist an installation token.
2. Agent stores the token in the encrypted secrets store as `GAIA_GITHUB_TOKEN` (mirrored to `AUTOMATION_GITHUB_TOKEN` by `SecretsManager`).
3. Agent updates repo/CI secrets and restarts jobs that need access.

Fallback: If a GitHub App cannot be created, the operator must create fine-grained PATs manually and use `scripts/rotate_tokens_helper.py` to persist them.

Security notes
- Keep the GitHub App private key in a secure place (the repo `.private` folder is acceptable during rotation if encrypted and audited).
- Revoke old tokens after validating consumers.
- Record all actions in `gaia.db` audit and `events.ndjson` (existing agent patterns).
