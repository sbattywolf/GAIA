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
