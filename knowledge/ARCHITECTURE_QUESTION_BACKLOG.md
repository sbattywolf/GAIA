# Architecture Question Backlog

- **Status:** Active

## Identity
- What stable mental model should the owner use for GAIA?
- What operational requirements define local-first?

## Core
- What is the minimum responsibility budget?
- Which concerns must remain outside Core?

## Planner and orchestration
- When does deterministic routing stop being sufficient?
- Which workflow semantics are truly required?

## Memory
- What may be retained, by whom, for how long, and with what provenance?
- Is memory peripheral or central to GAIA's value?

## Registry
- What scale or lifecycle justifies dynamic discovery?

## Capability and Resource
- What metadata, scope, risk, approval, and revocation semantics are required?

## Domain
- Is Home Assistant a platform, domain source of truth, or replaceable adapter?
- What second domain can test generality?

## Communication
- Which state survives channel replacement?

## Infrastructure
- What works without internet, cloud, or the primary model runtime?
- When is a second provider sufficient reason for a gateway?

## Future evolution
- What lifecycle governs collaborators, adapters, tools, and deprecated concepts?

## Backlog rule

Each critical question must map to a validation brief or Proposed ADR. Questions without validated urgency remain in research or the incubator.
