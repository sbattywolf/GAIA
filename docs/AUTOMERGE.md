Auto-merge policy

This project supports an opt-in auto-merge flow for contributor convenience.

Policy summary

- Opt-in label: `automerge` — add this label to a PR to request automatic merging.
- Required approvals: 1 approval from a reviewer who is not the PR author.
- Required checks: all required status checks and all check-runs for the PR head must be successful or neutral.
- Merge method: `squash` (keeps main history tidy).

How to opt-in

1. Add the `automerge` label to your PR (project maintainers or the author can add it).
2. Request at least one reviewer who is not the PR author.
3. After an approval and all checks pass, the repository workflow will attempt to merge the PR automatically.

Opt-out / disabling

- To opt-out for a specific PR: remove the `automerge` label.
- To temporarily disable auto-merge globally: remove or rename the workflow file `.github/workflows/auto-merge.yml` (requires repo write access).

Safety notes

- Auto-merge requires a non-author approval to avoid self-merges without review.
- Branch protection (recommended): require passing status checks and up-to-date branches before merging.
- If you want stricter rules (2+ approvals, label gating, team approvals), update the workflow and this doc accordingly.
