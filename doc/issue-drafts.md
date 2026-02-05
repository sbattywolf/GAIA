# Issue drafts for high/critical tasks

Generated from `doc/todo-archive.ndjson` on 2026-02-05 14:10

## [ID 1] Purge leaked tokens (filter-repo plan)
- Epic: Security & Secrets
- Feature: Secrets Cleanup
- Story: Purge tokens from history

Description:
We discovered leaked tokens in history; plan to run `git filter-repo` (or BFG) with a reviewed rewrite plan to purge sensitive values. Steps:

1. Identify files and commits containing secrets (use detect-secrets to confirm).
2. Draft `filter-repo` replacement maps and test locally in a cloned copy.
3. Coordinate with maintainers about force-push windows and downstream mirrors.
4. Rotate any credentials confirmed leaked.

Priority: critical
Est hours: 24
Scrum points: 13

Links: `05_02_project_overview.md`, `doc/todo-archive.ndjson`

---

## [ID 2] Add detect-secrets + pre-commit
- Epic: Security & Secrets
- Feature: Secrets Tools
- Story: Secret scanning

Description:
Add `detect-secrets` configuration, a baseline scan, and a `pre-commit` hook to prevent future leaks. Include CI job to run baseline on PRs.

Priority: high
Est hours: 16
Scrum points: 8

---

## [ID 4] Implement mocked Telegram API harness
- Epic: CI & Testing
- Feature: Integration tests

Description:
Create a lightweight mocked Telegram API server (flask/fastapi) used in CI to exercise agent flows without external network dependencies. Ensure it can simulate 429 and 5xx responses.

Priority: high
Est hours: 16
Scrum points: 8

---

## [ID 5] Exponential backoff, tests for 429/5xx
- Epic: Telegram Integration

Description:
Implement and test retry/backoff behavior in messaging clients. Add unit/integration tests that simulate 429/5xx and assert backoff and retry limits.

Priority: high
Est hours: 16
Scrum points: 8

---

## [ID 6] Scaffold and run alby_agent dry-run prototype
- Epic: Agent Automation

Description:
Implement alby_agent dry-run functionality to validate doc merges and event emission without side-effects. Provide a `--dry-run` flag and local-only behavior.

Priority: high
Est hours: 16
Scrum points: 8
