# Identity

> Recovery status: Recovered from the surviving GAIA identity artefact and converted to Markdown  
> Source basis: `IDENTITY.md.rtf` authored by Carlo Argento  
> Confidence: High  
> Preservation rule: This retains the document role, section sequence, identity statement, tests and review guidance.

## Purpose

This document defines the identity of GAIA. It explains what GAIA is, what GAIA is not, and what should remain true even when architecture, technologies, models, frameworks, domains and implementations change. It is intentionally more stable than implementation documents and should guide architectural decisions, product direction, research priorities and future trade-offs without prescribing a specific technical solution.

GAIA's identity should not be derived from a framework, model provider, user interface or single integration. Those may change. The identity should remain.

## What GAIA Is

GAIA is a local-first Personal AI Operating System. It is a personal ecosystem of specialised digital collaborators that help the user reduce cognitive load, coordinate work, manage context and interact with digital or physical systems within explicit boundaries.

GAIA is intended to grow over time with the user. It should learn the user's working style, preferences, recurring needs, important context and boundaries, but only in ways that remain inspectable, correctable and under user control.

GAIA is not defined by conversation alone. Conversation may be one interface, but the system identity is broader than chat. GAIA is best understood as:

- a personal coordination environment;
- a system of specialised collaborators;
- a local-first control layer;
- a context-aware assistant ecosystem;
- a long-term personal software substrate;
- a system designed to remain understandable and replaceable.

## What GAIA Is Not

GAIA is not another chatbot. It is not primarily a prompt interface, chat window or conversational wrapper around a model. GAIA is also not:

- a generic agent framework;
- a workflow automation product;
- a home automation dashboard;
- a knowledge management application;
- a model provider wrapper;
- a cloud assistant;
- a single-purpose bot;
- a collection of scripts;
- a replacement for human judgement;
- a system that silently acts on behalf of the user without clear authority.

Some categories may overlap with GAIA in specific areas. GAIA may use workflows, agents, memory, automation, messaging, local models or external tools. None of those defines GAIA's identity.

## Core Identity

### 1. Personal

GAIA exists for the user. It is not designed first as an enterprise platform, multi-tenant SaaS product, public assistant or generic automation system. Its primary relationship is with a single owner.

### 2. Local-First

GAIA should prefer local ownership, local execution and local control whenever practical. Local-first is not only a deployment preference. It expresses a product philosophy: personal systems should remain inspectable, recoverable and usable without unnecessary dependence on remote services.

### 3. Collaborator-Based

GAIA is composed conceptually of specialised digital collaborators. A collaborator is not merely a model call. It represents a bounded responsibility within the ecosystem. The collaborator metaphor should clarify responsibility, not hide complexity.

### 4. Human-Controlled

GAIA should amplify human capability without replacing human responsibility. Important actions, sensitive decisions and irreversible changes should remain visible and governable by the user.

### 5. Evolvable

GAIA should change over many years without collapsing under its own complexity. Its identity should survive changes in models, runtimes, frameworks, hardware, user interfaces and integrations.

## Relationship With The User

The user is not simply an operator issuing commands. The user is the owner, source of authority and final decision-maker for important outcomes. GAIA may reduce repetitive cognitive load, remember explicit preferences, organise context, prepare actions, coordinate specialised collaborators, surface relevant information, ask for clarification, propose safe next steps and automate low-risk routines when allowed.

GAIA should not manipulate the user, hide uncertainty, overstate confidence or make it difficult to understand why something happened. The relationship should be based on transparency, trust, user control, reversibility where possible, correction, explicit memory and explicit boundaries.

## Relationship With Technology

Technology is a means, not the identity of GAIA. Local models, cloud models, agent frameworks, workflow engines, databases, messaging systems, home automation platforms, retrieval systems and other tools remain subordinate to GAIA's principles.

A technology is healthy for GAIA when it solves a real problem, can be bounded and replaced, does not redefine Core identity, avoids unnecessary complexity, remains maintainable by a very small team, preserves local-first intent where relevant and improves user control.

A technology is risky when it becomes the hidden centre of gravity, forces GAIA to adopt its conceptual model, makes replacement unrealistic, owns too much state, turns adapters into platforms or creates operational complexity disproportionate to delivered value.

## Long-Term Vision

GAIA should remain useful, understandable and evolvable for many years. It may grow from a small set of collaborators into a broader personal operating environment without losing conceptual clarity. It may support multiple domains, richer memory, more capable collaborators, better local runtimes, deeper integrations and more sophisticated coordination. Growth should be incremental and validated.

The long-term goal is not maximum autonomy. The goal is sustainable augmentation: helping the user think, decide, remember, coordinate and act while preserving agency.

## Non-Goals

### Not Maximum Automation
GAIA should not optimise for doing as much as possible without the user. Automation is acceptable only when bounded, understandable and aligned with intent.

### Not Framework Competition
GAIA should not compete with agent frameworks, workflow engines, LLM platforms or automation tools. It may reuse, learn from or integrate them without being defined by them.

### Not Cloud Dependency
Cloud services may be useful, but they should not be the default foundation of GAIA's identity and should remain explicit and replaceable where possible.

### Not Feature Accumulation
GAIA should not grow by adding every possible integration, collaborator or capability. Growth should serve coherence, not novelty.

### Not Invisible Intelligence
GAIA should not become opaque. If the user cannot understand or inspect important behaviour, the system is moving away from its identity.

### Not Replacement Of The User
GAIA should not aim to make the user unnecessary. It should support agency, judgement and intent.

## Identity Tests

1. **Chatbot Test** - If chat were removed, would GAIA still make sense?
2. **Framework Replacement Test** - If the main framework were replaced, would GAIA still be GAIA?
3. **Model Replacement Test** - If the model provider changed, would identity remain intact?
4. **Channel Replacement Test** - If Telegram, voice or web UI were replaced, would the same principles hold?
5. **Local-First Test** - Can GAIA provide meaningful value when external services are unavailable?
6. **Human Control Test** - Can the user understand, approve, correct or stop important behaviour?
7. **Memory Intent Test** - Is it clear what was remembered, why, and how to correct or forget it?
8. **Complexity Test** - Can a very small team understand and maintain the system?
9. **Boundary Test** - Is ownership of each responsibility clear?
10. **Identity Over Implementation Test** - Does the decision strengthen durable identity or merely follow a tool, trend or shortcut?

## Stable Identity Statement

> GAIA is a local-first Personal AI Operating System: a personal ecosystem of specialised digital collaborators that helps the user reduce cognitive load, coordinate context, and act through explicit capabilities while keeping important decisions under human control.

This statement is not an architecture. It is the identity future architecture should protect.

## Review Guidance

This document should change rarely. A change to `IDENTITY.md` should be treated as a significant project event because it may affect architecture, roadmap, glossary, principles, ADRs and implementation priorities. Before changing it, ask whether identity is changing or implementation knowledge is merely improving. If only implementation changes, this document should probably remain stable.
