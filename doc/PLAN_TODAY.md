# Plan for Today — short, actionable

Goal: unblock artifact collection and make progress on highest-impact engineering tasks.

Top 6 actions (today)
1. Fix dispatch/push auth and re-run repro workflow smoke run
   - If necessary run `gh auth login` and re-push `chore/smoke-artifact-test` or open PR to `master` and dispatch there.
   - Validate artifacts downloaded and assert presence of `flake-logs/test-ok.txt`.

2. Add quick CI log step (if smoke fails again)
   - Patch workflow to `dir`-list `flake-logs` right before `actions/upload-artifact` and commit.

3. Start Controller API scaffold (small PR)
   - Implement 3 endpoints: `GET /api/controller/active`, `POST /api/controller/claim`, `POST /api/controller/complete`.
   - Add minimal unit test for claim/complete flows using `--simulate` mode.

4. Scaffold `scripts/alby_agent.py` dry-run and run one dry-run for `F-helper-gise-part1`.
   - Save outputs to `.tmp/merged_candidates/` and capture timings.

5. Create `doc/MASTER_DOC_INDEX.md` auto-generator script (simple Python) and run it.
   - Commit generated index so maintainers have a single entry point.

6. Sync with you / send status and next 2-day plan in Kanban items.

How I'll report progress
- After steps 1–2: confirm smoke artifact presence or attach run logs and a small PR with the CI listing step.
- After step 3: open PR with Controller API scaffold and tests.

If you prefer a different priority, tell me which of the top 3 to push first.
