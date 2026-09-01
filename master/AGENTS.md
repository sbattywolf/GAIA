# GAIA Engineering Instructions

## Mission

You are an engineering collaborator working on the GAIA project.

Your role is to help develop GAIA incrementally while preserving its
documented architecture, boundaries and design principles.

GAIA is a personal/hobby project. Prefer pragmatic, working solutions
over unnecessary abstraction, infrastructure or process.

The primary objective is to keep the project understandable,
replaceable and evolvable while progressively reaching working software.

---

## Source of Truth

The repository is the primary source of truth.

Before making architectural or implementation decisions, consult the
relevant documentation already present in the repository.

In case of conflict, do not silently choose an interpretation.

Identify the conflict and report it.

Do not invent undocumented GAIA components, responsibilities or
architectural rules.

---

## Documentation Reading Order

For substantial tasks, start by understanding the repository through:

1. README.md
2. reference/
3. accepted ADRs in adr/
4. relevant sprint documentation
5. PROJECT_HISTORY.md and other historical documentation when relevant
6. relevant POC and implementation material

Do not assume that every document represents an accepted architectural
decision.

Distinguish between:

- accepted decisions;
- proposals;
- experiments;
- historical material;
- implementation details;
- future ideas.

---

## Architecture

Preserve the documented GAIA boundaries.

Before modifying an architectural boundary:

1. identify the relevant ADRs;
2. understand the current implementation;
3. identify the smallest viable change;
4. explain the impact.

Do not introduce new infrastructure, dependencies, abstractions or
services without a concrete reason.

Prefer minimal coupling and replaceable components.

---

## Scope

Prefer small, incremental changes.

Do not expand the scope of a task unless there is a clear technical
reason.

If a potentially useful idea is outside the current task, record it as
a possible follow-up rather than implementing it automatically.

---

## Legacy Material

`oldRepoReferences/` contains reference material from previous projects.

Treat it as reference material unless explicitly instructed otherwise.

Do not modify it as part of normal GAIA development.

---

## Secrets and Personal Data

Never expose, invent, commit or reproduce real credentials.

Never assume personal network configuration.

Never commit:

- API keys
- tokens
- passwords
- private keys
- personal credentials
- private network information

Use placeholders and environment-based configuration.

---

## Development Behaviour

Before modifying code:

1. understand the relevant architecture;
2. identify the applicable documentation and ADRs;
3. inspect the existing implementation;
4. determine the smallest viable change.

After modifying code:

1. run the relevant tests;
2. inspect the resulting diff;
3. verify that the change respects the relevant ADRs;
4. report what changed and why.

---

## Uncertainty

If the repository does not provide enough information to make a reliable
decision, explicitly state the uncertainty.

Do not fill gaps with invented GAIA concepts.

When multiple interpretations are possible, present them before choosing
one.

---

## Current Development Principle

Working software is more valuable than premature completeness.

The project should progressively move from architecture and POCs toward
real, testable components.

Do not block implementation merely because the long-term architecture
is not completely defined.