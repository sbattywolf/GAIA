# Reuse Analysis

## Thesis

GAIA should build only the contracts and semantics that preserve its identity. Mature external systems should be reused behind explicit adapters when their state, lifecycle and failure modes remain bounded.

## Build internally

- GAIA-native vocabulary and contracts;
- capability and approval semantics;
- resource identity and boundary rules;
- collaborator descriptors;
- trace/audit envelope;
- adapter interfaces and replacement tests.

## Reuse externally

- Home Assistant state, registries and service execution;
- Telegram transport;
- Ollama or another local model runtime;
- databases, vector stores and workflow engines only when a validated need exists;
- MCP selectively for interoperability, never as implicit authority.

## Decision matrix

| Area | Default | Reason |
|---|---|---|
| Core semantics | Build minimal | Defines GAIA |
| Model inference | Reuse | Commodity and replaceable |
| Home state/control | Reuse Home Assistant | Existing domain source of truth |
| Messaging transport | Reuse | Channel is not identity |
| Orchestration | Defer / experiment | Risk of framework ownership |
| Memory | Validate before selecting | Semantics precede storage |
| Observability | Reuse tooling, own trace semantics | Operational support without losing meaning |

## Risks

A “thin adapter” can still leak an external conceptual model. Framework checkpoints can become canonical memory. Tool schemas can become capability policy by accident. A first successful Home Assistant integration can silently redefine the whole Core.
