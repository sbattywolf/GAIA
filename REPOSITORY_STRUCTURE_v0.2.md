# Repository Structure

**Project:** GAIA  
**Document type:** Repository Governance  
**Status:** Proposed  
**Version:** 0.2  
**Supersedes:** `REPOSITORY_STRUCTURE.md`  
**Phase:** Architecture Convergence  
**Last updated:** 2026-08-03

## 1. Purpose

This document defines how the GAIA repository is organised and how documents move from research and proposals to accepted decisions and implementation.

The repository supports a personal domestic project maintained by one Human Owner. Its structure must preserve clarity and history without introducing enterprise-scale process overhead.

The repository optimises for:

- easy discovery;
- clear Source of Truth;
- architectural traceability;
- fast movement from decision to useful implementation;
- separation of stable and experimental work;
- low maintenance burden;
- safe preservation of superseded material.

## 2. Repository principles

### Source of Truth

The repository is the official Source of Truth for GAIA project documentation and code.

### Documentation proportional to risk

Document decisions that materially constrain architecture, safety, correctness, or replacement. Do not create documents solely to appear complete.

### Stable versus experimental separation

Accepted reference material is separated from Sprint research, validation work, and ideas.

### Decisions are first-class

Material architectural decisions belong in ADRs, but only when a real decision exists.

### Research is preserved

Research remains available even when conclusions change.

### Experiments are disposable

Experiments reduce uncertainty. They do not define architecture automatically.

### Production value matters

Repository structure must not delay a useful domestic production slice through ceremony, duplicate artefacts, or speculative design.

## 3. Proposed repository overview

```text
GAIA/
├── README.md
├── REPOSITORY_STRUCTURE_v0.2.md
│
├── reference/
│   ├── DESIGN_PRINCIPLES.md
│   ├── IDENTITY.md
│   ├── NORTH_STAR.md
│   ├── MANIFESTO.md
│   ├── GLOSSARY.md
│   ├── GLOSSARY_v0.2.md
│   ├── GAIA_MODEL.md
│   ├── GAIA_MODEL_v0.2.md
│   ├── ARCHITECTURE_CONVERGENCE.md
│   ├── ARCHITECTURE_CONVERGENCE_v0.2.md
│   ├── CONTEXT_MODEL.md
│   ├── CONTEXT_MODEL_v0.2.md
│   ├── WORLD_MODEL.md
│   ├── WORLD_MODEL_v0.2.md
│   └── NEXT_STEPS_v0.2.md
│
├── adr/
│   └── README.md
│
├── sprint-01/
├── sprint-02/
├── sprint-03/
│
├── incubator/
├── validation/
├── diagrams/
└── src/                         # introduced when implementation begins
```

During Architecture Convergence, versioned reference files may coexist. After acceptance and Git-based history resume, canonical filenames without version suffixes should normally be restored.

## 4. Root files

### `README.md`

Repository entry point containing project overview, current status, reading order, principles, and active reference versions.

### `REPOSITORY_STRUCTURE_v0.2.md`

This document. It defines folder responsibilities, document lifecycle, and naming rules.

Root files should remain minimal.

## 5. Reference folder

`reference/` contains the current project identity, principles, vocabulary, conceptual models, and roadmap.

### Stable identity documents

- `DESIGN_PRINCIPLES.md`
- `IDENTITY.md`
- `NORTH_STAR.md`
- `MANIFESTO.md`

These should change rarely.

### Active convergence documents

- `GLOSSARY_v0.2.md`
- `GAIA_MODEL_v0.2.md`
- `ARCHITECTURE_CONVERGENCE_v0.2.md`
- `CONTEXT_MODEL_v0.2.md`
- `WORLD_MODEL_v0.2.md`
- `NEXT_STEPS_v0.2.md`

These remain `Proposed` until reviewed and accepted.

### Version preservation during convergence

When a substantial compatible revision is created:

```text
DOCUMENT.md
DOCUMENT_v0.2.md
```

The new document records:

```text
Status: Proposed
Version: 0.2
Supersedes: DOCUMENT.md
```

The previous file remains unchanged until the new version is accepted. After acceptance, the previous version may be marked `Superseded` but is not deleted during convergence.

Minor corrections may update the active file without a new filename when they do not alter meaning.

## 6. ADR folder

`adr/` contains Architecture Decision Records for material decisions.

### Candidate ADR set

The following filenames are **provisional candidates**, not accepted decisions:

- `ADR-0001-Core-Boundary.md`
- `ADR-0002-Memory-Semantics.md`
- `ADR-0003-Capability-Model.md`
- `ADR-0004-HomeAssistant-Boundary.md`
- `ADR-0005-Communication-State.md`
- `ADR-0006-Tool-Trust.md`
- `ADR-0007-Event-Semantics.md`

Only ADR-0001 and ADR-0003 are current pre-prototype requirements.

### ADR rule

Create an ADR when a decision:

- materially constrains architecture;
- has meaningful alternatives and trade-offs;
- is difficult or costly to reverse;
- affects safety, authority, or boundaries;
- must remain understandable after implementation changes.

Do not create an ADR for terminology cleanup, routine refactoring, minor configuration, or an idea without a decision.

### ADR content

Each ADR should state:

- status;
- context and problem;
- decision;
- alternatives considered;
- trade-offs;
- consequences;
- validation or evidence;
- affected documents;
- superseded decisions, if any.

## 7. Sprint folders

Sprint folders preserve time-bounded research, critique, and learning.

### `sprint-01/`

Foundational research, reuse analysis, architectural critique, and discussion guides.

### `sprint-02/`

