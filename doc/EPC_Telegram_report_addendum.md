# EPC_Telegram — Report Addendum: Reorder & Human Summaries

Date: 2026-02-04

This addendum documents the feature reorder and human-readable summaries introduced during the recent backlog work (branch `feat/merge-STR_TestGise-candidates`). It complements `doc/EPC_Telegram_Report.md` and `doc/EPC_Telegram.current`.

Summary of changes

- Total features (post-split): 10
- Total stories (post-split): 10

Reordered feature list (priority to agent/infra work)

1. F-helper-gise-part1 — Helper Gise: Foundation
   - Summary: Design and scaffold core agent functionality: repository scanning, architecture/design, and a safe scaffold for `scripts/alby_agent.py`.
   - Stories:
     - `stoy_alby_scan`: locate ALby references and examples to inform design.
       - t38: Scan repo for ALby 0.3 documentation and examples — locate examples and note patterns.
     - `stoy_alby_design`: design agent architecture and component list.
       - t39: Design small local agent using ALby patterns — produce a brief design doc.
     - `stoy_alby_scaffold`: scaffold CLI and safe dry-run behaviors.
       - t40: Scaffold `scripts/alby_agent.py` — implement `--dry-run`, archive/validate hooks.

2. F-helper-gise-part2 — Helper Gise: Prototype & Acceptance
   - Summary: Prototype runs and the STR_TestGise acceptance flow; collect timing signals and iterate heuristics.
   - Stories:
     - `stoy_alby_prototype`: run dry-runs and live archive/validate cycles.
       - t41: Run `alby_agent` prototype in dry-run then archive+validate+tests.
     - `stoy_alby_iterate`: measurement and iteration on heuristics.
       - t42: Iterate heuristics and update epic estimates.
     - `STR_TestGise.part1`: environment checks and helpers (t1,g1,gd1,gd2).
     - `STR_TestGise.part2`: acceptance tests and governance (t2,d1,d2,g2,t_final).

3. F-security-token — Security & token rotation
   - Summary: ensure secure handling of `.tmp/telegram.env`, rotate admin tokens, and document recommended storage.

4. F-command-safety — Command execution safety
   - Summary: guardrails around command execution, `ALLOW_COMMAND_EXECUTION` default, and UI confirmation flows.

5. F-integration-tests — Integration tests
   - Summary: mocked Telegram harness and e2e tests for approve→claim→requeue flows.

6. F-ttl-requeue-policy — Claim TTL & Requeue Policy
   - Summary: finalize TTL defaults, env configuration, and tests for takeover semantics.

7. F-retryer — Retryer error classification
   - Summary: classify retry behavior for HTTP errors and implement backoff/jitter + tests.

8. F-metrics-alerts — Metrics & alerts
   - Summary: metrics collection, persistence, and alert wiring for threshold breaches.

9. F-permanent-failed-ui — Permanent-failed UI & requeue
   - Summary: UI for listing and requeueing permanent-failed entries with audit traces.

10. F-backup-retention — Backup & retention
    - Summary: timestamped archives for `.tmp` and `gaia.db`, and cleanup/retention rules.

Notes on traceability

- The canonical backlog (`doc/EPC_Telegram.current`) now contains per-feature and per-story `summary` fields and per-task `summary` where available.
- For the split operations we added `moved_from` and `moved_at` metadata to tasks moved from `STR_TestGise` into `STR_TestGise.part1` and `STR_TestGise.part2`.
- Detailed per-feature/story/task human-readable summaries are available in this addendum and in `doc/EPC_Telegram.current`.

Next steps

- Use these summaries for PR descriptions and review guidance.
- If you'd like, I can push the changes and open the PR, or continue to split additional features as flagged by scoring.
