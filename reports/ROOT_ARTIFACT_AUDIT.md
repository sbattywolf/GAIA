# GAIA Root Artifact Audit

## Purpose

This document audits files and directories located at the repository root that
may be implementation artifacts, historical imports, generated outputs,
temporary patch scripts, local runtime artifacts, or legitimate project
documentation.

This audit does not authorize deletion, movement, renaming, or archival.

## Decision vocabulary

- `retain-root` — legitimate root-level project material.
- `retain-in-place` — historical or structural material that should remain where
  it is for now.
- `relocate-candidate` — likely belongs in a dedicated directory but requires
  dependency/reference verification.
- `archive-candidate` — historical or obsolete candidate requiring explicit
  verification.
- `generated-candidate` — generated/runtime output that should normally not be
  versioned.
- `gitignore-candidate` — local/generated artifact that should normally be
  ignored.
- `unknown` — insufficient evidence; do not change.

## Root documentation and governance

| Artifact | Initial classification | Proposed action |
|---|---|---|
| `README.md` | retain-root | canonical repository entry point |
| `AGENTS.md` | retain-root | repository-level agent/development instructions |
| `DOCUMENT_MANIFEST.md` | retain-root | retain pending documentation reconciliation |
| `MANIFEST.txt` | retain-root | retain pending provenance/manifest reconciliation |
| `REPOSITORY_STRUCTURE.md` | duplicate-candidate | reconcile lineage before changing |
| `REPOSITORY_STRUCTURE_v0.2.md` | historical/reference candidate | compare with current structure documents |
| `GAIA_ENGINEER_AS_IS_REVIEW.md` | report/review | retain until lineage and relevance are verified |
| `REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md` | design/reference candidate | retain; assess final ownership later |
| `SHA256SUMS.txt` | provenance/integrity artifact | retain unless superseded by a verified mechanism |

## Root directories

| Directory | Initial classification | Proposed action |
|---|---|---|
| `adr/` | retain-in-place | architectural decision history |
| `reference/` | retain-in-place | durable conceptual/reference material |
| `validation/` | retain-in-place | validation evidence |
| `reports/` | retain-in-place | reports and consolidation artefacts |
| `sprint-01/` | retain-in-place | historical engineering/research record |
| `sprint-02/` | retain-in-place | historical engineering/research record |
| `sprint-03/` | retain-in-place | historical engineering/research record |
| `incubator/` | retain-in-place | unpromoted ideas |
| `prompts/` | review | determine whether prompts are historical, active, or generated |
| `src/` | retain-in-place | source/runtime area |
| `gaia-bootstrap-poc/` | retain-in-place | prototype and benchmark implementation |
| `.github/` | retain-root | repository automation/instructions |

## Root Python implementation files

Previously observed root-level files include:

```text
runner.py
schemas.py
scoring.py
verifier.py

## Root patch scripts

Previously observed files include:

- `patch_*.py`

Initial classification:

`archive-candidate`

These scripts document the incremental engineering process used to evolve the
Collaborator benchmark.

They should not automatically be deleted merely because their changes are now
consolidated.

Before deciding their final location, verify:

- whether they are referenced by current documentation;
- whether they are reproducible historical evidence;
- whether their changes are completely represented in Git history;
- whether keeping them as standalone files provides value beyond Git history.

Potential future destination:

`reports/archive/patches/`

This location is deliberately not created by this audit.

## ZIP and packaged artifacts

Previously observed archives include:

- `gaia-collaborator-finalize-v1.zip`
- `gaia-collaborator-oracle-audit-v*.zip`
- other benchmark/package archives

Initial classification:

`archive-candidate` / `generated-candidate`

Each archive must be checked individually.

A ZIP should not be retained merely because it was once used to transfer a
patch if the same content is already represented in Git history.

Before removal verify:

1. whether it contains material absent from Git;
2. whether it is referenced by documentation;
3. whether it is required as an external release artifact;
4. whether its checksums or provenance are recorded elsewhere.

## Local model/runtime artifacts

Previously observed root-level names include:

- `devstral:24b`
- `devstral-small-2:latest`
- `gemma4:26b`
- `gpt-oss:20b`
- `qwen2.5-coder:14b`
- `qwen3-coder:30b`

Initial classification:

`gitignore-candidate`

These names appear to correspond to local model/runtime artifacts rather than
GAIA source material.

They should not be moved into documentation or source directories.

Before changing `.gitignore`, verify whether these are files, directories,
symlinks, or other local artifacts and whether they are currently tracked by
Git.

## Root-level temporary/generated artifacts

Any additional root-level files produced by benchmark runs, patch generation,
local tooling, or experiments should be classified before cleanup.

Default rule:

- source -> retain in appropriate source area;
- historical evidence -> retain/archive;
- generated local output -> ignore or remove;
- temporary transfer artifact -> remove/archive after verification;
- unknown -> leave untouched.

## Cleanup order

The repository should be cleaned in this order:

1. classify;
2. verify references;
3. identify canonical location;
4. identify historical value;
5. decide retain/relocate/archive/remove;
6. perform moves in a separate reviewable commit;
7. update references;
8. verify repository and tooling.

## Non-destructive constraint

This audit intentionally performs no filesystem restructuring.

No root artifact should be deleted, renamed, moved, or added to `.gitignore`
solely because it appears in this document.

## Next audit

The next step is a reference/dependency audit of the root Python files,
patch scripts, ZIP archives, and local runtime artifacts.

That audit should establish which artifacts are:

- already represented by Git history;
- referenced by active tooling;
- required by documentation;
- historical but worth retaining;
- safe to archive;
- safe to remove;
- safe to ignore.

