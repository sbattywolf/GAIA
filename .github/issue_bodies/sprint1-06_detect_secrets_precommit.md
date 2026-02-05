### Add `detect-secrets` + `pre-commit` integration (dry run)

Problem
- Repo contains leaked secrets historically; an automated scanning and pre-commit hook will prevent future leaks.

Goal
- Integrate `detect-secrets` as a scanning tool and configure `pre-commit` hooks for developer workflows (dry-run mode first).

Acceptance criteria
- A `detect-secrets` baseline is created and stored (or instructions provided to create one).
- A `pre-commit` config is added with `detect-secrets` in dry-run mode; documentation explains how to opt-in for baseline updates.

Notes
- This work should be non-disruptive initially (dry-run) and then rolled to blocking mode after vetting.
- Label: `security`, `high`