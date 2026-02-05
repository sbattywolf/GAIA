### Filter-repo purge plan + playbook for token purge (dry-run)

Problem
- Leaked tokens were discovered; history needs pruning in a safe, reviewable way.

Goal
- Produce a safe `git filter-repo` plan and an operational playbook for purging secrets from history with a staged rollout.

Acceptance criteria
- A documented dry-run plan (`filter-repo --analyze` / `--replace-refs`) exists in the repository (e.g., `doc/security/`), including verification steps.
- Backup and restore steps are documented; reviewers confirmed.

Notes
- Reference existing issue #59 and include the list of known leaked files/strings.
- Label: `security`, `critical`