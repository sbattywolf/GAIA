# Document Manifest

## Status

This file is a high-level inventory of important GAIA project documentation.

It is not a complete filesystem manifest and does not define repository
structure authority.

The current repository structure is defined by `REPOSITORY_STRUCTURE.md`.

## Current project documentation

### Root

- `README.md`
- `AGENTS.md`
- `REPOSITORY_STRUCTURE.md`
- `GAIA_ENGINEER_AS_IS_REVIEW.md`
- `REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md`

### Reference

- `reference/`

### Architecture decisions

- `adr/`

### Validation

- `validation/`

### Research and engineering history

- `sprint-01/`
- `sprint-02/`
- `sprint-03/`

### Reports

- `reports/`

### Prototype and benchmark

- `gaia-bootstrap-poc/`

## Historical and provenance material

The repository also contains historical or recovered material that must not be
confused with the current canonical project documentation.

Examples include:

- `REPOSITORY_STRUCTURE_v0.2.md`
- `reference/REPOSITORY_STRUCTURE.md`
- `MANIFEST.txt`
- `oldRepoReferences/`
- reconstruction and audit reports under `reports/`

## Authority

`REPOSITORY_STRUCTURE.md` is the canonical description of the current
repository structure.

`DOCUMENT_MANIFEST.md` is an inventory/navigation aid.

`MANIFEST.txt` is retained as historical/provenance inventory and is not the
canonical document manifest.

## Versioning

Missing historical versions are not reconstructed merely to complete a
filename sequence.

Current documents use Git history as their primary version history unless a
versioned filename has an explicit historical or convergence purpose.

## Maintenance rule

When a new canonical document is introduced, update this manifest if the
document is part of the project's durable documentation set.

Do not attempt to mirror every generated, temporary, benchmark-result, cache,
or runtime artifact here.
