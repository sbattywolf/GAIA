# GAIA Document Authority Decision

## Status

Accepted for repository consolidation.

This document records the authority decision resulting from the repository
documentation reconciliation.

## Repository structure

### Current canonical document

`REPOSITORY_STRUCTURE.md`

Reason:

- it is located at repository root;
- it has the explicit role of repository structure documentation;
- it is aligned with the actual repository areas;
- Git provides its primary revision history.

### Historical convergence document

`REPOSITORY_STRUCTURE_v0.2.md`

Classification:

`historical / superseded`

It remains valuable because it records the Architecture Convergence model and
the temporary versioning strategy used during that period.

It must not be treated as the current repository structure contract.

### Recovered reference document

`reference/REPOSITORY_STRUCTURE.md`

Classification:

`recovered / reference`

It preserves recovered repository-structure material and its provenance.

It is not the current repository structure authority.

## Manifest documents

### `DOCUMENT_MANIFEST.md`

Classification:

`current documentation inventory`

It provides a high-level navigation and documentation inventory.

It does not define repository structure.

### `MANIFEST.txt`

Classification:

`historical / provenance inventory`

It is retained because it records a broader recovery/package inventory.

It is not maintained as the canonical current manifest.

## Versioning decision

GAIA does not attempt to reconstruct missing historical versions.

The previous convergence-era `v0.2` structure document remains because it
exists and has historical value.

The current repository structure is represented by the unversioned canonical
filename:

`REPOSITORY_STRUCTURE.md`

Future substantial changes should normally be represented through Git
history unless a versioned document provides clear historical or convergence
value.

## Archive decision

No structure or manifest document is archived or deleted by this decision.

Archival can be considered later for material whose historical value is
understood and whose removal from the active tree improves discoverability
without destroying provenance.

## Result

The repository now has an explicit authority hierarchy:

1. `REPOSITORY_STRUCTURE.md` — current repository structure
2. `DOCUMENT_MANIFEST.md` — current documentation inventory
3. `MANIFEST.txt` — historical/provenance inventory
4. `REPOSITORY_STRUCTURE_v0.2.md` — historical convergence record
5. `reference/REPOSITORY_STRUCTURE.md` — recovered reference material

This hierarchy prevents historical recovery material and convergence snapshots
from competing with the current repository contract.
