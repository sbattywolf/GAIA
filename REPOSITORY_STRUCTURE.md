# Repository Structure

- **Version:** 0.2
- **Status:** Consolidated
- **Audience:** Contributors, reviewers, future collaborators

## Purpose

The repository preserves clarity, discoverability, architectural traceability, historical context, and long-term maintainability. Stable definitions, research, decisions, experiments, and implementation must remain visibly separate.

## Structure

```text
GAIA/
├── README.md
├── REPOSITORY_STRUCTURE.md
├── DOCUMENT_MANIFEST.md
├── reference/
├── sprint-01/
├── sprint-02/
├── adr/
├── validation/
├── incubator/
├── diagrams/
└── src/                  # future
```

## Folder responsibilities

- `reference/`: stable project identity, direction, principles, vocabulary, current model, and roadmap.
- `sprint-01/`: foundational framework research, reuse analysis, hostile critique, and decision framing.
- `sprint-02/`: stress-test synthesis and lessons transferred to validation.
- `adr/`: proposed and accepted Architecture Decision Records.
- `validation/`: briefs that define uncertainty, evidence, tests, and decision linkage.
- `incubator/`: unvalidated ideas, not commitments.
- `diagrams/`: editable visual sources. Mermaid is preferred when practical.
- `src/`: implementation only after sufficient validation.

## Document lifecycle

Idea → Research → Review → Validation → ADR → Implementation

Not every idea reaches implementation. Research is preserved even when superseded. Decisions belong in ADRs, not chat logs or commit messages.

## Rules

1. Stable and experimental content must not be mixed.
2. Every canonical document has one responsibility.
3. Duplicate research is merged; superseded copies are archived outside the canonical tree or deleted after verification.
4. Unvalidated ideas remain in the incubator.
5. The Core is protected from speculative features.
6. Editable diagrams are canonical; raster exports are secondary.
7. Enterprise-confidential or Restricted material must not enter this personal repository.
8. The repository optimises for understanding, not volume.
