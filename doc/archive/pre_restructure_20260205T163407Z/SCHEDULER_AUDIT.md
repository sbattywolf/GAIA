# Scheduler Audit — GAIA

Purpose
- Enumerate scheduler scripts and scheduled-task registrations in the repo, verify safety, idempotence, observability, and propose doc edits and archive candidates.

Discovered scheduler-related scripts and docs (initial list)
- TOBEDELETE__AILocalModelLibrary/scripts/scheduler-prefer-skill.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/scheduler-prefer-skill.psm1
- TOBEDELETE__AILocalModelLibrary/scripts/register_monitor_task.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/trace-schedule-local-llama.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/run-agents-epic.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/monitor-agents-epic.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/stress/stress-parallel.ps1
- TOBEDELETE__AILocalModelLibrary/docs/SESSION_SUMMARY_AND_EPICS.md
- TOBEDELETE__AILocalModelLibrary/docs/BACKLOG_OLLAMA_PENDING.md

Checklist (per-script)
- Identify scheduling mechanism: Windows Scheduled Task (`register_monitor_task.ps1`), cron, loop, or external orchestrator.
- Verify `DryRun` or safe mode exists and works.
- Confirm scripts are idempotent and safe to run concurrently.
- Ensure environment loading (`env_loader` / `.private/.env`) is explicit and documented.
- Confirm audit events are emitted to `events.ndjson` and/or `gaia.db` for start/complete/error.
- Validate logging: structured logs, rotation, and retention policy.
- Check resource constraints: vram/cpu/memory parameters respected and validated.
- Verify failure modes: retry/backoff, dead-letter or alerting, and non-silent failures.
- Check registration/unregistration helpers (e.g., `register_monitor_task.ps1`) include an uninstall path.
- Identify tests and CI coverage (Pester/pytest) for scheduler logic.

Repo-level recommendations
- Move legacy scheduler prototypes from `TOBEDELETE__AILocalModelLibrary` into a `scripts/schedulers/` area or `doc/archive/` with clear ownership notes.
- Add a short `docs/SCHEDULER_RUNBOOK.md` that prescribes: how to register tasks, recommended env flags, DryRun steps, and monitoring expectations.
- Add CI smoke tests: run `DryRun` for each scheduler script in a controlled matrix job.
- Document retention and rotation strategy for scheduler logs and `events.ndjson` traces.

Next actions (short)
1. Run each scheduler script in DryRun locally and capture outputs. (I can run these if you want.)
2. Produce `doc/archive/candidates.md` listing files to move/archive.
3. Draft `docs/SCHEDULER_RUNBOOK.md` with recommended patterns.
4. Finish `Agent Mode` review and produce `PLAN_AGENT_MODE.md` (next).

Notes
- Many scheduler-related files live under `TOBEDELETE__AILocalModelLibrary` (prototypes and tests). These should be reviewed for archival vs. production readiness.
