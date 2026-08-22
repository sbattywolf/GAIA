# GAIA Repository Structure Lineage

## Purpose

This report compares the repository-structure documents currently present in
GAIA and records their provisional lineage.

It does not rename, move, delete, or rewrite any structure document.

## Documents under review

- `REPOSITORY_STRUCTURE_v0.3.md`
- `REPOSITORY_STRUCTURE_v0.2.md`
- `reference/REPOSITORY_STRUCTURE_v0.1.md`

## Comparison criteria

Each document must be evaluated against:

1. stated purpose;
2. date and Git history;
3. repository structure described;
4. relationship to the current repository;
5. references from other documents;
6. explicit version/supersession statements;
7. whether it describes current state or a historical snapshot.

## Provisional rule

Filename naming is not sufficient to establish authority.

The canonical repository-structure document should be the document whose
content and provenance best describe the accepted current repository state.

Versioned documents that describe historical states should remain available as
historical evidence unless their removal is explicitly justified.

## Current decision

No canonical document is declared yet.

No document is considered obsolete solely because another document has a higher
version number.

No document should be renamed, moved, archived, or deleted until the three
documents have been compared in full and their inbound references and Git
history have been reviewed.

## Required evidence

The final authority decision should record:

- canonical document;
- historical documents;
- superseded documents, if any;
- unresolved contradictions;
- references that require updating;
- whether a new consolidated document is actually necessary.

## Non-destructive constraint

This report is an analysis artifact.

It must not itself trigger filesystem restructuring.

The repository should preserve historical documentation until its provenance and
value have been established.