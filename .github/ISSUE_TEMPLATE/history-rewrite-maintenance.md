---
name: History rewrite maintenance request
about: Request approval & schedule maintenance window to run a safe history rewrite (opt-in)
title: "[ACTION REQUIRED] Request: History rewrite maintenance window"
labels: maintenance, security
assignees: ''
---

## Summary
We propose a short maintenance window to run a safe, auditable history rewrite to remove previously-identified leaked secrets from repository history.

This is a destructive operation (force-push). All live credentials must be rotated before the final push.

## Proposed window
- Date/time (UTC): __________________
- Duration: 30–60 minutes

## Impact
- All active branches will be rewritten. Contributors must reclone or run `git fetch --all --prune` and reset their local branches after the push.

## Checklist (please comment or react to approve)
- [ ] I confirm my team has rotated/revoked any live credentials identified in `.tmp/replace_candidates.csv`.
- [ ] I accept the maintenance window and will stop pushing during the window.
- [ ] I approve the final force-push when the audit and tests pass.

If you want this postponed, comment `defer` and assign an alternative date.

---
Short note: the full step-by-step plan is in `doc/HISTORY_REWRITE_PLAN.md`.
