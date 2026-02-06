**Roadmap v2 — Updated after 05_02 mini-sprint**

Overview:

- Version: v2 (post-05_02 sprint)
- Focus areas: Security (secrets cleanup), CI stability, Agent/Telegram integration

High-level milestones:

1. Secrets remediation (audit, rotate tokens, history rewrite) — CHECKPOINT process progressed; rotation executed for `AUTOMATION_GITHUB_TOKEN` (backup + audit recorded)
2. CI hardening (pytest basetemp, regression tests, gh auth handling)
3. Agent infra: mocked Telegram (complete), retryer (complete), inbound processing (pending)
4. Release automation: auto-triage archive & run→gist mapping (partial)

Notes:
- Percent complete (approx): 75%
- Remaining work estimated at ~20h across prioritized tasks.

Recent sprint artifacts:
- Canonical merged sprint file: `doc/sprints/05_02_26_merged.md` (contains consolidated Part1..Part4 content).
- Candidate inventory: `doc/sprints/analysis/candidates.ndjson` (~14,579 entries).
- Prioritized CHECKPOINT issues created: #110..#129.
- Automated token rotation executed (non-destructive flow): `AUTOMATION_GITHUB_TOKEN` rotated and updated in GitHub Actions secrets; backup and audit logged.
