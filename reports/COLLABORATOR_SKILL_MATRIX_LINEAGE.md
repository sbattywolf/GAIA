# GAIA Collaborator Skill Matrix Lineage

## Status

`skill-test-matrix.yaml` is retained as historical/reference metadata.

It is not the canonical execution contract for Collaborator benchmark v0.3.

## Origin

The file was introduced by commit `5bb1488`:

`feat: add GAIA collaborator skills benchmark`

At that point the benchmark used a single Home Assistant-oriented test set:

- `C01_intent_recognition`
- `C02_tool_selection`
- `C03_home_assistant_action`
- `C04_invalid_entity`
- `C05_ambiguous_request`
- `C06_multiturn_state`

The same change introduced the corresponding Collaborator skills under
`.github/skills/gaia-collaborator-*`.

## Original responsibility

The matrix mapped each benchmark case to:

- one primary Collaborator skill;
- zero or more secondary skills.

It therefore represented skill coverage and attribution rather than the
complete behavioral evaluation contract.

## Current v0.3 structure

Collaborator v0.3 is organized by domain:

- `domains/home_assistant/`
- `domains/coding/`

Each domain has its own:

- test prompts;
- assertions;
- golden expectations.

The current benchmark contract is defined by these domain artifacts and the
shared evaluator implementation.

The current matrix does not participate in benchmark execution.

## Relationship to current skills

The original skill files remain present under:

`.github/skills/gaia-collaborator-*`

The continued existence of those skills means the historical matrix retains
useful traceability: it records which skills were originally associated with
the first Collaborator benchmark cases.

However, the matrix must not be interpreted as saying that the current v0.3
coding cases have the same skill attribution.

No such mapping has been established by the v0.3 consolidation.

## Decision

Classification:

`historical/reference`

Action:

`retain in place`

Do not:

- rename it to imply that it is the v0.3 contract;
- delete it solely because the runner does not consume it;
- modify its historical mappings to match the newer benchmark;
- use it as evidence that a current domain case tests a particular skill unless
  a new mapping is explicitly established.

## Future option

If GAIA later requires explicit skill-coverage reporting, a new versioned
matrix may be introduced for the current benchmark.

Such a matrix should be derived from the v0.3 domain contracts rather than
silently rewriting this historical file.

## Conclusion

The repository therefore preserves both:

1. the historical skill-oriented Collaborator benchmark lineage;
2. the consolidated domain-oriented v0.3 benchmark.

This is intentional and avoids destroying useful engineering history during
repository consolidation.
