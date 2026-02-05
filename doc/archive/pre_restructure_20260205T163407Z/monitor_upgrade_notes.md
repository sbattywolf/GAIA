# Monitor & Upgrade Notes

Created: 2026-02-05

Purpose: capture runtime errors, observations and a slow/safe upgrade plan for the approval listener and resource monitor.

Current status
- Approval listener: started (PID -> `.tmp/approval_listener2_pid.txt`). Initial start failed due to missing `TELEGRAM_BOT_TOKEN`; restarted after loading `.private/.env`.
- Resource monitor: created `scripts/resource_monitor.py` and started (PID -> `.tmp/resource_monitor_pid.txt`). It logs to `.tmp/resource_monitor.log` and errors to `.tmp/resource_monitor.err`.

Where to find logs
- Approval listener stdout/stderr: `.tmp/approval_listener2.out`, `.tmp/approval_listener2.err`
- Runner logs: `.tmp/automation_runner.out`, `.tmp/automation_runner.err`
- Resource monitor logs: `.tmp/resource_monitor.log`, `.tmp/resource_monitor.err`
- Short one-line events: `.tmp/last_messages.log`
- Audit events: `events.ndjson`

Initial errors & learning
- Approval listener first start printed `ERROR: TELEGRAM_BOT_TOKEN env required` because background Start-Process did not inherit env vars. Fixed by loading `.private/.env` into the PowerShell session before launching.
- Resource monitor requires `psutil`. If missing, the script writes the import failure to `.tmp/resource_monitor.err`. Install via `pip install psutil`.

Next steps (safe upgrade plan)
1. Confirm Telegram approval flow: ask operator to reply `approve` to the test Telegram message; verify approval is recorded in `events.ndjson`.
2. Harden environment loading: create small launcher script that loads `.private/.env` for all scheduled services to avoid manual env propagation.
3. enable lightweight supervisor (restart on crash) and ensure each service writes a `<service>_pid.txt` in `.tmp`.
4. Gradual upgrades: roll out changes to the listener/monitor on a staging machine for 24-48 hours with notifications enabled and manual approvals.
5. After stable runs, integrate persistent audit writes into `gaia.db` for long-term tracing.

If you want, I can start step 1 now and wait for your Telegram approval to validate the end-to-end flow.
