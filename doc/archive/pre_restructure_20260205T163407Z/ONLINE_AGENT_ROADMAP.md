# Online Agent Roadmap — GAIA

Purpose

Provide a concise, executable roadmap for the minimal online agent (GitHub Actions) and the next iterations (Telegram bridge, hardening, CI integration). Include time estimates, feature/user-stories, tasks, and scrum story points so we can prioritize work and start implementing quickly.

Assumptions
- Two-week sprint cadence (adjustable). Keep initial scope small and safe (prototype/simulated mode by default).

MVP (Goal: remote-control basics, safe, manual dispatch)
- Deliverables (already partly done):
  - `.github/workflows/online-agent.yml` (workflow_dispatch)
  - `scripts/online_agent.py` (dry_run, send_telegram, create_issue)
  - `doc/ONLINE_AGENT_README.md`

MVP stories & tasks

1) As a repo operator I can run a manual online agent dry-run
   - Acceptance: workflow can be dispatched with `command=dry_run`, `events.ndjson` receives an event, `gaia.db` audit row created.
   - Tasks: verify workflow, add CI smoke-test. (Est: 2h, 1 SP)

2) As a repo operator I can send a Telegram test (prototype mode)
   - Acceptance: with `PROTOTYPE_USE_LOCAL_EVENTS=1` the run logs show the action simulated; with `PROTOTYPE_USE_LOCAL_EVENTS=0` and `ALLOW_COMMAND_EXECUTION=1` (protected env) the message is delivered.
   - Tasks: add secrets to protected env, test runs, document. (Est: 4h, 2 SP)

3) As a repo operator I can create an issue via the agent
   - Acceptance: `command=create_issue` opens a GitHub issue; event and audit recorded.
   - Tasks: test GH API flow, ensure token scope, document. (Est: 3h, 2 SP)

Phase 1 (stability & safety)

4) Add production environment + protections
   - Tasks: create GitHub Environment `production`, add secrets, require reviewers for the environment.
   - Est: 1h, 1 SP

5) Add CI smoke test for the agent
   - Tasks: add a CI job that runs `scripts/online_agent.py --command dry_run` in Actions matrix; fail if script errors.
   - Est: 2h, 1 SP

6) Harden agent (retries, logging, tests)
   - Tasks:
     - add retry/backoff for network calls (requests + simple backoff)
     - structured logging (JSON or plain with timestamps)
     - unit tests for `online_agent.py` behaviors (dry_run, error handling)
     - integration test that runs against mock Telegram server
   - Est: 12–18h, 8 SP

Phase 2 (automation & bridge)

7) Bridge Telegram → GitHub (lightweight adapter)
   - Story: accept chat commands and trigger `gh workflow run online-agent.yml` (simulated first).
   - Tasks:
     - small adapter (serverless or a minimal Heroku/Glitch container) to receive Telegram updates and call `gh` REST run API
     - permission model: adapter uses a bot account or dispatch token; require reviewers for production runs
     - safety: commands default to simulation unless reviewer-approved
   - Est: 16–24h, 13 SP

Phase 3 (operational & advanced)

8) Auto-PR and triage agent
   - Story: agent creates PRs for low-risk fixes and opens triage issues for higher-risk items.
   - Tasks: auto-PR workflow, review policy, event tracing.
   - Est: 8–12h, 5 SP

9) Observability & dashboard
   - Story: lightweight dashboard (SSE or static tail) for `events.ndjson` and `gaia.db` traces.
   - Tasks: small web UI or static logs viewer, health checks, tailing. (Est: 8h, 5 SP)

Total rough estimate (to reach safe automated Telegram bridge + hardened agent): ~45–70 hours (rough), ~34 story points.

Priority suggestions
- Highest: secure production secrets + verify dry-run and GH issue flows (Phase 0 → Phase 1 tasks 1–5).
- Next: harden agent with tests and add CI smoke test (Phase 1 task 6).
- Then: bridge Telegram→GH in simulated mode and test (Phase 2 task 7).

Minimal next sprint (2 weeks) — recommended backlog
- Sprint goal: Harden agent and add CI smoke tests; prepare production env.
  - Tasks:
    - Add CI smoke test for `online_agent.py` (2h, 1 SP)
    - Implement retry/backoff and structured logging (6h, 3 SP)
    - Add unit tests for dry_run and error-handling (4h, 3 SP)
    - Create production environment and add secrets (1h, 1 SP)
  - Sprint total: 13h (est), 8 SP

Risks & mitigations
- Risk: accidental external sends — mitigate by defaulting to `PROTOTYPE_USE_LOCAL_EVENTS=1`, gating production secrets via protected environment, and requiring reviewers.
- Risk: agent token compromise — mitigate with short-lived tokens and limited scopes.
- Risk: CI drift — keep local test harness (mock server) and add CI smoke test early.

Acceptance & done criteria (MVP):
- Manual dispatchable workflow exists and runs without errors in dry-run.
- `events.ndjson` and `gaia.db` have consistent entries for commands.
- Production secrets exist in a protected GitHub Environment and manual approval is required to enable real sends.

Next immediate action (I will do on confirmation): implement the Harden agent with tests (Phase 1 task 6). I will:
1. Add retry/backoff to `scripts/online_agent.py` for network calls.
2. Add structured logging to the script.
3. Add unit tests for dry_run and error paths under `tests/test_online_agent.py` (mock requests).
4. Add a CI smoke-step that runs `scripts/online_agent.py --command dry_run`.

Estimated time for that immediate action: 12–18 hours (8 SP). If you confirm, I'll start by adding the tests and retry/backoff.

## Score & Reuse Tracking

To keep track of how previous work, tests, and reusable components reduce future estimates, we append a simple scoring table. Update this table as you complete work or identify reusable components — the **Score** column should reflect how much effort (in % of original estimate) can be reused from earlier work (higher score = more reuse, lower remaining work).

### High-level functionality score (per chapter)

| Functionality / Chapter | Original Estimate (hours) | Reuse Score (%) | Adjusted Estimate (hours) | Notes |
|---|---:|---:|---:|---|
| Manual dry-run & audit | 2 | 80 | 0.4 | Events + audit already implemented and tested |
| Send Telegram (prototype) | 4 | 60 | 1.6 | Mock server + env gating available |
| Create GH issue | 3 | 70 | 0.9 | `backlog_agent` patterns reusable |
| Hardening (retries/logging/tests) | 12 | 30 | 8.4 | Some retry code present; tests added |
| CI smoke test | 2 | 0 | 2.0 | New CI step required |
| Bridge Telegram→GH (Phase 2) | 20 | 10 | 18.0 | Architecture partially documented |

### Per-entity / per-functionality quick tracker

Use this smaller table for per-function or entity-level tracking (update with PR/commit refs):

| Entity / Function | Status | Reuse (%) | Remaining Notes |
|---|---|---:|---|
| `events.ndjson` append | Done | 100 | Core mechanism in place, reuse fully |
| `gaia.db` audit writes | Done | 80 | `audit_v2` fallback added to maintain compatibility |
| `scripts/mock_telegram_server.py` | Done | 70 | Use in integration tests |
| `scripts/online_agent.py` | In progress | 40 | Adding env-driven retries and tests (this PR) |
| CI workflow (smoke) | In progress | 0 | New smoke-step being added |

Update these tables every sprint to reflect measured reuse and to reduce future estimates accordingly.
