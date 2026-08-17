# GAIA README Navigation Audit

## Status

This audit records navigation and authority mismatches found in the current
`README.md` after repository document-authority consolidation.

This patch does not modify `README.md`.

## Verified findings

### Repository-structure authority

`README.md` currently points readers to:

`reference/REPOSITORY_STRUCTURE.md`

The repository authority decision now establishes the root-level:

`REPOSITORY_STRUCTURE.md`

as the canonical current repository-structure document.

The file under `reference/REPOSITORY_STRUCTURE.md` is explicitly retained as
recovered/reference material and is not the current authority.

### Repository tree

The repository-structure tree embedded in `README.md` is historical/incomplete
relative to the current repository.

The current repository also contains areas such as:

- `AGENTS.md`
- `DOCUMENT_MANIFEST.md`
- `MANIFEST.txt`
- `REPOSITORY_STRUCTURE.md`
- `REPOSITORY_STRUCTURE_v0.2.md`
- `GAIA_ENGINEER_AS_IS_REVIEW.md`
- `REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md`
- `SHA256SUMS.txt`
- `prompts/`
- `reports/`
- `sprint-03/`
- `src/`
- `tests/`
- `gaia-bootstrap-poc/`
- `oldRepoReferences/`

These are already represented by the canonical repository-structure document.

### Sprint navigation

The existing Sprint 1 and Sprint 2 links in `README.md` point to real files.

Sprint 3 also exists and is not currently represented in the README's reading
sequence. Verified Sprint 3 material includes:

- `sprint-03/ARCHITECTURE_CONVERGENCE_REVIEW_v0.1.md`
- `sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md`
- `sprint-03/MEMORY_ROLE_VALIDATION.md`
- `sprint-03/engineer-agent/`

No assumptions are made here about the intended reading order of Sprint 3.

## Decision

Classification:

`navigation-reconciliation-candidate`

The README should be updated in a subsequent patch to:

1. point repository-structure guidance to the canonical root-level
   `REPOSITORY_STRUCTURE.md`;
2. avoid presenting the older embedded repository tree as the authoritative
   current structure;
3. acknowledge `sprint-03/` as part of the repository's engineering/validation
   history;
4. preserve the README's existing project identity and architectural framing.

## Scope boundary

This audit does not authorize:

- deletion of `reference/REPOSITORY_STRUCTURE.md`;
- deletion or renaming of historical Sprint documents;
- rewriting Sprint history;
- changes to architecture or implementation;
- changes to benchmark contracts.

## Rationale

The purpose is to separate repository navigation from historical document
recovery.

The README is a project entry point. The canonical repository-structure
document is the authority for current filesystem organization. Historical
structure documents remain available for provenance but should not compete with
that authority.

## Next step

A subsequent patch can make the minimal README navigation corrections
identified above, without changing GAIA identity, architecture, benchmark
behavior, or historical material.
