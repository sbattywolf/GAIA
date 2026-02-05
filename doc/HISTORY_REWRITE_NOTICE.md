# History Rewrite: Maintenance Notice (short)

Purpose: request approval and schedule a short, coordinated maintenance window to perform a safe history-rewrite using `git-filter-repo`.

Proposed window (UTC): __________________

Impact: repository history will be rewritten; after the final push, all contributors should reclone or run:

```bash
git fetch origin --prune
git reset --hard origin/<branch>
```

Quick checklist for owners:
- Rotate/revoke any live credentials found in `.tmp/replace_candidates.csv`.
- Confirm tests and detect-secrets results on the dry-run mirror.
- Approve the final push via issue comment `approve`.

If you'd rather postpone or disable the rewrite, comment `defer` or `disable` on the request issue.

See `doc/HISTORY_REWRITE_PLAN.md` for full details and commands.
