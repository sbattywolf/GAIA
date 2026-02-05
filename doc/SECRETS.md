# Secrets and Identifiers — GAIA

This guide explains which secrets the repository needs for Telegram integration and how to obtain them safely.

Required items

- `TELEGRAM_BOT_TOKEN` — token for your Telegram bot created via BotFather.
- `TELEGRAM_CHAT_ID` — numeric chat id where messages will be sent (user or group).

Quick collection steps

1) Create a Telegram bot and get its token

- In Telegram, open a chat with `@BotFather`.
- Run `/newbot` and follow prompts to set a bot name and username.
- BotFather returns a token that looks like `123456789:AAE...` — store this value.

2) Get your chat id

Option A — personal id
- In Telegram open `@userinfobot` and send `/start` — it replies with your numeric id.

Option B — group id
- Add your bot to a group and send a message in the group.
- Poll updates with the bot token: `curl -s "https://api.telegram.org/bot<token>/getUpdates" | jq .` and inspect `message.chat.id`.

Storing secrets locally

- Preferred local file: `.private/.env` (not checked into git). Put:

  TELEGRAM_BOT_TOKEN=...
  TELEGRAM_CHAT_ID=...

- Alternative: `.tmp/telegram.env` for temporary testing.

Storing secrets in GitHub

- Use environment-scoped secrets for the `production` environment (we added `scripts/gh_setup_env.sh` and `scripts/gh_setup_env.ps1` to help create them).
- The scripts will store `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as environment secrets.

Validating secrets

- Run:

  ```bash
  python scripts/validate_secrets.py
  ```

- The script attempts to read `.private/.env` or `.tmp/telegram.env` and environment variables and reports missing items and guidance.

Security notes

- Never commit secrets into git. Use `.private` and add it to `.gitignore`.
- For CI, use environment-scoped secrets and require manual approvals for workflows that will perform real sends.


---

<!-- Merged from docs/SECRETS.md on 20260205T160615Z UTC -->

# Secrets Scanning

This project uses `detect-secrets` to detect accidental secret commits and prevent regressions.

Quick notes:

- Baseline file: `.secrets.baseline` (committed).
- CI job: `.github/workflows/secret-scan.yml` runs `detect-secrets scan --all-files --json` and fails if the scan finds files not present in the baseline.

To update the baseline locally (only when you have vetted the findings):

```bash
python -m pip install detect-secrets
detect-secrets scan > .secrets.baseline
git add .secrets.baseline && git commit -m "chore: update detect-secrets baseline"
```

If the CI job flags new files, review them carefully; do not add real secrets to the baseline. Instead rotate and remove any leaked credentials.
