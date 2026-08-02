# GAIA Architecture Discussion Guide

## Purpose

This guide identifies decisions to discuss. It does not make decisions, design the final architecture, or select frameworks.

## Critical decisions

| Priority | Decision | Why it matters |
|---|---|---|
| Critical | Operational identity | Determines what Core must protect |
| Critical | Core boundary | Prevents framework creep or hidden coupling |
| Critical | Human control | Shapes capability, approval, and sensitive actions |
| Critical | Memory role | May become the system's centre of gravity |
| High | Home Assistant role | Adapter, domain, or dominant platform |
| High | Capability/permission model | Required before exposing real tools |
| High | Communication state | Telegram must not own conceptual state |
| Medium | MCP boundary | Promising but not mandatory |
| Medium | Internal vs external orchestrator | Requires workflow evidence |

## Decision areas

### Identity and local-first
Define the user problem, stable mental model, offline/degraded expectations, local data rules, and acceptable remote fallback.

### Core
Define the minimal responsibility budget and compare a thin coordination layer, microkernel, event-based core, and orchestrator-centric alternatives.

### Planner and orchestration
Compare implicit model planning, deterministic routing, hybrid planning, and explicit workflow graphs on the same scenarios.

### Memory
Define what may be remembered, prohibited retention, provenance, correction, deletion, export, and cross-domain access.

### Registry
Introduce only if the number and lifecycle of tools, collaborators, adapters, or capabilities justify dynamic discovery/versioning.

### Capability and Resource
Define metadata, scope, risk, approval, revocation, versioning, and audit. Resources require stable identity across adapters.

### Domain Model
Keep Home Assistant from defining all future domains. Validate at least one replaceability or second-domain pressure test.

### Communication
Keep channel identity, session, notification, and threading concerns outside the durable conceptual state.

### Infrastructure
Validate runtime, storage, observability, recovery, and no-network behaviour. Avoid early multi-provider abstractions.

## Decision roadmap

1. Clarify identity and constraints.
2. Delimit the first domain.
3. Validate real complexity.
4. Evaluate standardisation only where evidence requires it.
5. Prepare a second-domain pressure test.

## Output discipline

Open questions become validation briefs. Decisions become ADRs. Ideas without evidence remain in the incubator.
