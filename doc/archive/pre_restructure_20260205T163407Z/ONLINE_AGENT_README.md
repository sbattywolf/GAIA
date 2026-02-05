# Online Agent (minimal)

Purpose

Provide a minimal, free online agent using GitHub Actions that can be manually dispatched to perform a tiny set of remote operations (dry-run, send Telegram message, create GitHub issue). The agent is intentionally small and gated by `PROTOTYPE_USE_LOCAL_EVENTS` and `ALLOW_COMMAND_EXECUTION` flags.

Files added

- `.github/workflows/online-agent.yml` — `workflow_dispatch` workflow that runs `scripts/online_agent.py`.
- `scripts/online_agent.py` — minimal runner supporting `dry_run`, `send_telegram`, and `create_issue`.

Usage

1) Configure secrets (recommended: store in a protected `production` environment):

- `TELEGRAM_BOT_TOKEN` — bot token for Telegram sends.
- `TELEGRAM_CHAT_ID` — chat id to send to.
- `GITHUB_TOKEN` — available automatically in Actions; ensure it has `issues:write` if needed.
- `PROTOTYPE_USE_LOCAL_EVENTS` — set to `1` (default) to avoid real actions. Set to `0` to allow execution (use with caution).
- `ALLOW_COMMAND_EXECUTION` — set to `1` to permit execution when `PROTOTYPE_USE_LOCAL_EVENTS` is disabled.

2) Run from the GitHub UI: Actions → Online Agent → Run workflow → fill inputs.

3) Or via `gh` CLI:

```bash
gh workflow run online-agent.yml -f command=dry_run
gh workflow run online-agent.yml -f command=send_telegram -f body="Hello from GAIA"
gh workflow run online-agent.yml -f command=create_issue -f title="New issue" -f body="Created by online agent"
```

Notes

- The agent appends events to `events.ndjson` and writes a short audit (SQLite) row to `gaia.db` for traceability.
- This workflow is manual by design — later we can bridge Telegram→GH to trigger this workflow on chat commands.

Safety

- Keep `PROTOTYPE_USE_LOCAL_EVENTS=1` to avoid external side effects while testing.
- Use GitHub Environment protections (required reviewers) for `TELEGRAM_BOT_TOKEN` before enabling real sends.
