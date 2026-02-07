# Merged Sprint — 2026-02-07

Summary
- Date: 2026-02-07
- Branch consolidated: `fix/ci-test-fixes` merged with `master` and pushed
- Repo snapshot: created git bundle at `.tmp/archives/GAIA-repo.bundle`
- Goal: stabilize CI for token-policy work, collect failing logs, fix CI flakes, and prepare cleanup plan for repo size

This document consolidates today's sprint work, assigns story points and time estimates to tasks we've worked on together, and lists next actions for tomorrow.

Task list (status / story points / estimated hours)

- Define branch strategy — completed — 1 SP / 2h
- Scaffold Git agent — completed — 3 SP / 6h
- Enable safe auto-merge — not-started — 5 SP / 10h
- Add project table in `gaia.db` — completed — 2 SP / 3h
- Secrets & role model — not-started — 5 SP / 8h
- Scaffold repeatable tasks — not-started — 3 SP / 6h
- Add checkpoints/audit hooks — not-started — 3 SP / 6h
- Open PR for git agent — completed — 1 SP / 1h
- Document git history vs labels — completed — 1 SP / 1h
- Review GAIA PR #144 — completed — 1 SP / 1h
- Merge & cleanup PRs 145-148 — completed — 2 SP / 3h
- Implement token policy workflows — not-started — 8 SP / 16h
- Run CI on token policy PRs — not-started — 3 SP / 6h
- Analyze failures & propose fixes — not-started — 5 SP / 10h
- Fix detect-secrets `--json` flag — completed — 1 SP / 1h
- Monitor PR #158 secret-scan — not-started — 1 SP / 2h
- Collect failing logs for token PR — completed — 2 SP / 3h
- Add CI step to create `.tmp/pytest` — completed — 1 SP / 1h
- Add DB migration for `audit.actor` — completed — 2 SP / 2h
- Retrigger workflows by committing to `feat/implement-token-policy` — not-started — 1 SP / 1h
- Monitor CI runs for `feat/implement-token-policy` — not-started — 1 SP / 2h
- Fetch logs for any new failures — completed — 1 SP / 2h
- Run broader local test subset — completed — 1 SP / 2h
- Run local tests excluding `test_secrets.py` — completed — 1 SP / 1h
- Monitor PR #160 workflow runs — not-started — 1 SP / 2h
- Small sprint: projects-table PR & CI monitoring — not-started — 2 SP / 4h
- Open PR for `fix/ci-test-fixes` — completed — 1 SP / 1h
- Monitor CI for `fix/ci-test-fixes` — in-progress — 2 SP / ongoing
- Add `tests/conftest.py` to create `.tmp/pytest` at session start — completed — 1 SP / 1h
- Harden audit migrations to add missing columns — completed — 2 SP / 2h
- Patch workflows to remove detect-secrets `--json` and fix heredocs — completed — 2 SP / 3h
- Push workflow fixes and monitor CI — in-progress — 2 SP / ongoing
- Extract openclaw heredoc blocks into scripts and update workflows — completed — 2 SP / 3h
- Retrigger CI for `fix/ci-test-fixes` — completed — 1 SP / 0.5h
- Fetch new CI failed logs for `fix/ci-test-fixes` — completed — 1 SP / 1h
- Add basetemp directory creation to `ci-fixed` workflow — completed — 1 SP / 0.5h
- Create repo size report — completed — 1 SP / 0.5h
- Create git bundle archive of repository — completed — 1 SP / 0.5h
- Evaluate large-history cleanup options (BFG/filter-branch) — not-started — 5 SP / 10h
- Propose archive & history-rewrite plan for approval — not-started — 3 SP / 6h
- Merge master into current branch — completed — 1 SP / 0.5h
- Push merged branch to origin — completed — 1 SP / 0.5h

Notes and decisions
- Non-destructive snapshot: a `git bundle` archive saved to `.tmp/archives/GAIA-repo.bundle` for safe rollback/archive before any history rewrite.
- Rate limits: CI watcher requires authenticated `gh` (use `GITHUB_TOKEN`); started helper scripts to prompt for token.
- No history rewrites have been performed. Any destructive history edits will require an explicit CHECKPOINT and approval.

Next actions (highest priority)
1. Validate CI runs for `fix/ci-test-fixes` after merge and workflow updates (monitor via watcher) — owner: automation — 2 SP / ongoing
2. Prepare a detailed CHECKPOINT plan for large-history cleanup (identify large blobs, propose BFG vs LFS migration, impact & rollback) — owner: you/lead — 5 SP / 10h
3. Implement `feat/implement-token-policy` CI runs and iterate on remaining failures (heredoc, sqlite columns) — owner: engineering — 8 SP / 16h
4. Enable safe auto-merge policy (review branch protection and automerge workflow) — owner: engineering — 5 SP / 10h

If you're happy with these estimates and the merged sprint snapshot, I'll:
- commit this document to `doc/SPRINT_MERGED_2026-02-07.md` (done),
- open a follow-up CHECKPOINT file outlining the large-history cleanup plan for explicit approval before any destructive git history operations.
