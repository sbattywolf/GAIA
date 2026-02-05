# Roadmap: Local Monitoring Framework & NAS Migration

Created: 2026-02-05

Goals
- Provide a small, robust monitoring framework to observe local agent processes and resource usage.
- Keep the implementation tiny so it can run on a NAS/minimal host later.
- Add a safe token-rotation plan and recommend creating a dedicated machine user/token for Git operations.

Short-term (this week)
1. Deploy `scripts/monitor_framework.py` (local) to watch key services and send Telegram alerts. Heartbeat every minute.
2. Run resource monitor (`scripts/resource_monitor.py`) on the same host to alert at CPU/MEM >=90%.
3. Harden env-loading: create a launcher that loads `.private/.env` for scheduled services. This avoids missing-token errors.
4. Create a machine GitHub user (or GitHub App) with minimal permissions; store its token in repository secrets (or a password manager). Do NOT hardcode tokens in repo files.

Medium-term (1–2 months)
1. Move the monitor + approval listener to a low-resource NAS box for continuous uptime. Use system service (systemd, or NAS task scheduler) to restart on crash.
2. Add persistent audit writes to `gaia.db` for monitoring events and approval traces.
3. Add repository CI job to validate token and secret access patterns (detect leaked tokens in PRs).

Long-term (token rotation)
1. Implement a token-rotation pilot: a small service that rotates a machine user's token on schedule and updates the secret store.
2. Add automated verification: after rotation, run a smoke task using the new token before revoking the old one.

Security notes
- Use least privilege for machine users. Prefer GitHub Apps for fine-grained permissions.
- Store tokens in secret stores (GitHub secrets, Bitwarden) and use short-lived tokens where possible.

Operational notes
- Logs and pidfiles are kept under `.tmp/` for easy inspection. Make sure the NAS has sufficient disk retention rules.
- When moving to NAS, consider containerizing the monitor to standardize runtime requirements (Python + psutil).
