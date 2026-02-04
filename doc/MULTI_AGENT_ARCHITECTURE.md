# Multi-Agent Architecture — GAIA

Goal

Design a safe, auditable multi-agent system for GAIA where small agents perform focused tasks (tests, PRs, issue triage, Telegram notifications) under strict security and review controls.

Principles

- Least privilege: agents receive only the permissions they need (Actions/GitHub App scopes).
- Human-in-the-loop for external side-effects: any real-world send (Telegram, GH issue closure, external API) requires a protected environment and reviewer approval.
- Observable & auditable: agents write concise events to `events.ndjson` and record audit traces in `gaia.db`.
- Incremental rollout: start with safe, read-only or simulated agents; add protected manual approvals for higher-impact actions.

Agent Roles

1. CI Agent (Actions)
- Purpose: run tests, run linters, build artifacts, and optionally open auto-PRs for trivial fixes.
- Scope: repo `contents: write` for PRs, actions runner token; PRs should be created by `GITHUB_TOKEN` or a bot account.
- Safety: auto-PRs only when tests pass; schedule or manual triggers recommended.

2. Backlog Agent
- Purpose: create and triage GitHub issues based on analysis (failed runs, lint issues, security scanning).
- Scope: `issues: write` or GitHub App with limited issue-scoped permissions.
- Safety: include `trace_id` in issue bodies and append event to `events.ndjson`.

3. Telegram Notification Agent
- Purpose: send periodic progress summaries or alerts to Telegram channels/users.
- Scope: environment-scoped secrets (TELEGRAM_BOT_TOKEN, CHAT_ID); no direct write to repo required.
- Safety: gated by `production` environment, require reviewers; default to simulated mode in PRs/CI.

4. Auto-PR Bot
- Purpose: perform small automated fixes (formatting, dependency updates) and open PRs.
- Scope: `contents: write`, `pull-requests: write`; prefer a dedicated bot account or GitHub App.
- Safety: create PRs only; never auto-merge without human approval.

Permissions & Environment Strategy

- Use GitHub Environments for secrets and gating: `production` environment holds `TELEGRAM_BOT_TOKEN` and other high-privilege secrets.
- Use `PROTOTYPE_USE_LOCAL_EVENTS=1` in PRs and simulated runs to avoid external side effects.
- Require `REVIEWERS` for `production` environment and protect real-send workflows with manual approval.

Phased Rollout Plan

Phase 0 — Safe baseline
- Add `validate_secrets.py`, `.private/.env` workflow helpers, mock Telegram server for tests, pre-commit secret checks.
- Keep CI in simulated mode for PRs.

Phase 1 — Automated housekeeping (low risk)
- Deploy Auto-PR workflows (manual dispatch + tests). Use the PR branch/merge policy to review and merge.

Phase 2 — Triage automation
- Backlog agent creates issues for high-confidence findings (failed reproducible tests, security alerts).
- Use a bot account or GitHub App; events logged in `events.ndjson`.

Phase 3 — Controlled notifications
- Enable scheduled notifications using `production` environment and required reviewers.
- Keep an opt-out and simulated mode for testing.

Phase 4 — Advanced agents (opt-in)
- Consider a GitHub App for advanced workflows (commenting, merging under policy), with explicit approvals and narrow scopes.

Operational Notes

- Audit: write agent actions to `gaia.db` and keep `events.ndjson` append-only.
- Emergency stop: every agent must respect `ALLOW_COMMAND_EXECUTION=0` and `PROTOTYPE_USE_LOCAL_EVENTS=1` defaults.
- Onboarding: document how to create `production` environment and set secrets (see `doc/TELEGRAM_ENV_TEMPLATE.md`).

Next steps (I can implement):
- Produce a minimal GitHub App manifest and deployment steps.
- Scaffold the Backlog Agent to create issues from failed CI runs.
- Add a small dashboard/monitor to tail `events.ndjson` via SSE.

