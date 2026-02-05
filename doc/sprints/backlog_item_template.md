Backlog Item / Issue Template
=============================

Use this template when creating stories, bugs, or tasks related to the triage automation or other sprint work.

- Title: [type] Short descriptive title (e.g. Bug: gist uploads failing)
- Summary: One-line summary of the item.
- Context / Links:
  - Link to relevant runs/logs: `doc/sprints/analysis/`
  - Link to events or prior issues: `events.ndjson` and `doc/sprints/analysis/created_followup_issues.txt`
  - Link to PRs or commits that introduced the behavior.
- Motivation: Why this matters, impact.
- Acceptance Criteria (explicit):
  - AC1: Observable condition showing fix is successful.
  - AC2: Tests or monitoring that will validate behavior.
- Reproduction Steps (for bugs):
  1. Step
  2. Step
- Proposed Fix / Notes: short description, risks, approximate estimate.
- Priority: P0/P1/P2
- Estimate: T-shirt or story points
- Owner: @handle
- Labels: area/ci area/triage bug enhancement
- Definition of Done:
  - Code changes merged, tests passing
  - Documentation updated (`README_RUNBOOK.md` or `doc/sprints/*`)
  - Monitoring or metric added to track regressions

Example: Stabilize gist uploads
- Title: Task: stabilize auto-triage gist uploads
- Summary: Ensure triage uploads run logs reliably; handle empty logs and API errors gracefully.
- Context / Links: `doc/sprints/analysis/created_gists.txt`, `doc/sprints/analysis/logs_archive_2026-02-05.zip`
- Motivation: Missing logs and failed gist uploads reduce traceability and create noise.
- Acceptance Criteria:
  - AC1: For 7 days, gist upload success rate >= 95%.
  - AC2: Empty logs are skipped and recorded, not attempted to upload.
  - AC3: Script comments the follow-up issue with gist URL when upload succeeds.
- Proposed Fix: Add pre-check for non-empty log files; retry with exponential backoff; add better CLI flag handling for `gh gist create`.
- Priority: P1
- Estimate: 3 points
- Owner: @sbattywolf
