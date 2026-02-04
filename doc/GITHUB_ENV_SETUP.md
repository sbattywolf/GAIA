# GitHub Environment: `production` setup

This document explains how to configure the `production` environment used by
`.github/workflows/real-send.yml` so that manual runs require repository-level
approval before jobs can access secrets and run the send step.

Steps (UI)
1. Open your repository on GitHub and go to `Settings` → `Environments`.
2. Click **New environment** and name it `production`.
3. (Optional) Add one or more required reviewers under **Environment protection rules**:
   - Under **Required reviewers**, add individual users or teams who must approve runs.
   - Save the protection rule.
4. Add repository-level secrets scoped to the environment (these are accessible
   to jobs that run in the environment once approved):
   - `TELEGRAM_BOT_TOKEN` — the bot token
   - `TELEGRAM_CHAT_ID` — the chat id to send messages to

Steps (CLI)
If you prefer the GitHub CLI (installed and authenticated):

```bash
# create environment (UI is recommended; environments cannot be fully created via gh yet)
# add secrets (run from repo root)
gh secret set TELEGRAM_BOT_TOKEN --body "$(cat /path/to/token.txt)" --repo OWNER/REPO
gh secret set TELEGRAM_CHAT_ID --body "123456789" --repo OWNER/REPO
```

Notes & Safety
- The `real-send.yml` workflow is configured to use `environment: production`.
  That causes the job to pause and require approval from the environment's
  required reviewers before steps that reference `secrets` or `environment`
  variables run.
- Keep the number of approvers small and use teams for easier rotation.
- Do not store long-lived secrets in plain repo files — use the environment
  secrets feature or an external secrets manager.

Verification
1. After configuring, open the workflow at `.github/workflows/real-send.yml` in
   the repo and click **Run workflow** → fill inputs and dispatch.
2. The workflow will pause at the environment approval step and show a link to
   request approvals from the configured reviewers.

If you want, I can prepare a small checklist to copy into your repo README with
the exact reviewer names and a suggested rotation schedule.
