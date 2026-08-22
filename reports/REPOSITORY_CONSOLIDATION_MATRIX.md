# GAIA Repository Consolidation Matrix

## Purpose

This document is the working inventory for repository consolidation.

It distinguishes current/canonical material from historical, research,
validation, generated, experimental, and consolidation candidates before
any files are moved, renamed, archived, or deleted.

This is an inventory and decision aid. It does not itself authorize
destructive repository changes.

## Status vocabulary

- **canonical** — current authoritative project material.
- **historical** — retained because it records project history or evolution.
- **reference** — durable conceptual or architectural reference material.
- **validation** — material used to validate architectural or behavioral claims.
- **research** — exploratory/research material.
- **engineering** — implementation, prototype, benchmark, or operational material.
- **incubator** — ideas intentionally not promoted to the core architecture.
- **generated** — generated/runtime/output material that should normally not be
  treated as source documentation.
- **candidate-archive** — likely obsolete or superseded material requiring
  explicit verification before moving.
- **unknown** — insufficient evidence; do not change.

## Versioning rule

GAIA has used incremental evolution rather than consistently renaming
documents for every revision.

The existence of a `v0.x`, `v1`, or `v2` suffix must therefore not by itself
determine which document is authoritative.

Where a newer version exists, the relationship between versions must be
verified before archival or removal.

Historical documents should normally remain available when they preserve
decision history, criticism, research, or architectural evolution.

## Current top-level structure

| Area | Current role | Initial disposition |
|---|---|---|
| `adr/` | Architectural decisions and candidates | retain |
| `reference/` | Durable GAIA conceptual/reference material | retain |
| `validation/` | Architectural and boundary validation | retain |
| `reports/` | Reports, reconstruction, source/control material | retain; consolidate internally |
| `sprint-01/` | Historical engineering/research record | retain as history |
| `sprint-02/` | Historical engineering/research record | retain as history |
| `sprint-03/` | Historical validation/research record | retain as history |
| `incubator/` | Unpromoted ideas and experiments | retain |
| `prompts/` | Working prompts/research-session material | review |
| `src/` | Source/runtime area | retain |
| `gaia-bootstrap-poc/` | Prototype/benchmark implementation | retain |
| `.github/` | Repository tooling/instructions | retain |

## Known consolidation concerns

### Documentation duplication

The repository contains multiple documents with similar or versioned names,
including architecture, world-model, glossary, next-step, and repository
structure material.

These must be classified by role and lineage before any deletion or rename.

### Repository structure documents

The repository contains multiple structure descriptions, including:

- `REPOSITORY_STRUCTURE_v0.3.md`
- `REPOSITORY_STRUCTURE_v0.2.md`
- `reference/REPOSITORY_STRUCTURE_v0.1.md`

They must not be treated as duplicates solely from their names.

Their authority and historical role must be verified before consolidation.

### Versioned reference documents

Several areas contain both unversioned and versioned documents.

The current policy is:

1. do not rename the existing historical document merely to introduce a
   version suffix;
2. use a new versioned document when a materially new revision is required;
3. preserve historical versions when they document project evolution;
4. explicitly identify the authoritative/current document.

### Sprint material

Sprint directories are part of the engineering history.

They should not be flattened into the current reference documentation merely
to reduce file count.

Their role is to preserve what was researched, tested, discussed, and decided
at different stages of the project.

### Root-level clutter

The repository has previously accumulated temporary scripts, generated
artifacts, patch scripts, model/runtime artifacts, and other working files at
the root.

These are consolidation candidates, but no root-level file should be deleted
or moved solely because its location appears undesirable.

Each candidate requires classification and, where relevant, verification of
whether it is referenced by current tooling or documentation.

## Proposed next consolidation passes

### Pass 1 — inventory

Identify all root-level files and directories and classify them using the
status vocabulary above.

### Pass 2 — document lineage

For similarly named or versioned documents, record:

- current authority;
- predecessor/successor relationship;
- historical value;
- duplicate status;
- proposed final location.

### Pass 3 — generated and temporary artifacts

Identify generated outputs, temporary patch scripts, local model artifacts,
benchmark results, archives, and other non-source material.

Determine whether each belongs in:

- Git-tracked source;
- a dedicated artifact directory;
- an archive;
- `.gitignore`;
- removal.

### Pass 4 — structural cleanup

Only after the previous passes are reviewed:

- move files where the destination is clear;
- archive historical material where appropriate;
- remove confirmed obsolete artifacts;
- update references and documentation.

## Non-destructive rule

This matrix does not authorize deletion, renaming, or movement.

Any destructive or structural change should be a separate commit with a
specific rationale and an independently reviewable diff.

## Open questions

1. Which document is authoritative when multiple versions coexist?
2. Which root-level scripts are still required?
3. Which generated/runtime artifacts should be ignored rather than tracked?
4. Which historical documents should remain in place for traceability?
5. Which historical documents can safely move to an archive?
6. Is the current `reports/` structure coherent enough, or should reports be
   separated by purpose?

## Confidence

This is a consolidation working document, not a final repository policy.

Items whose lineage or authority has not yet been verified remain intentionally
unresolved.
