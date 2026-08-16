---
name: gaia-collaborator-home-assistant
description: Handle Home Assistant collaborator operations through the GAIA integration boundary.
---

# GAIA Collaborator Home Assistant

## Purpose

Handle Home Assistant-related requests through the architectural boundary defined by GAIA.

## Rules

- Home Assistant is an external system.
- Do not place Home Assistant-specific assumptions in GAIA Core behavior.
- Use the available Home Assistant adapter/integration boundary.
- Do not bypass the adapter boundary.
- Do not invent entity IDs.
- Do not invent device state.
- For reads, report the observed state.
- For actions, use only the explicitly requested operation and target.
- If the target cannot be identified reliably, stop before execution.

## Evidence

The collaborator must distinguish:

- requested state
- observed state
- requested action
- executed action
- execution result

Do not claim an action succeeded without tool evidence.

## Failure

If the Home Assistant boundary is unavailable or insufficient:

- do not simulate success;
- do not fabricate state;
- report that the requested operation could not be demonstrated.
