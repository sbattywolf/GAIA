# Multi-Agent Architecture — GAIA

Goal

Design a safe, auditable multi-agent system for GAIA where small agents perform focused tasks (tests, PRs, issue triage, Telegram notifications) under strict security and review controls. Start with Telegram as the first channel and iterate.

Core idea

Multiple input channels (Telegram, email, local GUI) feed a single Orchestrator/Controller that centralizes validation, backlog management, and dispatching to agents. Agents (local or online) perform tasks and return events; the Orchestrator is the canonical source of truth.

Responsibilities (concise)

- **Orchestrator:** accept commands/events, validate, persist backlog/epics/stories, resolve conflicts, enforce permissions, and record audit traces.
- **Agents:** perform focused work (create issues, run checks, send notifications). Prefer asynchronous events and require orchestrator approval for state changes that affect backlog or production.
- **Channel adapters:** thin translators that convert channel-specific messages into normalized orchestrator commands/events.

Design primitives (schemas & contracts)

- Event / Command schema (JSON):

```json
{
  "id": "uuid",
  "type": "command|event",
  "action": "create_issue|notify|scaffold_project",
  "source": "telegram|email|gui|agent_name",
  "actor": "user:alice|agent:ci-bot",
  "payload": { },
  "timestamp": "2026-02-04T12:34:56Z",
  "trace_id": "uuid",
  "idempotency_key": "optional-string"
}
```

- Orchestrator↔Agent contract:
  - Small synchronous RPCs for low-latency checks (authorize, validate).
  - Async event bus for work items: agents subscribe to events, publish results/events back with `trace_id`.
  - All messages must include `trace_id` and `idempotency_key` for dedupe and audit.

- Auth & trust model:
  - Agents hold short-lived credentials; only orchestrator stores authoritative secrets.
  - Use `ALLOW_COMMAND_EXECUTION` and `PROTOTYPE_USE_LOCAL_EVENTS` flags to gate side effects.

Audit & observability

- Append-only events: `events.ndjson` (one JSON object per line) is the event sink.
- Persist concise traces in `gaia.db` (`audit` table) for critical actions with references to `trace_id`.

Safety controls

- Default simulation: `PROTOTYPE_USE_LOCAL_EVENTS=1` in PRs and CI.
- Production secrets stored in `production` GitHub Environment and require `REVIEWERS` for access.
- Critical workflows (real sends, merges) require explicit human approval and environment gating.

Telegram-first prototype plan (practical steps)

1) Channel adapter
  - Implement a Telegram adapter that converts messages and commands into normalized events and POSTs them to the orchestrator API or appends to `events.ndjson`.

2) Minimal Orchestrator API
  - Provide a small HTTP endpoint to accept events, validate, persist backlog items, and return `trace_id`.

3) Backlog management
  - Orchestrator stores backlog items (epic/story/feature) in a simple SQLite table and exposes read endpoints.

4) Agent prototype
  - One online agent (Actions or bot) that reads events and creates scaffolded GitHub issues or repo scaffolding in dry-run mode, posting results back to orchestrator and `events.ndjson`.

5) Tests and mocks
  - Reuse `scripts/mock_telegram_server.py` and `tests/conftest.py` to run integration tests locally and in CI.

6) Audit & approvals
  - Each action that reaches production writes an audit row to `gaia.db` and requires environment-level approval.

Risks & mitigations

- Conflicting updates: always route state changes through the Orchestrator; avoid agent-to-agent direct writes except when orchestrator-authorized.
- Privilege escalation: prefer short-lived tokens, limit scopes, and require reviewers for production secrets.
- Test drift between local and Actions: keep CI deterministic, set `PYTHONPATH` in workflows, and optional editable install (`pip install -e .`) for consistent imports.

Next steps I can take (pick one):

- Update `doc/MULTI_AGENT_ARCHITECTURE.md` with diagrams and the JSON schema as machine-readable files.
- Scaffold the Telegram adapter and minimal orchestrator HTTP endpoint plus a test harness.
- Create a minimal GitHub App manifest and CI workflow to exercise the backlog agent in dry-run mode.

---

Files referenced: `events.ndjson`, `gaia.db`, `scripts/mock_telegram_server.py`, `tests/conftest.py`, `.private/.env`, `.github/workflows/ci.yml`.
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
