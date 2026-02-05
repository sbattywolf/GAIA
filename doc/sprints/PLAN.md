Part 3 — Stabilize & Verify Auto‑Triage
=====================================

Goal
- Stabilize the auto‑triage automation and verify it works reliably for production usage. Focus on monitoring, small improvements, documentation, and closing the loop with stakeholders.

Scope (4 steps)
1. Monitor (7 days)
   - Run automated triage daily; collect metrics: runs, success/failures, gist upload success, empty-log hits, auth errors.
   - Log metrics into `doc/sprints/analysis/metrics/triage-metrics.ndjson` (simple NDJSON per run).
2. Document
   - Add runbook note in `README_RUNBOOK.md` describing how triage runs, tokens used, and recovery steps.
   - Add `doc/sprints/backlog_item_template.md` for consistent issue/backlog creation.
3. Small fixes & regression checks
   - Add a small CI smoke that validates `gh auth` tolerant behavior and `pytest --basetemp` invocation (non‑TTY guard test).
   - Script to reconstruct run→gist→issue mapping by scanning follow-up issues and extracting gist links (optional automation script under `scripts/`).
4. Close-out
   - Produce a retro note summarizing metrics, incidents, and decisions.
   - Tag final artifacts, move release from draft to published if approved, and archive logs.

Acceptance criteria
- No more than 5% triage runs fail for auth or gist upload reasons during the monitoring window (or acceptable threshold agreed by team).
- Documentation updated (runbook + backlog template) and accessible from README.
- Small regression check exists in CI and passes on `master`.

Owner & timeline
- Owner: TBD (suggest: `@sbattywolf` or whoever owns triage automation)
- Timeline: 7 days monitoring + 2 days for follow-up fixes and retro (total 9 days recommended)

Artifacts produced
- `doc/sprints/analysis/triage-metrics.ndjson`
- `doc/sprints/backlog_item_template.md`
- `README_RUNBOOK.md` addition (runbook section)
- Optional: `scripts/reconstruct_gist_mapping.py`

Next step
- Create the `doc/sprints/backlog_item_template.md` and a PR for the `PLAN.md` if you want review before merging.
