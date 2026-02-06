# GitHub App Creation Checklist & Per-Consumer Minimal Scopes
Purpose: safely create a GitHub App for GAIA automation, obtain installation tokens, and assign minimal permissions per consumer.

1) Decision
- Prefer GitHub App (recommended): short-lived installation tokens, repo-scoped installs, fine-grained permissions.

2) Create the App (owner / org admin)
- In GitHub: Settings → Developer settings → GitHub Apps → New GitHub App.
- Fill: name `GAIA-Automation`, description, webhook (optional for events), callback (not required for scripts).
- Generate and download the private key (PEM). Save to `.private/gaia_app.pem` in operator machine (never commit).
- Record `APP_ID` (App settings) and `INSTALLATION_ID` (after installing to repo/org).

3) Install the App
- Install into target repo(s) only — avoid org-wide install unless necessary.
- Note the installation ID for each repo (use GitHub API or UI to find it).

4) Minimal permissions (per consumer)
- CI / Build (short-lived tokens used by runner helpers)
  - Permissions: `contents: read`, `checks: read`, `pull_requests: read`.
  - Grants: read-only unless workflows need to push tags or update PRs — then add `contents: write` and `pull_requests: write` as required.

- Publisher / Issue creator (`scripts/publish_issues.py`)
  - Permissions: `issues: write`, `pull_requests: read`, `metadata: read`.

- Token-cache service
  - This service returns installation tokens to local agents. Its installation should be limited to the repo and the App permissions should match the union of needed consumer scopes (e.g., `issues:write`, `contents:read`).

- Agents / Workers (background automation)
  - Assign per-agent least-privilege: `issues:write` for issue tasks, `actions:workflows:write` only if they need to trigger workflows, `contents:read` for read operations.

- Actions workflows using `GITHUB_TOKEN`
  - Prefer using the built-in `GITHUB_TOKEN` for in-repo operations. Replace any use of personal PATs or repo-wide shared tokens with App-based tokens for external automation.

5) Exchange App key for installation token (example)
- Using the repo scripts (after placing PEM at `.private/gaia_app.pem`):

  ```bash
  python scripts/github_app_token.py --app-id <APP_ID> --key-path .private/gaia_app.pem --installation-id <INSTALLATION_ID>
  # prints JSON {"token": "...", "expires_at": "..."}
  ```

6) Persist tokens (operator)
- Persist the installation token into the encrypted store with a canonical name using the helper:

  ```bash
  python scripts/github_app_token.py --app-id <APP_ID> --key-path .private/gaia_app.pem --installation-id <INSTALLATION_ID> --persist --name GAIA_GITHUB_TOKEN
  ```

7) Validate and iterate
- Run `scripts/validate_consumers.py` (smoke tests), test the token-cache (`scripts/token_cache_server.py`), and run a dry-run of `scripts/publish_issues.py`.
- If a consumer fails due to insufficient scopes, increase minimal scope only for that consumer and re-validate.

8) Rotation & safety
- Use the App private key to regularly (e.g., daily/hourly) request fresh installation tokens via `scripts/github_app_token.py` or the token-cache service.
- Record each rotation in `gaia.db` audit and append a `token.fetch` event to `events.ndjson` (the codebase helpers do this automatically).
- Create a `CHECKPOINT` PR before revoking any existing admin PATs.

9) Post-creation checklist for operators
- Store `.private/gaia_app.pem` securely and restrict access.
- Add CI and environment secrets for consumers pointing to the new canonical secret names (e.g., `GAIA_GITHUB_TOKEN`, `GAIA_CI_TOKEN`).
- Revoke any broad-scope PATs after validating consumers.

10) Troubleshooting
- If `scripts/github_app_token.py` fails due to missing libraries, install `PyJWT` and `requests` in the environment.
- For local testing, use `GAIA_TEST_MODE=1` with `GAIA_GITHUB_TOKEN` set to a test token.

If you want, I can now produce a per-repo `permissions.csv` mapping each consumer (from `rotation/inventory.json`) to recommended minimal permissions. Proceed? 
