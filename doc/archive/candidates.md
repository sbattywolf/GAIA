# Archive candidates

These files appear to be scheduler prototypes, large test artifacts, or examples that should be reviewed for archival or relocation into `scripts/schedulers/` or `doc/archive/`.

- TOBEDELETE__AILocalModelLibrary/scripts/scheduler-prefer-skill.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/scheduler-prefer-skill.psm1
- TOBEDELETE__AILocalModelLibrary/scripts/register_monitor_task.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/trace-schedule-local-llama.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/run-agents-epic.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/monitor-agents-epic.ps1
- TOBEDELETE__AILocalModelLibrary/scripts/stress/stress-parallel.ps1
- TOBEDELETE__AILocalModelLibrary/.continue/* (ci-failures, large json artifacts)
- TOBEDELETE__AILocalModelLibrary/.continue/skill-candidates.json (very large)

Action suggestion
- Move the `TOBEDELETE__AILocalModelLibrary` folder into `doc/archive/AILocalModelLibrary/` after quick validation, or split production-ready scripts into `scripts/schedulers/` and keep prototypes in `doc/archive/`.
- Keep `register_monitor_task.ps1` and `run-agents-epic.ps1` if they are actively used; otherwise archive.
