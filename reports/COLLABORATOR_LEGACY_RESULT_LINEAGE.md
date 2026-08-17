# GAIA Collaborator Legacy Result Lineage

## Status

This report closes the remaining item identified by the Collaborator runtime
artifact audit: the legacy top-level result file

`gaia-bootstrap-poc/benchmark/collaborator/results/devstral-small-2-24b.json`

The current benchmark results directory is runtime output and is excluded by
the repository's `.gitignore`.

This report does not delete or relocate runtime files.

## Verified Git history

The legacy result file appears in Git history associated with these benchmark
consolidation commits:

- `c1e1d8f` — `refactor: structure collaborator benchmark v2`
- `388e29b` — `refactor: consolidate collaborator evaluation core`

The file is not currently tracked in the working tree.

No current repository references to the legacy result filename were found.

## Current benchmark authority

The current Collaborator benchmark uses:

- `gaia-bootstrap-poc/benchmark/collaborator/domains/coding/`
- `gaia-bootstrap-poc/benchmark/collaborator/domains/home_assistant/`
- shared evaluator code under `core/`
- committed baseline documentation under
  `gaia-bootstrap-poc/benchmark/collaborator/reports/`

Individual runtime result JSON files are not part of the durable benchmark
contract.

The v0.3 baseline report is the durable summary of the diagnostic baseline.

## Classification

The legacy result is classified as:

`historical/generated evaluation artifact`

It is not:

- a current benchmark contract;
- a golden expectation;
- an active input to the runner;
- a required source file;
- a canonical performance record.

## Decision

No repository cleanup action is required.

Because the artifact is not currently tracked and is covered by the existing
runtime-results ignore rule, it should remain outside the committed repository
state.

Its historical existence is preserved by Git history and by this lineage
record. Reintroducing the JSON as a committed file would duplicate runtime
output without improving reproducibility.

## Boundary

This decision does not authorize deletion of arbitrary files from a developer's
local workspace.

It only establishes that the legacy result must not be restored to the
canonical repository tree during consolidation.

## Collaborator artifact cleanup status

The previously identified Collaborator artifacts now have explicit treatment:

| Artifact | Decision |
|---|---|
| Python `__pycache__` | generated/local, ignored |
| benchmark `results/` JSON | generated/local, ignored |
| empty `golden/README.md` | removed after history/reference verification |
| `skill-test-matrix.yaml` | historical/reference, retained |
| legacy top-level result JSON | historical/generated, not restored |

## Conclusion

The Collaborator runtime-artifact audit is now complete at the repository
consolidation level.

No further Collaborator artifact removal is justified by the current evidence.
Future benchmark redesign may create new cleanup decisions, but those should
be handled independently from this repository-consolidation PR.
