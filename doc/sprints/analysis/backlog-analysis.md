# Backlog Analysis — Sprint Intake

Generated: 2026-02-05

Summary
- Total open issues captured: 39
- Critical-labeled issues detected: 0 (exact matches on label name)
- High-labeled issues detected: 0 (exact matches on label name)
- Issues labeled `ci`: 0
- Issues labeled `testing`: 0

Notes
- The counts above are a conservative substring match on label JSON; label names may vary or use synonyms. See `backlog-issues.ndjson` for full issue details (one JSON object per line).

Top priorities observed (manual inspection required)
- Security / token purge (issue #68) — critical by intent; please confirm label applied.
- Detect-secrets + pre-commit (issue #69) — high priority to prevent further leaks.
- CI basetemp + TTY guards (issues #64, #66) — quick fixes with high ROI to reduce CI noise.
- Mocked Telegram harness (issue #67) — required to stabilize integration tests.

Files produced
- `doc/sprints/analysis/backlog-issues.ndjson` — machine-readable list of open issues (one JSON object per line).
- `doc/sprints/analysis/workflow-runs.ndjson` — recent workflow run records (one JSON object per line).
- `doc/sprints/analysis/summary_counts.txt` — simple counts used for this summary.

Recommended next actions
1. Confirm label normalization: ensure `critical`, `high`, `ci`, `testing` labels exist and are consistently applied. I created several labels earlier; please review.
2. Run CI with the two PRs open (PR #71, PR #72) to validate basetemp + TTY fixes reduce noise.
3. Triage the 39 open issues by priority and attach estimates/assignees for Sprint planning.
4. I can proceed to automatically create a prioritized CSV/NDJSON of issues with suggested assignment and estimated effort if you want.

Raw counts (see `summary_counts.txt`):

```
"$(Get-Content doc/sprints/analysis/summary_counts.txt -Raw)"
```

If this looks good I will: 1) normalize labels on all open issues, 2) produce a CSV/NDJSON with priority/epic mapping and suggested sprint slot, and 3) begin scheduling lower-priority items into Sprints 2–4.
