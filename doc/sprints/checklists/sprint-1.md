# Sprint 1 Checklist — Current (2 weeks)

Priority sequence: stabilize CI → unblock tests → secure secrets → enable mocked integrations → lightweight automation.

- [ ] Ensure pytest basetemp in CI (`.tmp/pytest` or `--basetemp`) — create writable path in workflows
- [ ] Add CI step to create writable basetemp path before pytest
- [ ] Add DB test fixture / migration to provide `audit.timestamp` column for tests
- [ ] Guard/remove TTY/ioctl calls from scripts used in CI (make non-interactive safe)
- [ ] Implement mocked Telegram harness and CI-local runner ([#61])
- [ ] Prepare filter-repo plan + playbook for token purge (draft) ([#59])
- [ ] Add `detect-secrets` + `pre-commit` integration (dry run) ([#60])
- [x] Add/verify VS Code auto-approve task and local confirmation flow (done)
- [ ] Run full local `pytest -q` and produce failing-tests report

Notes / next actions:
- Complete basetemp + TTY guards first to reduce CI noise.
- Break any remaining items into separate issues for tracking and assignment.
