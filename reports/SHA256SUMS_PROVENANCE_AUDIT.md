# GAIA SHA256 Provenance Artifact Audit

## Status

This document audits the provenance role of the root `SHA256SUMS.txt`.

No checksum file is regenerated or rewritten by this audit.

## Verified provenance

`SHA256SUMS.txt` is a tracked root-level artifact containing SHA-256 entries
for a finite set of repository files.

The current file records hashes for examples including:

- `README.md`;
- ADR files;
- selected reference documents;
- selected reports.

It is therefore a checksum manifest, not a complete inventory of every
current repository artifact.

## Git history

The available Git history shows `SHA256SUMS.txt` was present in the imported
repository state at commit `d9e8e91`:

`chore: import current GAIA state from Copilot`

The file also exists in the earlier `9805a86` documentation history.

This establishes that the checksum manifest predates the repository
consolidation work performed in the current phase.

## Current limitation

Subsequent repository changes introduced or modified many documents.

The checksum manifest has not been demonstrated to cover all of those newer
artifacts.

Therefore the manifest must not be interpreted as:

- a complete repository inventory;
- proof that every current file has a recorded checksum;
- proof that every recorded checksum corresponds to the current content;
- a replacement for Git history.

## Classification

`provenance/integrity artifact`

Authority:

`historical provenance evidence`

Operational role:

`non-authoritative checksum manifest`

## Decision

Retain `SHA256SUMS.txt` in place.

Do not silently regenerate it as part of repository consolidation.

Do not delete it merely because it is incomplete.

If GAIA later needs an authoritative integrity mechanism, define that mechanism
explicitly and create a separate change for adoption.

A future integrity mechanism may generate a new checksum manifest from a
specified canonical file set, but that should be a deliberate reproducible
process rather than an implicit cleanup step.

## Conclusion

`SHA256SUMS.txt` has legitimate provenance value, but its scope is limited.

The safe interpretation is:

> historical checksum evidence for a defined subset of the repository.

It should remain preserved without being treated as a complete current-state
integrity guarantee.
