# External Secrets (Option A)

This document explains how to keep secrets outside the repository and how
the project loads them.

Summary
- Place an external env file outside the repo, for example: `E:\Workspaces\Git\.secret\.env`.
- Set `PRIVATE_ENV_PATH` in your shell or system environment to point to that file.
- The project loader (`scripts/env_loader.py` and `scripts/env_utils.py`) will prefer `PRIVATE_ENV_PATH` if present.

Quick steps
1. Create the external file (example path used by this repo):

   E:\Workspaces\Git\.secret\.env

2. Populate with the required keys (do not paste tokens into chat):

   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   AUTOMATION_GITHUB_TOKEN=...

3. Point your shell to the path for the current session:

   PowerShell:

   $env:PRIVATE_ENV_PATH = 'E:\Workspaces\Git\.secret\.env'

   Or set a persistent user environment variable if you prefer.

CI / GitHub Actions
- In CI you should not use `PRIVATE_ENV_PATH` — instead add required values to repository or environment secrets and the `scripts/check_secrets_ci.py` helper can validate they are present.

Example GitHub Actions snippet (set secrets in repo settings):

```yaml
jobs:
  check-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate secrets
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          AUTOMATION_GITHUB_TOKEN: ${{ secrets.AUTOMATION_GITHUB_TOKEN }}
        run: python scripts/check_secrets_ci.py
```

Notes
- Option B (encrypted `.private/secrets.enc` + key) remains available and is recommended for long-term use.
- Keep external env files out of source control; add them to your OS-level backups and restrict filesystem permissions.
