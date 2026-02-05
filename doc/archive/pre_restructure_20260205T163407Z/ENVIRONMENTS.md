# Environments: dev and pre-prod

Purpose: define two lightweight GitHub environments for the prototype backlog.

- `dev` — experimental, fast feedback. Developers may push and run integration tests. Use this environment for messy work, feature branches, and rapid iterations.
- `pre-prod` — staging-like environment for integration + full E2E runs. This environment is intended for gated runs and should be used by CI to run more expensive tests.

Recommended setup steps (repo admins):

1. Create environments in the repository settings: `dev` and `pre-prod`.
2. Add secrets scoped to each environment (for example, `PREPROD_TEST_DB_URL`, `PREPROD_API_KEY`) via the Environments UI.
3. Configure required reviewers or protection for `pre-prod` if you want manual approvals before environment use.
4. Use branches to map to environments: push to `dev` (or `backlog/prototype`) to run integration CI; push to `pre-prod` to run E2E.

CI notes:
- Integration workflows should target `dev` and lightweight branches and run fast tests (marker: `not e2e`).
- E2E workflows should target `pre-prod` and set `environment: pre-prod` in the job spec. GitHub will enforce environment protections.

Developer workflow:
- For rapid iteration:

```bash
git checkout -b feat/xyz
git push origin feat/xyz
# Open PR against `dev` (or `backlog/prototype`) to trigger integration CI
```

- For staging/E2E validation:

```bash
# Merge to `pre-prod` or create a PR targeting `pre-prod`
git push origin pre-prod
```

Keep environment secrets out of the repository and rotate them if leaked.
