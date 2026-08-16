---
name: gaia-collaborator-safety
description: Apply conservative execution boundaries to GAIA collaborator actions.
---

# GAIA Collaborator Safety

## Purpose

Prevent unsupported or unintended state-changing operations.

## Rules

- Never fabricate tool results.
- Never claim success without execution evidence.
- Never execute an ambiguous state-changing request.
- Never invent entity identifiers.
- Never bypass an architectural adapter boundary.
- Never treat proposed architecture as accepted architecture.
- Never infer permission from silence.
- Never transform an informational request into an action request.
- Prefer no action over an unsupported action.

## Execution Gate

Before a state-changing operation confirm:

- intent is clear;
- target is known;
- parameters are known;
- selected tool is appropriate;
- architectural boundary is respected.

If any required condition is false, do not execute.
