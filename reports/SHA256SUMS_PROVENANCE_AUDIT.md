# GAIA SHA256SUMS Provenance Audit

## Status

This audit evaluates the root `SHA256SUMS.txt` after repository consolidation.

It does not regenerate the checksum file and does not authorize deleting or
replacing it.

## Verified role

`SHA256SUMS.txt` is a repository-level integrity/provenance artifact.

It contains hashes for a snapshot of project files, including architecture
documents, reference material, diagrams, prompts, and reports.

It is therefore different from:

- `DOCUMENT_MANIFEST.md`, which is a documentation inventory;
- `REPOSITORY_STRUCTURE.md`, which defines current repository structure;
- Git history, which is the primary version history for current documents.

## Evidence of snapshot semantics

The checksum file contains entries for historical/recovered material such as:

- `reference/REPOSITORY_STRUCTURE.md`
- reconstruction reports under `reports/`
- prior non-approved output under `reports/prior-nonapproved-output/`

It also contains hashes for project material that may evolve independently
through Git.

The file itself therefore represents a checksum snapshot, not a continuously
maintained filesystem authority.

## Current authority relationship

`REPOSITORY_STRUCTURE.md` explicitly defines Git history as the primary version
history for current documents and treats historical/recovered structure
documents separately.

`DOCUMENT_MANIFEST.md` explicitly identifies `MANIFEST.txt` as historical/
provenance inventory and does not assign `SHA256SUMS.txt` a documentation
authority role.

No evidence was found that the current benchmark or repository tooling uses
`SHA256SUMS.txt` as an execution input.

## Classification

`provenance/integrity artifact`

Secondary classification:

`historical snapshot`

## Decision

Retain `SHA256SUMS.txt` in place.

Do not:

- regenerate it automatically during repository consolidation;
- treat it as a current manifest;
- use it to decide which files are canonical;
- delete it merely because its snapshot is older than the current tree.

If GAIA later requires a reproducible integrity mechanism, that should be
designed explicitly and documented separately.

## Important distinction

A stale checksum snapshot is not necessarily an invalid artifact.

Its value is provenance: it records what was hashed at the time it was
generated.

Replacing it with freshly generated hashes would destroy that historical
meaning unless the old snapshot were preserved separately.

## Consolidation consequence

No filesystem change is justified by this audit.

The repository can retain:

1. `SHA256SUMS.txt` as historical integrity evidence;
2. Git as the primary version history;
3. `DOCUMENT_MANIFEST.md` as documentation inventory;
4. `REPOSITORY_STRUCTURE.md` as current structure authority.

## Next decision gate

The repository-consolidation phase should not regenerate or reorganize
checksum/provenance material unless a specific future requirement establishes:

- what is being attested;
- when checksums are generated;
- which files are in scope;
- where the authoritative checksum record lives;
- how updates and historical snapshots are preserved.

Until then, preservation is the lowest-risk and most traceable choice.
