**STR_TODO_stoybl_bl_bl_1_runbook**

Purpose
- Capture operator-facing runbook snippets for claiming, approving, requeue, token handling, and incident recovery.

Runbook snippets
- Claim inspection:
  - `python scripts/claim_cli.py inspect --id <claim_id>`
- Claim a pending command for review (dry-run):
  - `python scripts/claim_cli.py claim --id <claim_id> --ttl 300 --dry-run`
- Approve a claimed command (exec guarded by `ALLOW_COMMAND_EXECUTION`):
  - `python scripts/claim_cli.py approve --id <claim_id> --token $MONITOR_ADMIN_TOKEN`
- Manual requeue (admin):
  - `python scripts/telegram_queue_admin.py --requeue --id <message_id> --reason 'operator requeue'`

Incident recovery
- If a claim appears stuck, check `gaia.db` traces for `claim.acquired` and `claim.refreshed` timestamps.
- For stuck items older than TTL, an admin may takeover by using `claim_cli.py takeover --id <claim_id> --token $MONITOR_ADMIN_TOKEN` (audit trace recorded).

Operator checklist before approve
- Inspect the command payload and scope the side-effects.
- Confirm idempotency of the action or prepare a compensating step.
- Ensure `ALLOW_COMMAND_EXECUTION` is enabled only in controlled sessions and recorded in audit traces.
