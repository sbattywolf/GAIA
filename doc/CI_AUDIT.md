# CI Audit — Recent Failures

Date: 2026-02-04

Summary

- Multiple recent workflow runs failed (see Actions runs). Common symptoms:
  - Many tests abort at collection with `ModuleNotFoundError: No module named 'agents'` or `No module named 'scripts'` and `No module named 'orchestrator'`.
  - A `fatal: No url found for submodule path 'external/openclaw' in .gitmodules` appeared during post-job cleanup.

Root causes (likely)

1. Tests run without the repository root on `PYTHONPATH` (so local packages `agents`, `scripts`, `orchestrator` are not importable).
2. Checkout/submodule issues: `.gitmodules` references `external/openclaw` with an invalid or missing URL, causing checkout/post-job failures.
3. Workflow duplication in `.github/workflows/ci.yml` increases maintenance risk and may lead to inconsistent job behavior.

Immediate fixes applied

- `.github/workflows/ci.yml`: added `env: PYTHONPATH: '.'` at the job level and configured `actions/checkout@v4` to use `fetch-depth: 0` and `submodules: false` so the runner sees the repository root and avoids failing on the broken submodule.

Recommended next steps

1. Stabilize imports in CI
   - Ensure all CI workflows that run tests set `PYTHONPATH='.'` or run `python -m pytest` from the repo root.
   - Alternatively, install the package in editable mode (`pip install -e .`) before running tests so imports resolve consistently.

2. Fix submodule config
   - Inspect `.gitmodules` and either provide a valid `url` for `external/openclaw` or remove the submodule if it's not required.
   - For the short term, keep `submodules: false` in checkout steps to avoid failures until `.gitmodules` is fixed.

3. Audit workflows
   - Remove duplicate/overlapping workflow definitions in `.github/workflows/ci.yml` to keep a single clear CI pipeline.
   - Add caching and OS-matrix pruning to reduce CI runtime.

4. Incremental CI cleanup plan
   - Run a single CI workflow on `master` after fixes to confirm green state.
   - Clean up stale branches and old workflow runs once CI is green.

5. Longer term (multi-agent design)
   - Define agent responsibilities and permissions (documented in `doc/MULTI_AGENT_ARCHITECTURE.md`).
   - Use protected `production` environment for any workflow that sends external messages; require manual approvals.
   - Consider a GitHub App or dedicated bot account for higher-privilege automation (issue creation, backfills).

If you want, I can:
- Open a PR with the CI fixes (I already pushed workflow files earlier).
- Inspect and patch `.gitmodules` or remove the problematic submodule.
- Produce `doc/MULTI_AGENT_ARCHITECTURE.md` draft (phase plan + permissions model).

