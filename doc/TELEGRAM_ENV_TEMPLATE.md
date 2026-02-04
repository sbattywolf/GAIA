# Telegram env template and usage

Place a copy of this template at `.tmp/telegram.env` for local runs.

Recommended file contents (`.tmp/telegram.env`):

TELEGRAM_BOT_TOKEN=your_bot_token_here
CHAT_ID=your_admin_chat_id_or_group_id
ALLOW_COMMAND_EXECUTION=0
TELEGRAM_RETRIES=3
TELEGRAM_BACKOFF_MS=500
CLAIM_DEFAULT_TTL=300

# Optional: enable periodic notifications from `scripts/gise_autonomous_runner.py`.
# To enable, place a copy of this template at `.private/telegram.env` and set:
# PERIODIC_NOTIFICATIONS_ENABLED=1
# ALLOW_COMMAND_EXECUTION=1
# When developing or testing locally, prefer `PROTOTYPE_USE_LOCAL_EVENTS=1` to
# simulate sends instead of posting to Telegram.

Security & permissions
- Keep `.tmp/telegram.env` local and out of version control. Add `.tmp/` to `.gitignore` if not already ignored.
- File permissions: on Windows, restrict file to your user account. On Unix: `chmod 600 .tmp/telegram.env`.
- Rotate tokens regularly and store the active token in a secure secret store if available.

Quick helper
- Use `scripts/init_telegram_env.py` to create a starter `.tmp/telegram.env` from this template (if present).

CI / Protected sends checklist
- Create the `production` environment in GitHub (see `doc/GITHUB_ENV_SETUP.md`).
- Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` as environment secrets.
- Configure required reviewers for the `production` environment to approve manual runs.
- Use the `real-send.yml` workflow to dispatch manual, reviewed sends.
