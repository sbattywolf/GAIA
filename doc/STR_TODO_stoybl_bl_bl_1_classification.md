**STR_TODO_stoybl_bl_bl_1_classification**

Purpose
- Execute `t2`: normalize TODO classification across the story to improve discoverability, triage, and prioritization.

Acceptance criteria
- All tasks in `.tmp/todolists/...current` have a `classification` array and `impact` field where applicable.
- `doc/AGENT_BEST_PRACTICES.md` includes an explicit mapping of classifications used (e.g., `test`, `cli-ui`, `runbook`, `governance`, `documentation`, `concurrency`).

Implementation
1. Audit existing task entries and add `classification` and `impact` where missing.
2. Add a short section to `doc/AGENT_BEST_PRACTICES.md` listing canonical classifications and examples.
3. Update automation that generates STR files to emit `classification` metadata.

Tests / validation
- Run a quick script to validate JSON schema for all `.tmp/todolists/*.current` files and report missing fields.
