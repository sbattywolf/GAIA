# Telegram setup for periodic summaries

This document shows the exact commands to test the summary locally and store the secrets for the scheduled GitHub Action. Replace `OWNER/REPO` and `ORG` with your repository or organization values.

1) Local test (PowerShell)

```powershell
Set-Location E:\Workspaces\Git\GAIA
# install dependency if needed
python -m pip install --upgrade pip
python -m pip install requests

# set env vars for this session (do NOT commit these)
# prefer GAIA-prefixed names locally for consistency
$env:GAIA_TELEGRAM_CHAT_ID='123456789'
$env:GAIA_TELEGRAM_BOT_TOKEN='your_new_token_here'

# run the summary (prints to stdout and sends Telegram if token+chat present)
python .\scripts\telegram_summary.py
```

2) Add secrets to repository (so Actions can use them)

Use the GitHub CLI from your machine (recommended) or the GitHub UI.

```powershell
# replace OWNER/REPO with your repo path (e.g. sbattywolf/GAIA)
# store GAIA-prefixed secrets for clarity in workflows
gh secret set GAIA_TELEGRAM_BOT_TOKEN --repo OWNER/REPO --body 'your_new_token_here'
gh secret set GAIA_TELEGRAM_CHAT_ID --repo OWNER/REPO --body '123456789'
```

Notes:
- Repo secrets are the simplest and scope the token to this repository only.
- If you prefer an organization secret, run `gh secret set TELEGRAM_BOT_TOKEN --org ORG --body 'token'` and then grant repository access in the GitHub UI.

3) Trigger the workflow immediately (optional)

```powershell
# trigger the workflow on the default branch (e.g. main)
gh workflow run notify-telegram-summary.yml --repo OWNER/REPO --ref main

# list recent runs and get the run id
gh run list --workflow notify-telegram-summary.yml --repo OWNER/REPO

# view logs
gh run view <run-id> --log --repo OWNER/REPO
```

4) Quick verification checklist

- Local test printed the summary or you received a Telegram message.
- `gh secret list --repo OWNER/REPO` shows the two secrets.
-- The scheduled Action runs every 30 minutes; check Actions → `Notify - Telegram summary` for recent runs.

5) Security notes

- Never commit tokens to the repo. If a token was committed, rotate it and scrub history.
- Keep secrets in GitHub Secrets (or your secret manager) and prefer short-lived tokens when possible.

If you want, I can add a small `Makefile` or PowerShell helper to automate the `gh secret set` calls for your `OWNER/REPO` — tell me the repo slug and I will add it.
