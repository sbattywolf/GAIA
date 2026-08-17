# GAIA Collaborator v0.3 — Baseline Report

## Status

The Collaborator benchmark v0.3 golden evaluation is consolidated on `main`.

Official metric:

- `golden_score`

The legacy `score` remains available only for regression comparison.

## Scope

Domains:

- `coding`
- `home_assistant`

Models evaluated:

- `qwen2.5-coder-14b`
- `qwen3-coder-30b`
- `devstral-24b`
- `devstral-small-2-24b`
- `gpt-oss-20b`
- `gemma4-26b`

Each domain contains six behavioral cases.

## Consolidation notes

The benchmark went through several oracle/verifier audits before being frozen.

Important final decisions:

- C02 file/tool selection is treated as a stable contract.
- C06 multiturn context explicitly separates the current activity target from the preserved previous component.
- C06 `execution_claim` is a boolean and is expected to be `false` for the benchmark scenario.
- C03 explicitly requires `operation` to be exactly `plan`.
- C01 retains explicit semantic evidence for the requested 30-second timeout and read-only behavior.
- C05 retains strict execution-status semantics and does not accept arbitrary descriptive labels as equivalent to the canonical operation.

The benchmark was not tuned to maximize any individual model's score.

## Latest diagnostic baseline before final contract consolidation

The last six-model coding diagnostic run produced:

| Model | Coding golden |
|---|---:|
| devstral-small-2-24b | 83.3% |
| qwen2.5-coder-14b | 83.3% |
| devstral-24b | 66.7% |
| gemma4-26b | 66.7% |
| gpt-oss-20b | 66.7% |
| qwen3-coder-30b | 33.3% |

This run was diagnostic. The final C03/C06 contract correction was committed afterward, so these values must not be presented as a formally reproducible post-freeze matrix.

## Known limitations

The benchmark measures structured collaborator behavior through a small fixed scenario set. It is not a general coding-agent benchmark and should not be interpreted as one.

Known sensitivity areas include:

- exact semantic representation of requested changes;
- explicit preservation of read-only constraints;
- operation naming;
- ambiguity handling;
- multiturn context preservation;
- claims about external execution or test results.

Future benchmark changes should be treated as versioned benchmark changes rather than incremental tuning of the current oracle.

## Freeze rule

After this baseline is committed:

1. Do not modify the current cases merely to improve model scores.
2. New cases or semantic changes require a new benchmark version.
3. Verifier/scoring changes require an explicit benchmark audit.
4. Runtime result JSON files remain generated artifacts and should not be treated as source-of-truth benchmark definitions.

## Next phase

The Collaborator benchmark moves to maintenance/frozen state.

GAIA work can proceed to:

1. repository/documentation consolidation;
2. Engineer/Codex work;
3. first real Home Assistant/domain collaborator implementation.

These tracks can be developed in parallel where their interfaces are already stable.
