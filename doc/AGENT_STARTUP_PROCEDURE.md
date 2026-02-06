**Agent Startup Check**

**Purpose:** Validate required runtime tokens on agent startup and surface impediments early.

- **What it does:** Runs `scripts/agent_startup_check.py` at agent start. The script:
  - Reads required token names from `STARTUP_REQUIRED_TOKENS` env var (comma-separated). Defaults to `TELEGRAM_BOT_TOKEN,AUTOMATION_GITHUB_TOKEN`.
  - Uses the repository `SecretsManager` to load tokens (prefers `environment` and `encrypted_file`).
  - Performs lightweight API checks for Telegram (`getMe`) and GitHub (`/user`) with short timeouts.
  - Writes audits via `orchestrator.write_audit()` using actor `agent_startup`.
  - Writes a local status file at `.private/startup_check.json` with results.
  - Exits `0` if all required tokens validated; `1` if any failed; `2` on unexpected errors.

- **How to wire into agent start:** invoke the script early in your agent entrypoint, e.g. in `orchestrator` bootstrap or agent `__main__`:

```bash
python scripts/agent_startup_check.py || exit 1
```

- **Operator guidance:** If the startup check raises an impediment, inspect `.private/startup_check.json` and the orchestrator audit table for details. Typical remediation steps:
  1. Ensure required token(s) are present in the encrypted store (`scripts/secrets_cli.py set KEY -`).
  2. If using the external fallback, restore via `scripts/restore_external_env.py --force` (not recommended for production).
  3. Re-run the startup check.

**Notes:** This check is intentionally conservative: it validates only tokens declared in `STARTUP_REQUIRED_TOKENS` to avoid unnecessary external calls on startup.
