# Per-Sprint Roadmap (next 4 sprints)

This document expands the per-sprint roadmap. Sprint 1 is detailed and prioritized so you can start executing immediately. Sprints 2–4 are high-level epics to refine after Sprint 1 completes.

---

## Sprint 1 — Current (2 weeks)

Priority sequence: stabilize CI → unblock tests → secure secrets → enable mocked integrations → lightweight automation.

| Story / Task | Priority | Est Hrs | Status |
|---|---:|---:|---:|
| Ensure pytest basetemp in CI (`.tmp/pytest` or `--basetemp`) | high | 4 | pending |
| Add CI step to create writable basetemp path before pytest | high | 2 | pending |
| Add DB test fixture / migration to provide `audit.timestamp` column | high | 8 | pending |
| Guard/remove TTY/ioctl calls from scripts used in CI | high | 6 | pending |
| Implement mocked Telegram harness and CI-local runner ([#61]) | high | 16 | pending |
| Prepare filter-repo plan + playbook for token purge (draft) ([#59]) | critical | 12 | pending |
| Add `detect-secrets` + `pre-commit` integration (dry run) ([#60]) | high | 8 | pending |
| Add/verify VS Code auto-approve task and local confirmation flow | medium | 2 | completed |
| Run full local `pytest -q` and produce failing-tests report | high | 4 | pending |

Notes: Complete tasks in the order above; many small fixes (basetemp, TTY guards) will immediately reduce CI noise.

---

## Sprint 2 — Stabilize & Harden

- Finish integration tests: acceptance flows (claim→approve→archive), idempotency/replay tests.
- Implement exponential backoff and tests for 429/5xx handling ([#62]).
- Complete alby_agent dry-run integration and basic metrics collection ([#63]).
- Create CI job matrix to run critical integration tests in isolation.

---

## Sprint 3 — Secrets & Ops

- Execute filter-repo purge (windowed, reviewable) and rotate tokens.
- Create GitHub `production` environment with required reviewers and protection rules.
- Wire metrics persistence, alerts, and basic dashboard for failed/retry rates.

---

## Sprint 4 — Automation & Scale

- Expand alby_agent automation to handle release tasks and doc merges.
- Add monitor UI actions (one-click requeue) and secure audit traces.
- Runbook completion and on-call playbooks; test runbooks via mocked harness.

---

### Sequence to execute now (Sprint 1, in order):
1. CI basetemp creation + ensure writable path.
2. Add test DB fixture / small migration to create `audit.timestamp` for tests.
3. Guard scripts for TTY/ioctl usage so CI is non-interactive-safe.
4. Implement mocked Telegram harness and CI-local runner.
5. Prepare filter-repo purge plan (dry-run) and safe rollout steps.
6. Add `detect-secrets` + `pre-commit` (dry-run) and iterate.
7. Run and triage local `pytest -q`; open follow-up issues for remaining flakes.

---

If you'd like, I can:
- Break Sprint 1 stories into individual GitHub issues.
- Create `doc/sprints/checklists/` with per-task checkboxes.
- Open PRs that apply the minimal CI fixes (basetemp + TTY guards) in sequence.
