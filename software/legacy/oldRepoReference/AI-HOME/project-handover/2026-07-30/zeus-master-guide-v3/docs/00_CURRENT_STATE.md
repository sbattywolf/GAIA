# Current state

## Completed

### Milestone 1: semantic formatter

- Correct Italian vocabulary for windows, doors and light entities.
- Deterministic fast path preserved.
- Telegram results validated.

### Milestone 2: aggregate queries and home report

- Single and multi-category counts.
- Deterministic multiline/multi-category request handling.
- Home report.
- Automation state breakdown.
- `ZEUS_MAX_ENTITY_LIST` protection.
- Typo `accesse` recognised.
- One `get_states()` snapshot per aggregate/report request.
- 34 unit tests passed during implementation and on the 1070 test branch.

## Verified runtime observations

- Automation snapshot: 28 enabled (`on`), 6 disabled (`off`), 1 unavailable.
- Runtime report successfully returned open windows, open doors, light-domain entities on, automation breakdown and total unavailable entities.
- The report counted 375 unavailable entities in that snapshot. This is intentionally a raw runtime count and is not yet semantically filtered.
- The light-domain response still includes technical entities such as an indicator light and may contain group/member duplication. This is expected until Milestone 3/4.
- Telegram conflict observed during testing was caused by manually launching a second bot process while systemd already ran the official process.
- Correct operational rule: never start `telegram_agent.py` manually while `zeus-edge.service` is active.

## Service state at pause

- `zeus-edge` observed active.
- One `telegram_agent.py` process observed after controlled restart.
- Local documentation/backup stash was restored and dropped.
- Older stash `wip-followup-filters-before-ha-conversation` remains intentionally un-applied.

## Before resuming

Run only these checks on the 1070:

```bash
cd ~/github_repos/home_assistant_framework
git branch --show-current
sudo systemctl is-active zeus-edge
pgrep -af 'telegram_agent.py'
```

Expected: bootstrap branch, active service, one bot process. If the exact branch differs, inspect before changing anything.
