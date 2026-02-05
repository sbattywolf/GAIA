# Sprint 1 Checklist — Current (2 weeks)

Priority sequence: stabilize CI → unblock tests → secure secrets → enable mocked integrations → lightweight automation.

- [ ] Ensure pytest basetemp in CI (`.tmp/pytest` or `--basetemp`) — create writable path in workflows ([#64](https://github.com/sbattywolf/GAIA/issues/64))
- [ ] Add CI step to create writable basetemp path before pytest ([#64](https://github.com/sbattywolf/GAIA/issues/64))
- [ ] Add DB test fixture / migration to provide `audit.timestamp` column for tests ([#65](https://github.com/sbattywolf/GAIA/issues/65))
- [ ] Guard/remove TTY/ioctl calls from scripts used in CI (make non-interactive safe) ([#66](https://github.com/sbattywolf/GAIA/issues/66))
- [ ] Implement mocked Telegram harness and CI-local runner ([#67](https://github.com/sbattywolf/GAIA/issues/67))
- [ ] Prepare filter-repo plan + playbook for token purge (draft) ([#68](https://github.com/sbattywolf/GAIA/issues/68))
- [ ] Add `detect-secrets` + `pre-commit` integration (dry run) ([#69](https://github.com/sbattywolf/GAIA/issues/69))
- [x] Add/verify VS Code auto-approve task and local confirmation flow (done)
- [ ] Run full local `pytest -q` and produce failing-tests report ([#70](https://github.com/sbattywolf/GAIA/issues/70))

Notes / next actions:
- Complete basetemp + TTY guards first to reduce CI noise.
- Break any remaining items into separate issues for tracking and assignment.
