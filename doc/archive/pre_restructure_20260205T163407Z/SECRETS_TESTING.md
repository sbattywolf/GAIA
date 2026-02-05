## Secrets Testing & Unhappy-Path Strategy

Purpose
- Provide a simple, local-first pattern for storing and exercising secrets during development and for intentionally testing failure modes (invalid token, revoked token, wrong chat id).

Principles
- Do not commit real secrets. Use templates and `.env` for local tests.
- Keep runtime secrets out of the repository in production; for local testing use `.env` or Bitwarden via `scripts/secret_helper.py`.
- Provide a reproducible folder with example (templated) credentials to simulate unhappy scenarios.

Recommended layout (local only)
- `.env` — Primary local developer secrets (gitignored). Example keys: `TELEGRAM_BOT_TOKEN`, `CHAT_ID`, `TELEGRAM_NOTIFY_CHAT`.
- `.tmp/test_secrets/invalid_tokens.env.template` — Template file containing placeholder invalid tokens to exercise failure cases.

How to use

1. Create a test env copy

```powershell
copy .tmp\test_secrets\invalid_tokens.env.template .tmp\test_secrets\invalid_tokens.env
```

2. Edit the copied file to select a scenario:
- `INVALID_TOKEN=1` — use clearly invalid bot token
- `REVOKED_TOKEN=1` — simulate revoked credential
- `WRONG_CHAT=1` — set `CHAT_ID` to a value that the bot cannot post to

3. Load test secrets before starting a script (PowerShell example):

```powershell
$env:PYTHONPATH='.';
Get-Content .tmp\test_secrets\invalid_tokens.env | ForEach-Object { $p = $_ -split '='; if($p.Length -eq 2) { $env[$p[0]] = $p[1] } }
python scripts/approval_listener.py --poll 5
```

Unhappy scenarios to test
- Invalid token: ensures the process fails gracefully and logs an explicit error.
- Revoked token / permission denied: ensure retries/backoff and safe failure (no silent infinite retry).
- Wrong chat id: confirm error handling when send_message calls fail for target chat.
- Network outages: confirm queue persistence and resume behavior.

Logging & Observability
- Ensure `events.ndjson` contains `telegram.*` failure events for each unhappy scenario.
- Use `gaia.db` `command_audit` table to verify audit records are not recorded for failed executions.

Automated test note
- You can build small integration scripts that load each template and assert expected events/audit rows are written. Keep those scripts local-only and excluded from commits.

Test harness
- A small harness lives at `scripts/test_harness.py`. It can load `.tmp/test_secrets/invalid_tokens.env` and exercise unhappy-path scenarios (e.g., `invalid_token`). Use it to validate that failures are logged to `events.ndjson` and no audit rows are created for failed operations.
