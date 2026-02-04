# EPC_Telegram — All TODOs grouped by feature

Generated: 2026-02-04T08:20:00Z

Summary: consolidated list of all todo tasks found in `doc/EPC_Telegram.current`, grouped by feature and ordered by feature priority (high feature_score first). Total tasks found: 41

Order: features sorted by feature_score (highest → lowest).

---

## 1) F-helper-gise-part2 (feature_score: 34)
- t41 — Run alby_agent prototype in dry-run then execute archive+validate+tests — priority: high — status: todo
- t42 — Iterate heuristics and update epic report estimates — priority: medium — status: todo

### STR_TestGise.part1 (under helper-gise-part2)
- t1 — Initial smoke test: verify agent environment and connectivity — priority: medium — status: todo
- g1 — Verify agent can read .tmp/telegram.env and secrets (dry-run) — priority: high — status: todo
- gd1 — Add verbose logging around claim acquisition for debug — priority: medium — status: todo
- gd2 — Add small helper to export chat history to .tmp/exports — priority: medium — status: todo

### STR_TestGise.part2 (under helper-gise-part2)
- t2 — Run acceptance scenario: create claim → approve → archive event — priority: high — status: todo
- d1 — Add regression case: claim takeover when TTL expired — priority: high — status: todo
- d2 — Document expected chat-history lookup steps for audit — priority: medium — status: todo
- g2 — Run a full acceptance flow and record timestamps in gaia.db — priority: high — status: todo
- t_final — MANDATORY: Check history of the chat and all docs; record findings and close story — priority: critical — status: todo

---

## 2) F-helper-gise-part1 (feature_score: 21)
- t38 — Scan repository for ALby 0.3 documentation and examples — priority: high — status: todo
- t39 — Design small local agent using ALby patterns to automate merges/archives/validation/tests — priority: high — status: todo
- t40 — Scaffold scripts/alby_agent.py to run version_docs.py, validate_todolists.py, archive drafts, and run targeted tests — priority: high — status: todo

---

## 3) Features with feature_score: 13 (grouped)

### F-security-token
- t11 — Document recommended file permissions and storage for .tmp/telegram.env — priority: medium — status: todo
- t12 — Create .env.template and usage guidance — priority: medium — status: todo
- t13 — Add scripts/rotate_admin_token.py scaffold and CLI — priority: high — status: todo

### F-command-safety
- t14 — Enforce ALLOW_COMMAND_EXECUTION=0 by default — priority: high — status: todo
- t15 — Add UI confirmation modal and explicit approval step for destructive commands — priority: high — status: todo
- t16 — Add safe-quoting helpers and tests for tg_command_manager.py — priority: medium — status: todo

### F-integration-tests
- t17 — Implement mocked Telegram API harness for CI/local tests — priority: high — status: todo
- t18 — Add integration test exercising approval listener→UI→approve→claim_cli flow — priority: high — status: todo
- t19 — Add idempotency replay assertions for integration tests — priority: high — status: todo

### F-ttl-requeue-policy
- t20 — Finalize CLAIM_DEFAULT_TTL proposal and document tradeoffs — priority: medium — status: todo
- t21 — Add CLAIM_DEFAULT_TTL env var and update scripts/claims.py — priority: medium — status: todo
- t22 — Add automated tests for TTL expiry and takeover semantics — priority: high — status: todo

### F-retryer
- t23 — Map HTTP error codes for retryer (5xx/429/4xx) and tests — priority: high — status: todo
- t24 — Implement exponential backoff with jitter in retryer — priority: high — status: todo
- t25 — Add tests simulating 429 and 5xx responses — priority: high — status: todo

### F-permanent-failed-ui
- t29 — Add monitor page to list permanent-failed entries — priority: medium — status: todo
- t30 — Implement one-click requeue action with token protection — priority: high — status: todo
- t31 — Record audit traces for UI-initiated requeues and confirmation modal — priority: medium — status: todo

---

## 4) Features with feature_score: 8

### F-metrics-alerts
- t26 — Add counters and persist metrics to .tmp/metrics.json — priority: medium — status: todo
- t27 — Emit gaia.db traces when thresholds crossed — priority: medium — status: todo
- t28 — Wire scripts/alert_on_metrics.py to read metrics and notify admin chat — priority: medium — status: todo

### F-backup-retention
- t32 — Implement scripts/backup_tmp.py to create timestamped archives — priority: medium — status: todo
- t33 — Add retention policy config and scripts/cleanup_backups.py — priority: medium — status: todo
- t34 — Document backup cadence and include backup in release checklist — priority: low — status: todo

---

## 5) Features with feature_score: 3

### F-runbook-docs
- t35 — Populate CLI examples in doc/STR_Telegram.current#CLI-Examples — priority: low — status: todo
- t36 — Add example workflows (manual requeue, safe dry-run) to docs — priority: low — status: todo
- t37 — Add release checklist & CI badge guidance to runbook — priority: low — status: todo

---

## Totals
- Features: 14
- Total tasks: 41

If you'd like a CSV export or a flattened global priority list next, tell me which format you prefer.

---

