# Repository Structure

- **Version:** 0.3
- **Status:** Current
- **Audience:** Contributors, reviewers, future collaborators

## Purpose

This document describes the current repository structure and the responsibility
of its major areas.

Historical research, recovered documentation, validation evidence, prototypes,
runtime implementation, and project governance must remain distinguishable.

## Structure

```text
GAIA/
├── README.md
├── AGENTS.md
├── DOCUMENT_MANIFEST.md
├── MANIFEST.txt
├── REPOSITORY_STRUCTURE.md
├── REPOSITORY_STRUCTURE_v0.2.md
├── GAIA_ENGINEER_AS_IS_REVIEW.md
├── REAL_HOME_ASSISTANT_ADAPTER_DESIGN.md
├── SHA256SUMS.txt
│
├── reference/
├── adr/
├── validation/
├── incubator/
├── diagrams/
├── prompts/
├── reports/
├── sprint-01/
├── sprint-02/
├── sprint-03/
│
├── src/
├── tests/
├── gaia-bootstrap-poc/
├── oldRepoReferences/
├── assets/
│
└── .github/
```

## Folder responsibilities

- `reference/`: current project concepts, identity, principles, models, and roadmap material.
- `adr/`: explicit architectural decisions and their history.
- `validation/`: validation briefs, evidence, and decision-support material.
- `incubator/`: unapproved ideas and exploratory concepts.
- `diagrams/`: editable and supporting visual artefacts.
- `prompts/`: bounded prompts used to restart or guide project work.
- `reports/`: reconstruction, audit, baseline, consolidation, and other non-normative project reports.
- `sprint-01/`: foundational research and architectural critique.
- `sprint-02/`: stress testing, synthesis, and lessons learned.
- `sprint-03/`: validation-oriented engineering and project history.
- `src/`: current implementation/runtime source.
- `tests/`: implementation and integration tests.
- `gaia-bootstrap-poc/`: prototype and benchmark implementation.
- `oldRepoReferences/`: historical/reference material imported from previous projects; not current GAIA implementation.
- `assets/`: reusable visual or project assets.
- `.github/`: repository automation, agent definitions, skills, and workflows.

## Root documentation

Root documentation is intentionally limited to repository entry points,
governance, provenance, and high-value project-level references.

Documents with historical or reconstruction roles must not be treated as
current architecture merely because they are located at repository root.

## Historical structure documents

`REPOSITORY_STRUCTURE_v0.2.md` is retained as historical Architecture
Convergence material.

It records the repository structure and governance model proposed during that
period. It is not the current repository structure contract.

`reference/REPOSITORY_STRUCTURE.md` is retained as recovered reference
material. Its recovery status and source basis are documented in the file
itself. It is not the canonical current structure document.

## Document lifecycle

```text
Research → Validation → Proposed → Accepted/Current
                         ↓
                    Superseded
                         ↓
                     Archived
```

Historical documents are retained when they provide useful provenance or
explain previous engineering decisions.

Git history is the primary version history for current documents. Filename
versioning is used only when it provides meaningful historical or convergence
value.

## Repository rule

The repository should optimize for understanding, traceability, and safe
evolution rather than document volume.

Before creating a new document or directory, verify that an existing canonical
document or directory does not already own the responsibility.