World Model review, stress testing, patterns, hidden bottlenecks, lessons learned, and synthesis.

### `sprint-03/`

Current validation-oriented work, initially including:

- `MEMORY_ROLE_VALIDATION.md`;
- first-scenario validation brief;
- evidence that may inform later ADRs.

Sprint documents do not become normative automatically.

## 8. Validation folder

`validation/` is optional during the first personal prototype.

Use it only when validation artefacts outgrow a single Sprint folder or become recurring. Until then, `sprint-03/` is sufficient and simpler.

This avoids creating a folder hierarchy before it provides value.

## 9. Incubator folder

`incubator/` preserves ideas that are not roadmap commitments, architecture decisions, or implementation priorities.

Candidate ideas include:

- Memory Inspector;
- Capability Simulator;
- Planner red-team;
- MCP kill-switch;
- Event chaos testing;
- Research Collaborator;
- Voice Domain;
- auto-generated Domains;
- runtime scorecard;
- Home Assistant replay sandbox;
- boundary violation detector.

An idea is promoted only when it addresses a validated problem, has a bounded responsibility, and justifies its complexity.

## 10. Diagrams folder

`diagrams/` stores editable visual artefacts separately from canonical textual documents.

Preferred sources are editable formats such as Mermaid, Draw.io, or SVG where practical. PNG images may accompany them.

A diagram is explanatory unless a reference document explicitly declares it canonical. Sprint-generated diagrams remain historical hypotheses.

## 11. Source code folder

`src/` is introduced when implementation begins.

Do not freeze a detailed source tree before ADR-0001 and ADR-0003. The first implementation should use the smallest structure supporting the first scenario.

A possible initial shape may be:

```text
src/
├── core/
├── home/
└── adapters/
```

This is an implementation suggestion, not canonical architecture. Add folders only when code requires them.

Avoid pre-creating empty folders for Planner, Registry, Memory, Event Bus, Workflow, or Plugin systems.

## 12. Document lifecycle

| Status | Meaning |
|---|---|
| Draft | Being actively developed; incomplete. |
| Proposed | Complete enough for review and possible adoption. |
| Accepted | Current official reference or decision. |
| Superseded | Replaced by a later version; retained for traceability. |
| Deprecated | Still present or usable but discouraged and intended for removal. |
| Archived | Historical material outside the active decision path. |
| Research | Evidence, analysis, or critique without normative authority. |
| Incubating | Idea preserved without commitment. |
| Planned | Validation not started. |
| In Progress | Validation underway. |
| Completed | Validation finished with recorded evidence. |

Use `Superseded` for replaced documents. Use `Deprecated` for a still-existing concept or mechanism that should no longer be used.

## 13. Change classification

### Minor

Examples:

- typo;
- broken link;
- non-semantic clarification;
- status update.

Action: update the active file; optionally increment patch version.

### Substantial but compatible

Examples:

- major restructuring;
- clarified semantic boundary;
- responsibility refinement that preserves direction.

Action: create a new full version during convergence and preserve the previous one.

### Architectural

Examples:

- change to Core responsibility;
- new first-class concept;
- incompatible Capability semantics;
- change of Source of Truth;
- new mandatory platform or boundary.

Action: new full version, preserved predecessor, and ADR where material.

## 14. Canonical naming after convergence

Version suffixes are temporary support for local manual convergence.

When a proposed version is accepted and normal Git history resumes, prefer:

```text
GLOSSARY.md
GAIA_MODEL.md
CONTEXT_MODEL.md
WORLD_MODEL.md
```

Historical versions may move to `archive/reference/` or remain in Git history. Do not maintain filename versioning and Git history indefinitely unless it continues to add value.

## 15. Reading order

Recommended active reading order:

1. `README.md`
2. `reference/NORTH_STAR.md`
3. `reference/IDENTITY.md`
4. `reference/DESIGN_PRINCIPLES.md`
5. `reference/MANIFESTO.md`
6. `reference/GLOSSARY_v0.2.md`
7. `reference/GAIA_MODEL_v0.2.md`
8. `reference/CONTEXT_MODEL_v0.2.md`
9. `reference/WORLD_MODEL_v0.2.md`
10. `reference/ARCHITECTURE_CONVERGENCE_v0.2.md`
11. `reference/NEXT_STEPS_v0.2.md`
12. accepted ADRs
13. Sprint material as supporting history

## 16. Repository rules

1. Research is preserved but is not normative.
2. Architectural decisions belong in ADRs, not only conversations or commits.
3. Ideas remain in the Incubator until validated.
4. The Core is protected from speculative features.
5. The repository optimises for understanding, not volume.
6. A document must have a unique role.
7. Avoid duplicate checklists and repeated definitions where a reference is sufficient.
8. Do not create folders or templates before they are needed.
9. Production value may justify a modest implementation, but never hidden unsafe behaviour or uncontrolled data loss.
10. Every structural change should make GAIA easier for one person to understand, operate, or evolve.

## 17. Current active versions

During the current reconciliation, the proposed active set is:

- `ARCHITECTURE_CONVERGENCE_v0.2.md`;
- `CONTEXT_MODEL_v0.2.md`;
- `WORLD_MODEL_v0.2.md`;
- `GLOSSARY_v0.2.md`;
- `GAIA_MODEL_v0.2.md`;
- `NEXT_STEPS_v0.2.md`;
- `REPOSITORY_STRUCTURE_v0.2.md`.

The corresponding original unversioned files remain preserved until explicit acceptance.

## 18. Final test

Before adding a file, folder, template, or process, ask:

> Does this help one person understand, validate, operate, or safely evolve GAIA sooner?

If the answer is unclear, do not add it yet.
