# ROADMAP — Short-term roadmap (next 3 sprints)

Purpose

Now → Sprint 1 (2 weeks)
# Roadmap (Updated)

This roadmap is tuned for incremental, low-risk delivery. Each entry is split into small tasks and estimated roughly in hours.

1) CI & E2E stability — In Progress
	- Estimate: 4h
	- State: in-progress
	- Next: run two CI E2E runs; collect logs in `events.ndjson` and `gaia.db`.

2) Sprint Onboarding Automation — In Progress
	- Estimate: 6h
	- State: in-progress
	- Next: test `sprint_onboard.yml` on a labeled staging issue; add to Projects V2 using `PROJECT_V2_NUMBER=3`.

3) Automation Runner & Approval — In Progress
	- Estimate: 3h
	- State: in-progress
	- Next: run `scripts/run_20h.ps1` to supervise `automation_runner.py` for 20 hours (smoke tests first).

4) Secrets & Rotation Pilot — Planned
	- Estimate: 6h
	- State: planned
	- Next: complete `scripts/set_repo_tokens.ps1` dry-run and document rotation steps in `doc/SECRETS_HANDLING.md`.

5) Observability and Notifier — Planned
	- Estimate: 4h
	- State: planned
	- Next: enable `PERIODIC_NOTIFICATIONS_ENABLED=1` for heartbeat and implement `scripts/telegram_notifier.py`.

Notes:
- Work in small slices; prefer operator approvals and idempotent automation.
- Projects V2 is in use (project number 3). Classic Projects column id usage is deprecated in this repo.


---

<!-- Merged from docs/ROADMAP.md on 20260205T160615Z UTC -->

# GAIA Roadmap

Last updated: 2026-02-04

## Version History

- 2026-02-04 — v2026.02.04
  - Added CI stabilization work: written `.github/scripts/write_pth.py` to ensure repository imports in GitHub Actions and inserted smoke-check steps into workflows. (commits: aac820e, 73b00e4)
  - Fixed YAML matrix parsing by quoting `python-version` strings to avoid unintended float parsing.
  - Neutralized broken `external/openclaw` submodule by converting it to tracked files and added documentation.
  - Added Telegram scaffolding and helpers: scheduled summary job, secrets helper, and local test verification.

## Stories & Work Items

### Story: CI & Test Reliability
- Goal: Make the repository importable in CI so pytest collection and early smoke-import checks pass.

- Completed items:
  - Open PR to fix CI (`chore/fix-ci-workflow`) — completed 2026-02-04
  - Patch CI to write `gaia_repo_path.pth` (`.github/scripts/write_pth.py`) — completed 2026-02-04
  - Replace heredoc steps with cross-platform Python helper — completed 2026-02-04
  - Quote `python-version` entries in workflows to avoid YAML float parsing — completed 2026-02-04
  - Validate CI and imports across matrix (smoke import + pytest) — completed 2026-02-04

- Pending / Next:
  - Add optional fallback `python -m pip install -e .` in problematic jobs (conditional)
  - Add Telegram integration smoke matrix tests

### Story: Secrets & Telegram Integration
- Goal: Provide safe Telegram integration and ensure secrets are handled correctly.

- Completed items:
  - Telegram periodic summary scheduled job — completed 2026-02-04
  - Store `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in repository Secrets — completed 2026-02-04
  - Add `scripts/set_repo_secrets.ps1` helper — completed 2026-02-04
  - Local test summary run verified with `scripts/telegram_summary.py` — completed 2026-02-04

- Pending / Next:
  - Add secret scanning (detect-secrets baseline + CI) — planned
  - Remove secrets from Git history (scrub & rotate) — planned
  - Create protected `production` environment and gating rules — planned

### Story: External/openclaw Integration
- Goal: Neutralize broken submodule and provide reuse instructions.

- Completed items:
  - Convert `external/openclaw` submodule to tracked files — completed 2026-02-04
  - Add `external/openclaw/README.md` and `docs/OPENCLAW_REUSE.md` — completed 2026-02-04

- Pending / Next:
  - Decide vendor/submodule/package strategy and integrate usage wrapper — planned

### Story: Automation & Repository Maintenance
- Goal: Improve developer ergonomics and automation for merges and releases.

- Completed items:
  - Added scheduler helper `scripts/ascheduler.py` and docs — completed 2026-02-04
  - Defined naming conventions for tasks, scripts, and env vars — completed 2026-02-04

- Pending / Next:
  - Add auto-merge workflow to merge PRs after CI + approval
  - Purge leaked tokens from history if any remain (coordinate force-push)

## How to read this file
- Each story lists completed items with the date they were inserted into the roadmap (versioned).
- When an item is completed the entry is appended here with a short rationale and date.
- Use `TODO.md` at repo root for the current prioritized backlog (machine- and human-readable).
