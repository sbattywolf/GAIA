# CHECKPOINT_1: Normalize todos → PR draft

Action planned: create branch `feat/normalize-todos`, add `doc/todo-archive.ndjson`, and open a PR to merge into `master`.

Why: this is a repository-visible normalization of high/critical tasks so maintainers can triage and create issues.

Files changed locally: 
- `doc/todo-archive.ndjson` (NDJSON archive of prioritized tasks)

Automated steps to run (if you want me to continue automatically):

```bash
git checkout -b feat/normalize-todos
git add doc/todo-archive.ndjson CHECKPOINT_1.md
git commit -m "chore(todo): add normalized todo-archive.ndjson"
git push --set-upstream origin feat/normalize-todos
# Optionally create PR with gh (requires authentication):
gh pr create --fill --title "chore(todo): normalize todos" --body-file CHECKPOINT_1.md
```

Notes: I have not yet opened the PR. Creating a PR is a high-impact remote action; if you want full autonomy I can attempt to create it now and handle failures.
CHECKPOINT 1 — Execute automation runner actions

Plan:

1. Proceed to execute approved automation tasks from `tasks.json`.
2. Perform side-effecting actions (create issue, post to external APIs) only after this checkpoint is approved.
3. After approval, runner will update `.copilot/session_state.json` and perform micro-commit steps.

Approval:

APPROVATO

Add the single word APPROVATO (uppercase) anywhere in this file to permit execution.

Current status: APPROVATO
