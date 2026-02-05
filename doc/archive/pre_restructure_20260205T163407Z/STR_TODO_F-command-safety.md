# TODO — F-command-safety (Command execution safety)

Status: planned

Tasks
- [ ] t14 — Enforce `ALLOW_COMMAND_EXECUTION=0` by default
- [ ] t15 — Add UI confirmation modal / explicit approval step for destructive commands
- [ ] t16 — Add safe-quoting helpers and tests for `tg_command_manager.py`

Notes
- These tasks are high priority for preventing accidental destructive actions. I'll prefer doc + small code changes first (env defaults, tests), then add UI/approval scaffolds.
