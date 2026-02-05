# Scheduler Runbook — GAIA

Purpose
- Operational guidelines for running and registering scheduler scripts, DryRun checks, monitoring, and safe deployment patterns.

How to run safely (DryRun first)
- Ensure environment loaded: source `.private/.env` or use `env_loader` where available.
- Run scheduler prototype DryRun (example):

  powershell -NoProfile -ExecutionPolicy Bypass -File .\TOBEDELETE__AILocalModelLibrary\scripts\scheduler-prefer-skill.ps1 -DryRun -OutPath .\.tmp\scheduler_proposal.json

- Run the agents orchestrator DryRun:

  powershell -NoProfile -ExecutionPolicy Bypass -File .\TOBEDELETE__AILocalModelLibrary\scripts\run-agents-epic.ps1 -DryRun -MaxVramGB 32

Registration (Windows Scheduled Task)
- Use `register_monitor_task.ps1` to create Windows Scheduled Tasks. It includes unregister guidance.
- Always test the registered task with a DryRun/config that writes to a temporary output directory.

Observability
- Scheduler scripts should write proposals and status files to `.continue/` and emit audit events to `events.ndjson` or `gaia.db` via existing `orchestrator` helpers.
- Ensure `logs/` exists and is rotated. Recommend log retention: 30 days by default; archive older logs to `logs/archive/`.

Safety & best practices
- Require `-DryRun` verification before enabling production registration.
- Use `env_loader` to load secrets and gate live actions with `ALLOW_COMMAND_EXECUTION`.
- Prefer idempotent scripts: avoid in-place mutation of shared state without atomic writes (use `.tmp` then Move-Item).
- Limit resource parameters (e.g., `MaxVramGB`, `MaxParallel`) and validate config inputs.
- Add monitoring/alerts on repeated failures (use simple file-based dead-letter and an event emitter to `events.ndjson`).

CI
- Add a CI job that runs DryRun for each scheduler script (matrix with small `MaxVramGB` and `DryRun` flags) and validates output JSON structure.
