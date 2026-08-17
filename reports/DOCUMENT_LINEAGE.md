# GAIA Document Lineage

## Purpose

This document records relationships between documents that may represent
different revisions, historical states, parallel drafts, or overlapping
descriptions of the same subject.

It is a lineage map, not an authorization to delete, rename, or archive files.

## Versioning policy

GAIA has evolved incrementally.

Historical documents were not consistently renamed when newer revisions were
created. Therefore:

- a version suffix does not by itself establish authority;
- an unversioned document is not automatically newer;
- historical documents must not be renamed only for naming consistency;
- a document may remain in place because it preserves project history;
- archival or deletion requires explicit evidence and a separate change;
- when lineage is uncertain, the document remains `unknown` rather than being
  silently classified as obsolete.

## Document status

The following statuses are used:

- `current` — current authoritative document for its subject.
- `historical` — retained primarily for project history.
- `reference` — durable reference material.
- `research` — research or analysis material.
- `validation` — validation evidence or architectural testing.
- `proposed` — candidate/future material, not an accepted decision.
- `duplicate-candidate` — appears overlapping and requires comparison.
- `unknown` — lineage or authority has not yet been established.

## Known lineage groups

| Document group | Current assessment | Action |
|---|---|---|
| `REPOSITORY_STRUCTURE.md` / `REPOSITORY_STRUCTURE_v0.2.md` / `reference/REPOSITORY_STRUCTURE.md` | overlapping structure documentation; authority requires verification | compare before any move/rename |
| `GAIA_MODEL.md` / `GAIA_MODEL_v0.2.md` / `reference/GAIA_MODEL.md` | overlapping model documentation; authority requires verification | compare before any move/rename |
| `GLOSSARY.md` / `GLOSSARY_v0.2.md` / `reference/GLOSSARY.md` | overlapping vocabulary documentation; authority requires verification | compare before any move/rename |
| `NEXT_STEPS.md` / `NEXT_STEPS_v0.2.md` / `reference/NEXT_STEPS.md` | overlapping roadmap documentation; authority requires verification | compare before any move/rename |
| `ARCHITECTURE_CONVERGENCE.md` / `ARCHITECTURE_CONVERGENCE_v0.2.md` / `reference/ARCHITECTURE_CONVERGENCE.md` | potentially different architectural snapshots | compare before any move/rename |
| Sprint documents | chronological engineering/research record | retain history; do not normalize retrospectively |
| ADR documents | explicit decision records | preserve individual ADR identity and status |
| Validation documents | evidence and validation record | retain unless explicitly superseded |
| Incubator documents | intentionally unpromoted ideas | retain separately from canonical architecture |

## Important distinction

A document can be superseded as a source of current truth without becoming
obsolete.

For example, a historical architecture document may remain valuable because it
records:

- assumptions;
- alternatives;
- rejected approaches;
- unresolved questions;
- evidence available at that time;
- the reasoning that led to a later decision.

Therefore:

`superseded != obsolete`

and:

`older != disposable`

## Sprint lineage

Sprint directories represent chronological project work.

They should be treated as historical engineering and research records.

They should not be rewritten merely because later reference documents reached
different conclusions.

The current repository README explicitly describes Sprint 1 and Sprint 2 as
historical analytical artefacts whose criticism and alternatives should be
preserved.

## ADR lineage

ADR files represent explicit architectural decisions and their lifecycle.

ADR status must be determined from the ADR itself rather than inferred from
filename ordering.

A proposed ADR must not be treated as an accepted architectural decision.

A superseded ADR should normally remain available as decision history.

## Required verification before consolidation

Before moving, renaming, archiving, or deleting any document in a lineage group,
verify:

1. whether another document explicitly references it;
2. whether it is referenced by the README or repository structure;
3. whether it contains unique information;
4. whether it records historical reasoning;
5. whether a successor explicitly supersedes it;
6. whether the successor is actually authoritative;
7. whether links or scripts depend on its current path.

## Next lineage audit

The next audit should compare the actual contents of each known lineage group
and record:

- predecessor;
- successor;
- current authority;
- unique historical value;
- duplicate sections;
- references to the older document;
- recommended final location;
- confidence.

No file should be moved or deleted as part of this audit.
