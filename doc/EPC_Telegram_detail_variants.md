# EPC_Telegram — STR_TestGise: Detailed Variants

Date: 2026-02-03

This document provides two concrete implementation/workflow variants for the `STR_TestGise` story:
- "With Gise": assume the `Gise` agent handles claim/merge automation and some validation steps.
- "Without Gise": assume maintainers perform claim/merge/validation manually; automation is minimal.

File note: canonical epic remains at [doc/EPC_Telegram.current](doc/EPC_Telegram.current). This variants document is a decision aid for planning and sprint scoping.

---

**Variant A — With Gise (agent-assisted)**

Summary
- Gise performs most of the repetitive merge/claim work: runs validation, archives drafts, creates audit traces in `gaia.db`, and can optionally post progress to Telegram.
- Maintainer responsibilities: review merged content, approve exceptions, and resolve merge conflicts the agent can't fix.

Key tasks (step-by-step)
1. Implement agent entrypoint for STR_TestGise: `scripts/alby_agent.py` extension to detect `.tmp/todolists/EPC_Telegram.current.STR_TestGise.*` and prepare merge candidate. (est. 0.5 dev-days)
2. Add idempotent merge routine: read draft, validate with `scripts/validate_todolists.py`, snapshot to `doc/archive/` with `scripts/version_docs.py`, then `git add`/commit or emit merge artifact for maintainer. (est. 1.0 dev-days)
3. Add automatic audit trace write to `gaia.db` for each merged draft (timestamp, source agent, trace_id). (est. 0.5 dev-days)
4. Add conflict detection + safe abort + human-in-loop flagging (if auto-merge fails). (est. 0.5 dev-days)
5. Tests and e2e: unit tests + a dry-run harness that runs `scripts/alby_agent.py --dry-run`. (est. 0.5 dev-days)

Acceptance criteria
- Agent can process the STR_TestGise drafts and produce a mergeable candidate without human edits in at least 80% of cases.
- All merges create an audit record in `gaia.db` with `trace_id` and source file path.
- If validation fails or a conflict is detected, the agent leaves a clear human-actionable report in `.tmp/merged_reports/` and does not modify `doc/EPC_Telegram.current`.

Estimate (total): 3.0 dev-days (conservative)

Risks & notes
- Windows file RMW semantics: ensure atomic write pattern (temp+fsync+os.replace) to avoid partial writes.
- Agent quality depends on validation coverage; invest in `scripts/validate_todolists.py` tests first.

---

**Variant B — Without Gise (maintainer-driven)**

Summary
- No agent automation for merging. Maintainers run validation, versioning and merges manually via existing scripts and a simple checklist.

Key tasks (step-by-step)
1. Add a short maintainer checklist in `doc/EPC_Telegram.current` and/or `doc/MAINTAINER.md` describing the manual merge steps (validate, archive, merge, commit, write audit). (est. 0.25 dev-days)
2. Ensure `scripts/validate_todolists.py` is accessible and robust; add any missing schema tests. (est. 0.5 dev-days)
3. Add a small helper script `scripts/manual_merge_helper.py` that runs validation, prompts for confirm, archives drafts, and prints the `git` commands to run (no automatic commit). (est. 0.75 dev-days)
4. Tests: add short unit tests for the helper script and run the validator on the current `.tmp/todolists` set. (est. 0.25 dev-days)

Acceptance criteria
- Maintainers can follow the checklist and merge drafts without ambiguity.
- Validator returns zero errors before any merge; helper script reduces manual steps and records recommended audit metadata (printed for manual insertion into `gaia.db`).

Estimate (total): 1.75 dev-days (conservative)

Risks & notes
- Manual merges scale poorly if many agents produce drafts frequently.
- Human error risk for missed archival steps — enforce checklist and spot audits.

---

**Decision guidance**

- Choose "With Gise" when you expect frequent agent-produced drafts and want to minimize maintainer time; invest in test coverage and safe-guards first.
- Choose "Without Gise" for low-frequency drafts or when you need strict human control over merges and audit insertion.

**File**: [doc/EPC_Telegram_detail_variants.md](doc/EPC_Telegram_detail_variants.md)

---

If you'd like, I can also:
- Convert these steps into concrete `tNN` tasks and insert them into `doc/EPC_Telegram.current` under `STR_TestGise` (with and/or without `AgentGise` tags), or
- Open a PR that adds the variants doc and the report pointer.

---

**Scoring note**

This repository now uses a Fibonacci-based sizing heuristic stored in `doc/EPC_Telegram.current` under the `scoring` section. Stories or features with a score above `8` are candidates to be split; `STR_TestGise` is currently marked as a split candidate (score `34`). See `doc/EPC_Telegram.current` for the per-story and per-feature `score` and `score_history` entries.

---

**Detailed human summaries (appendix)**

Below are human-readable summaries for the newly split `F-helper-gise` features and the `STR_TestGise` story parts. These are intended to help reviewers and maintainers quickly understand scope and acceptance criteria.

- `F-helper-gise-part1` — Helper Gise: Foundation
	- Purpose: discover ALby artifacts, design the local agent architecture, and scaffold safe CLI entrypoints.
	- Acceptance: a short design doc, a scanned list of ALby examples, and a scaffolded `scripts/alby_agent.py` with `--dry-run` behavior.

- `F-helper-gise-part2` — Helper Gise: Prototype & Acceptance
	- Purpose: run the prototype (dry-run and live), collect timing signals, and execute STR_TestGise acceptance scenarios.
	- Acceptance: archive snapshots created, merge candidates produced, and audit traces written to `gaia.db` during live runs.

- `STR_TestGise.part1`
	- Purpose: validate agent environment and provide helper utilities (chat export, extra logging).
	- Acceptance: environment smoke test passes, helper scripts present in `.tmp/exports`, and debug logging toggles.

- `STR_TestGise.part2`
	- Purpose: full acceptance run and governance closure.
	- Acceptance: end-to-end acceptance flow completes, gaia.db timestamped records are present, and `t_final` verification steps complete.

These summaries are appended here for convenience; the canonical `doc/EPC_Telegram.current` contains the task-level summaries and `moved_from` metadata for traceability.

