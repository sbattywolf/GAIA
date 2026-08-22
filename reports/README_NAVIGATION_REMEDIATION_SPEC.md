# GAIA README Navigation Remediation Specification

## Status

Patch 10 has been pushed to the existing repository-consolidation PR.

The PR was re-checked after the push. It remains open, non-draft, and
mergeable.

## Verified current state

The repository now explicitly establishes:

1. `REPOSITORY_STRUCTURE_v0.3.md` — current repository-structure authority;
2. `DOCUMENT_MANIFEST.md` — current documentation inventory;
3. `MANIFEST.txt` — historical/provenance inventory;
4. `REPOSITORY_STRUCTURE_v0.2.md` — historical convergence record;
5. `reference/REPOSITORY_STRUCTURE_v0.1.md` — recovered reference material.

The current `README.md` still predates that authority decision in two places:

- it links readers to `reference/REPOSITORY_STRUCTURE_v0.1.md`;
- its embedded repository tree reflects the earlier repository organisation.

The README also documents Sprint 1 and Sprint 2 but does not currently provide
a Sprint 3 navigation section.

## Patch 11 scope

The next README edit should be intentionally minimal.

### Required change 1

Change the repository-structure navigation target from:

`reference/REPOSITORY_STRUCTURE_v0.1.md`

to:

`REPOSITORY_STRUCTURE_v0.3.md`

### Required change 2

Do not present the old embedded repository tree as the current authoritative
filesystem description.

Replace it with a concise statement directing readers to the canonical
root-level `REPOSITORY_STRUCTURE_v0.3.md`.

The README should remain a project entry point rather than becoming a second
repository manifest.

### Required change 3

Add Sprint 3 to the repository-reading guidance using only verified files.

Verified Sprint 3 files include:

- `sprint-03/ARCHITECTURE_CONVERGENCE_REVIEW_v0.1.md`
- `sprint-03/FIRST_HOME_SCENARIO_VALIDATION.md`
- `sprint-03/MEMORY_ROLE_VALIDATION.md`
- `sprint-03/engineer-agent/`

Do not invent a canonical reading order for Sprint 3 unless the repository
establishes one.

## Explicit non-goals

The README correction must not:

- change GAIA identity;
- change the conceptual model;
- change architecture;
- rewrite Sprint 1 or Sprint 2 history;
- delete `reference/REPOSITORY_STRUCTURE_v0.1.md`;
- delete `REPOSITORY_STRUCTURE_v0.2.md`;
- change Collaborator benchmark contracts;
- alter runtime code.

## Implementation rule

When applying the next patch, preserve the existing README content and make
only the navigation/authority corrections described above.

Do not reconstruct unrelated README sections merely for formatting or
consistency.

## Why this is a separate patch

The authority decision and the navigation audit are already committed in the
same consolidation PR. Separating the actual README edit keeps the change
reviewable and prevents accidental changes to GAIA's project-level framing.

## Result expected after Patch 11

A reader entering through `README.md` should be able to:

- understand GAIA's identity and current phase;
- find the canonical repository structure without being redirected to a
  historical/recovered structure document;
- discover Sprint 3 without changing the historical meaning of earlier sprints.

This specification is the implementation boundary for Patch 11.
