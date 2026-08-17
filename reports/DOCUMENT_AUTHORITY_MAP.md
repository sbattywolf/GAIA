# GAIA Document Authority Map

## Purpose

This document establishes provisional authority and lineage for document
families that describe repository structure, documentation inventory, and
project next steps.

It does not rename, move, archive, or delete any document.

## Authority rules

A document is treated as authoritative only when repository evidence supports
that role.

Filename order alone is insufficient.

A versioned document may be historical even when it has a higher version
number. An unversioned document may be historical. Provenance and explicit
status take precedence over naming convention.

## Repository structure family

| Document | Provisional status | Reason | Action |
|---|---|---|---|
| `REPOSITORY_STRUCTURE.md` | current-candidate | root-level current structure document | verify against actual repository |
| `REPOSITORY_STRUCTURE_v0.2.md` | historical/convergence | explicitly versioned convergence-era snapshot | retain as historical evidence |
| `reference/REPOSITORY_STRUCTURE.md` | current/reference-candidate | reference-area structure documentation | compare before deciding authority |

Decision:

Do not rename or delete any of these documents until their contents and
references have been compared.

The authoritative structure document should describe the repository that
actually exists after the consolidation work is complete.

## Document manifest family

| Document | Provisional status | Reason | Action |
|---|---|---|---|
| `DOCUMENT_MANIFEST.md` | reconstruction/provenance candidate | documents recovery-package contents and document roles | retain pending provenance review |
| `MANIFEST.txt` | reconstruction/provenance candidate | package/file inventory | retain pending provenance review |

These files should not be treated automatically as the current repository
structure specification.

## Next-steps family

| Document | Provisional status | Reason | Action |
|---|---|---|---|
| `reference/NEXT_STEPS.md` | historical/current-candidate | existing project next-step document | reconcile with current project state |
| `reference/NEXT_STEPS_v0.2.md` | convergence-era snapshot | versioned architecture-convergence roadmap | retain as historical evidence |

The current roadmap must be reconciled with accepted ADRs, Sprint 3,
Bootstrap POC, Collaborator v0.3, and the current Engineer/Home Assistant
workstream before one document is declared authoritative.

## Versioning policy

GAIA does not recreate missing historical versions.

If a historical `v1` file does not exist, the project does not invent one
merely to make the naming sequence look complete.

Future material revisions should use an intentional version when needed, but
the accepted/current document should ultimately have a clearly identifiable
canonical role.

## Required next verification

Before changing any document in the families above:

1. compare full contents;
2. inspect inbound references;
3. inspect Git history;
4. identify explicit supersession statements;
5. compare statements against the actual current repository;
6. record the final authority decision.

## Non-destructive rule

This map is an authority-analysis document only.

No document should be moved, renamed, archived, or deleted based solely on
this provisional classification.
