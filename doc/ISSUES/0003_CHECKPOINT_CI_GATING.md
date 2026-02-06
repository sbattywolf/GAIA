Title: CI: CHECKPOINT gating — enforce approvals in CI

Summary:
Add a CI job that inspects PRs for `CHECKPOINT` references and requires a matching `CHECKPOINT_<id>.approved` marker before allowing merge. Document the job and test on a feature branch.

Why:
Ensures automated enforcement of human approvals for high-impact changes and prevents accidental merges.

Acceptance criteria:
- CI job defined (GitHub Actions or equivalent) that fails when a PR contains `CHECKPOINT` changes without approved marker.
- Tests demonstrating blocked merge and allowed merge with approval marker present.
- Documentation in `doc/CI/` explaining the mechanism and required markers.

Suggested labels: checkpoint, ci, security

Suggested assignees: ci-team, security-team
