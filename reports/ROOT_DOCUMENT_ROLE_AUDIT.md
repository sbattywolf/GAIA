# GAIA Root Document Role Audit

## Purpose

This audit closes the remaining root-level documentation role questions after
the repository-consolidation and provenance phases.

It is intentionally non-destructive.

No root document is renamed, moved, deleted, or rewritten by this audit.

## Current root documents

The verified root-level documentation set includes:

- `README.md`
- `AGENTS.md`
- `DOCUMENT_MANIFEST.md`
- `MANIFEST.txt`
- `GAIA_ENGINEER_AS_IS_REVIEW.md`
- `REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md`
- `REPOSITORY_STRUCTURE.md`
- `REPOSITORY_STRUCTURE_v0.2.md`
- `SHA256SUMS.txt`

These files do not have interchangeable responsibilities.

## Role classification

| Artifact | Role | Current authority |
|---|---|---|
| `README.md` | project entry point and navigation | current |
| `AGENTS.md` | repository-level operating instructions | current |
| `DOCUMENT_MANIFEST.md` | documentation inventory and provenance notes | current |
| `MANIFEST.txt` | historical/provenance inventory | historical |
| `REPOSITORY_STRUCTURE.md` | repository structure authority | current |
| `REPOSITORY_STRUCTURE_v0.2.md` | previous convergence proposal | historical |
| `GAIA_ENGINEER_AS_IS_REVIEW.md` | engineering state/review report | contextual evidence |
| `REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md` | domain-boundary design/reference material | design reference |
| `SHA256SUMS.txt` | checksum/provenance snapshot | historical integrity evidence |

## Important distinction

The existence of multiple root documents is not itself duplication.

The repository currently contains documents serving different classes of
truth:

1. current project/navigation truth;
2. current governance/instruction truth;
3. historical research and convergence evidence;
4. contextual engineering/design evidence;
5. integrity/provenance snapshots.

Removing a document merely because another document also mentions the same
topic would destroy traceability.

## Documents requiring no cleanup

The following should remain at root for now:

- `README.md`
- `AGENTS.md`
- `DOCUMENT_MANIFEST.md`
- `REPOSITORY_STRUCTURE.md`

Their roles are active and distinct.

## Historical documents

`MANIFEST.txt` and `REPOSITORY_STRUCTURE_v0.2.md` should remain preserved.

Their historical status is already documented by the repository-consolidation
work. They should not be silently converted into current documents.

A future archival policy may relocate them, but that is a separate structural
change.

## Contextual engineering documents

`GAIA_ENGINEER_AS_IS_REVIEW.md` and
`REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md` remain useful evidence/reference
documents.

The current audit does not establish sufficient evidence to move either file
without first checking all inbound references and deciding whether a dedicated
architecture/design documentation area is intended.

Therefore both are classified:

`retain pending dedicated-document-area decision`

## Cleanup boundary

No deletion candidate is established by this audit.

No relocation candidate is sufficiently verified to justify an immediate move.

The correct next action is therefore not cleanup, but closure of the
classification phase.

## Repository-consolidation conclusion

The repository now has an explicit role for each verified root-level
documentation artifact.

The remaining question is organizational preference rather than unresolved
provenance:

> whether contextual engineering/design documents should eventually live
> outside the repository root.

That decision should be made only if GAIA establishes a durable location and
reference policy for such documents.

Until then, preservation in place is the least destructive option.

## Decision

Classification of this audit:

`repository documentation role closure`

Action:

`retain all verified root documents in place`

No filesystem restructuring is authorized by this document.