Source: `doc/EPC_Telegram.current`

---

## Flattened prioritized task list (global order)
Listing all tasks ordered by priority (critical → high → medium → low). Use this as the execution queue.

1. t_final — MANDATORY: Check history of the chat and all docs; record findings and close story — priority: critical — STR_TestGise.part2 (feature: F-helper-gise-part2)

High-priority tasks:
2. t13 — Add `scripts/rotate_admin_token.py` scaffold and CLI — priority: high — F-security-token
3. t14 — Enforce `ALLOW_COMMAND_EXECUTION=0` by default — priority: high — F-command-safety
4. t15 — Add UI confirmation modal and explicit approval step for destructive commands — priority: high — F-command-safety
5. t17 — Implement mocked Telegram API harness for CI/local tests — priority: high — F-integration-tests
6. t18 — Add integration test exercising approval listener→UI→approve→claim_cli flow — priority: high — F-integration-tests
7. t19 — Add idempotency replay assertions for integration tests — priority: high — F-integration-tests
8. t22 — Add automated tests for TTL expiry and takeover semantics — priority: high — F-ttl-requeue-policy
9. t23 — Map HTTP error codes for retryer (5xx/429/4xx) and tests — priority: high — F-retryer
10. t24 — Implement exponential backoff with jitter in retryer — priority: high — F-retryer
11. t25 — Add tests simulating 429 and 5xx responses — priority: high — F-retryer
12. t30 — Implement one-click requeue action with token protection — priority: high — F-permanent-failed-ui
13. t38 — Scan repository for ALby 0.3 documentation and examples — priority: high — F-helper-gise-part1
14. t39 — Design small local agent using ALby patterns to automate merges/archives/validation/tests — priority: high — F-helper-gise-part1
15. t40 — Scaffold `scripts/alby_agent.py` to run `version_docs.py`, `validate_todolists.py`, archive drafts, and run targeted tests — priority: high — F-helper-gise-part1
16. t41 — Run alby_agent prototype in dry-run then execute archive+validate+tests — priority: high — F-helper-gise-part2
17. g1 — Verify agent can read `.tmp/telegram.env` and secrets (dry-run) — priority: high — STR_TestGise.part1
18. g2 — Run a full acceptance flow and record timestamps in `gaia.db` — priority: high — STR_TestGise.part2
19. t2 — Run acceptance scenario: create claim → approve → archive event — priority: high — STR_TestGise.part2
20. d1 — Add regression case: claim takeover when TTL expired — priority: high — STR_TestGise.part2

Medium-priority tasks:
21. t11 — Document recommended file permissions and storage for `.tmp/telegram.env` — priority: medium — F-security-token
22. t12 — Create `.env.template` and usage guidance — priority: medium — F-security-token
23. t16 — Add safe-quoting helpers and tests for `tg_command_manager.py` — priority: medium — F-command-safety
24. t20 — Finalize `CLAIM_DEFAULT_TTL` proposal and document tradeoffs — priority: medium — F-ttl-requeue-policy
25. t21 — Add `CLAIM_DEFAULT_TTL` env var and update `scripts/claims.py` — priority: medium — F-ttl-requeue-policy
26. t26 — Add counters and persist metrics to `.tmp/metrics.json` — priority: medium — F-metrics-alerts
27. t27 — Emit `gaia.db` traces when thresholds crossed — priority: medium — F-metrics-alerts
28. t28 — Wire `scripts/alert_on_metrics.py` to read metrics and notify admin chat — priority: medium — F-metrics-alerts
29. t29 — Add monitor page to list permanent-failed entries — priority: medium — F-permanent-failed-ui
30. t31 — Record audit traces for UI-initiated requeues and confirmation modal — priority: medium — F-permanent-failed-ui
31. t32 — Implement `scripts/backup_tmp.py` to create timestamped archives — priority: medium — F-backup-retention
32. t33 — Add retention policy config and `scripts/cleanup_backups.py` — priority: medium — F-backup-retention
33. t1 — Initial smoke test: verify agent environment and connectivity — priority: medium — STR_TestGise.part1
34. gd1 — Add verbose logging around claim acquisition for debug — priority: medium — STR_TestGise.part1
35. gd2 — Add small helper to export chat history to `.tmp/exports` — priority: medium — STR_TestGise.part1
36. d2 — Document expected chat-history lookup steps for audit — priority: medium — STR_TestGise.part2

Low-priority tasks:
37. t34 — Document backup cadence and include backup in release checklist — priority: low — F-backup-retention
38. t35 — Populate CLI examples in `doc/STR_Telegram.current#CLI-Examples` — priority: low — F-runbook-docs
39. t36 — Add example workflows (manual requeue, safe dry-run) to docs — priority: low — F-runbook-docs
40. t37 — Add release checklist & CI badge guidance to runbook — priority: low — F-runbook-docs
41. t42 — Iterate heuristics and update epic report estimates based on prototype results — priority: medium/low — F-helper-gise-part2

---

Execution note: follow the numbered list above (1→41). I will work autonomously on these in order, send Telegram summaries every 5 minutes, and continue until you ask me to stop or 8 hours elapse.
