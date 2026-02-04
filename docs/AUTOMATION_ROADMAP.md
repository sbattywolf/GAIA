Automation roadmap
==================

This document describes the small, incremental automation steps planned for the prototype.

Goals
- Speed up PR merges for low-risk changes during prototype.
- Keep automation opt-in and observable.
- Keep secrets and elevated permissions out of committed files.

Planned steps (phased)
1) Opt-in automerge label + workflow (done): `automerge` label + `.github/workflows/auto-merge.yml`.
2) Local/cron agent (added): `agents/automerge_agent.py` — uses `gh` CLI, dry-run mode. Can be scheduled or run manually.
3) Observability: agent logs and small `events.ndjson` append for automated actions.
4) Expand automation: add tagging, release creation, and test promotion.

Security / safe defaults
- Agent requires `gh` CLI authentication and uses CLI commands (no tokens in files).
- `automerge` label is required to opt a PR into automation.
- `--dry-run` useful for testing; CI can run the agent in dry-run mode first.

Next improvements
- Add an agent-runner GitHub Action to execute the agent on a schedule.
- Add optional PR gating (label + minimum approvals) when moving out of prototype.
- Integrate with ticketing (Jira/Linear) and an audit log for automated merges.
