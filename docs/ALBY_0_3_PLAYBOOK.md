# Alby 0.3 Playbook — Run, Monitor, Escalate

This playbook describes how to run Alby 0.3 locally, step it up to more
complex tasks, and collect the minimal telemetry to improve next-gen agents.

1) Run Alby locally (basic)
- Ensure Python venv active and deps installed (`requirements.txt`).
- Example command (dry-run):

```powershell
python agents/alby_agent.py --cmd "echo hello" --concurrency 2 --dry-run
```

2) Increase task complexity (gradual)
- Step 1: single-shell commands (install, build, test) via `--cmd`.
- Step 2: task manifests (JSON files) describing multi-step tasks; Alby will
  run steps sequentially and emit per-step events.
- Step 3: integrate with CI runner (GitHub Actions or local runner) to run
  tasks in CI and send results back as events.

3) Monitoring & tracing
- Alby emits `alby.job.complete` events with `idem` and `trace` fields.
- Use `scripts/monitor_events.py` to get quick metrics and spot duplicates
  or errors.
- For deeper tracing, tail `events.ndjson` and forward events to a
  lightweight visualizer (not included here).

4) Escalation & controller
- If tasks require coordination, add a minimal `orchestrator` to consume
  events and schedule work with dedup and retries.

5) Secret placeholders & playbook for installs
- Use `.env` to store sensitive placeholders (do not commit). Example
  variables:

```
ALBY_INSTALL_USER=youruser
ALBY_INSTALL_PW_PLACEHOLDER=__REPLACE_ME__
```

When automating installs, record placeholders in manifests so you can
replace them with secure retrieval (Bitwarden CLI or CI secrets) later.

6) Next steps
- Add a manifest consumer to `agents/alby_agent.py` to run multi-step tasks.
- Add a CI job to run selected manifests and return results as events.
