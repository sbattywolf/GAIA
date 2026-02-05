# EPC_Telegram — Scoring Reference

Date: 2026-02-04

This file summarizes the Fibonacci-based scoring system applied to `doc/EPC_Telegram.current` and explains how to interpret the `scoring` section found there.

Rules
- Priority weights: `critical=8`, `high=5`, `medium=3`, `low=1`.
- For each story, sum the weights of its tasks, then map that sum to the nearest Fibonacci number in the series: [1,2,3,5,8,13,21,34,55,89].
- The same mapping is applied to compute a feature-level score by summing its story scores and mapping to the nearest Fibonacci number.
- Split threshold: any story or feature with a Fibonacci score > 8 is a candidate to be split into `Part 1` / `Part 2` to make planning and delivery more tractable.

Why this helps
- Fibonacci sizing gives a coarse, well-known scale for relative sizing and helps highlight large stories/features that need decomposition.
- `score_history` entries (present in `doc/EPC_Telegram.current`) provide an audit trail for how a story's size estimate changes over time.

How to re-run the scoring (developer)
1. Inspect task priorities in `doc/EPC_Telegram.current`.
2. Apply the priority weights and compute the sum per story.
3. Map the sum to the nearest Fibonacci number and add an entry into `scoring.stories.<feature>.<story_key>.score_history` with timestamp and reason.
4. Commit the updated `doc/EPC_Telegram.current`.

Split workflow recommendation
- When a story is marked as a `split_candidate`, create two new stories `...:part1` and `...:part2` under the same feature, move a subset of tasks to each part, recompute their scores, and update `score_history` for traceability.
- For large features (`feature_score` > 8), consider splitting the feature into `F-<name>-part1` and `F-<name>-part2` and update the canonical backlog accordingly.

Files updated
- `doc/EPC_Telegram.current` now contains a `scoring` section with per-story and per-feature scores and `score_history` entries (generated: 2026-02-04T00:00:00Z).
- `doc/EPC_Telegram_detail_variants.md` includes a short note linking to the canonical scoring section.

If you want, I can now:
- Split `STR_TestGise` into `STR_TestGise.part1` and `STR_TestGise.part2` with an initial task allocation, or
- Split `F-helper-gise` into two features as flagged by the scoring tool.

Which would you like me to do next?
