# GAIA

**A local-first Personal AI Operating System**

GAIA is a personal ecosystem of specialised digital collaborators designed to reduce cognitive load, coordinate context, and act through explicit capabilities while keeping important decisions under human control.

## Project status

GAIA is currently in the research and architectural validation phase. The repository defines the project identity, long-term direction, design principles, conceptual model, vocabulary, research findings, open questions, and validation roadmap. It does not yet define a final architecture or framework selection.

## Core commitments

- Human authority remains explicit.
- Local ownership and operation are preferred whenever practical.
- Components should remain replaceable.
- Capabilities and sensitive actions require clear boundaries.
- Memory must be inspectable, correctable, exportable, and removable.
- Complexity must remain sustainable for one human maintainer supported by AI collaborators.
- Implementation must not redefine the identity of GAIA.

## Recommended reading order

1. [`reference/NORTH_STAR.md`](reference/NORTH_STAR.md)
2. [`reference/IDENTITY.md`](reference/IDENTITY.md)
3. [`reference/MANIFESTO.md`](reference/MANIFESTO.md)
4. [`reference/DESIGN_PRINCIPLES.md`](reference/DESIGN_PRINCIPLES.md)
5. [`reference/GAIA_MODEL.md`](reference/GAIA_MODEL.md)
6. [`reference/GLOSSARY.md`](reference/GLOSSARY.md)
7. [`reference/NEXT_STEPS.md`](reference/NEXT_STEPS.md)
8. [`sprint-01/GAIA_Reuse_Analysis.md`](sprint-01/GAIA_Reuse_Analysis.md)
9. [`sprint-01/GAIA_Architectural_Critique.md`](sprint-01/GAIA_Architectural_Critique.md)
10. [`sprint-01/ARCHITECTURE_DISCUSSION_GUIDE.md`](sprint-01/ARCHITECTURE_DISCUSSION_GUIDE.md)
11. [`sprint-02/SPRINT_02_SYNTHESIS.md`](sprint-02/SPRINT_02_SYNTHESIS.md)

## Repository layout

```text
GAIA/
├── README.md
├── REPOSITORY_STRUCTURE.md
├── reference/
├── sprint-01/
├── sprint-02/
├── adr/
├── incubator/
├── diagrams/
└── src/                  # future
```

- `reference/` contains stable project definitions.
- `sprint-01/` preserves foundational research, reuse analysis, critique, and decision framing.
- `sprint-02/` preserves architectural stress testing and synthesis.
- `adr/` records explicit architectural decisions and consequences.
- `incubator/` contains unvalidated ideas that are not roadmap commitments.
- `diagrams/` contains editable visual sources and exported images.
- `src/` is reserved for implementation after sufficient validation.

## Current canonical research conclusion

GAIA should build the contracts, reuse the edges, and validate the centre. Frameworks, runtimes, channels, and external platforms may be reused behind explicit boundaries, but they must not define GAIA's identity or silently become its architectural centre of gravity.

## Immediate next step

Complete Phase 0 by validating the consolidated documentation set. Then begin Phase 1 with proposed ADRs and focused validation briefs. Proposed ADRs are decision candidates, not accepted architecture.

## Governance rule

Research may propose. Reviews may challenge. Validation should produce evidence. ADRs decide. Implementation follows accepted decisions.
