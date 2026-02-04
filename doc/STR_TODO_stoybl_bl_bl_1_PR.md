# STR: stoybl_bl_bl_1 — PR-ready summary

Overview
- Short key: `stoybl_bl_bl_1`
- Purpose: integrate durable claim primitives into operator flows and deliver safe, auditable approval UI/CLI with test coverage and runbook updates.

Sub-stories (detailed docs)
- Claims integration: [doc/STR_TODO_stoybl_bl_bl_1_claims.md](doc/STR_TODO_stoybl_bl_bl_1_claims.md)
- Tests: [doc/STR_TODO_stoybl_bl_bl_1_tests.md](doc/STR_TODO_stoybl_bl_bl_1_tests.md)
- Runbook: [doc/STR_TODO_stoybl_bl_bl_1_runbook.md](doc/STR_TODO_stoybl_bl_bl_1_runbook.md)
- CLI / UI: [doc/STR_TODO_stoybl_bl_bl_1_cli_ui.md](doc/STR_TODO_stoybl_bl_bl_1_cli_ui.md)
- Classification: [doc/STR_TODO_stoybl_bl_bl_1_classification.md](doc/STR_TODO_stoybl_bl_bl_1_classification.md)
- Part2 plan: [doc/STR_TODO_stoybl_bl_bl_1_part2.md](doc/STR_TODO_stoybl_bl_bl_1_part2.md)
- Governance: [doc/STR_TODO_stoybl_bl_bl_1_governance.md](doc/STR_TODO_stoybl_bl_bl_1_governance.md)

Quick operator commands (examples)
- Inspect an item (JSON):
```
python scripts/claim_cli.py inspect --id <claim_id> --json
```
- Claim (dry-run):
```
python scripts/claim_cli.py claim --id <claim_id> --ttl 300 --dry-run
```
- Approve (server forwards token):
```
python scripts/claim_cli.py approve --id <claim_id> --token $MONITOR_ADMIN_TOKEN
```
- Manual requeue:
```
python scripts/telegram_queue_admin.py --requeue --id <message_id> --reason 'operator requeue'
```

Acceptance checklist for PR
- [ ] `scripts/claims.py` is wired into `scripts/claim_cli.py` and monitor server endpoints.
- [ ] Unit and concurrency tests added and passing locally.
- [ ] `doc/HANDOFF.md` updated with runbook snippets and governance note.
- [ ] `gaia.db` audit traces show claim lifecycle events for sample run.

Notes
- Keep `ENABLE_CLAIMS_INTEGRATION` feature-flagged until rollout and metrics validated.
