# GAIA Repository Structure Version Lineage Audit

## Status

This audit records the relationship between the current root
`REPOSITORY_STRUCTURE.md` and the older `REPOSITORY_STRUCTURE_v0.2.md`.

It does not rename, delete, move, or rewrite either document.

## Verified files

Both files currently exist at repository root:

- `REPOSITORY_STRUCTURE.md`
- `REPOSITORY_STRUCTURE_v0.2.md`

The current `REPOSITORY_STRUCTURE.md` is the structure authority established
during the repository-consolidation phase.

`REPOSITORY_STRUCTURE_v0.2.md` is an older proposed governance document.

## Historical evidence

`REPOSITORY_STRUCTURE_v0.2.md` identifies itself as:

- Status: Proposed
- Version: 0.2
- Supersedes: `REPOSITORY_STRUCTURE.md`
- Phase: Architecture Convergence
- Last updated: 2026-08-03

It explicitly describes version-suffixed documents as temporary support for
manual convergence and states that, after acceptance and normal Git history,
canonical filenames without version suffixes should normally be restored.

Therefore the existence of both files is explained by the historical
convergence process rather than by two intended current authorities.

## Current authority

The current repository-consolidation decision establishes:

- `REPOSITORY_STRUCTURE.md` — current structure authority;
- `REPOSITORY_STRUCTURE_v0.2.md` — historical/recovered convergence reference.

The older document should not be silently rewritten to describe the current
tree because that would alter historical evidence.

## Classification

| File | Classification | Authority |
|---|---|---|
| `REPOSITORY_STRUCTURE.md` | current governance | current |
| `REPOSITORY_STRUCTURE_v0.2.md` | historical/recovered governance | non-current |

## Decision

Retain both files for now.

Do not:

- delete `REPOSITORY_STRUCTURE_v0.2.md`;
- rename it;
- update its historical content to match the current tree;
- treat it as co-authoritative with `REPOSITORY_STRUCTURE.md`.

The current file and Git history provide the active contract. The v0.2 file
provides provenance for the earlier convergence process.

## Future archival option

A later cleanup PR may move the v0.2 document into an explicit archive
location if the repository's archival policy establishes one.

That move should be separate from this audit because it changes repository
structure and may require reference updates.

Until that policy exists, retaining the file in place is the lowest-risk
choice.

## Consequence

No structural change is justified by this audit.

This closes the version-lineage question for the two repository-structure
documents without destroying historical evidence.
