# Architecture Discussion Guide

> Recovery status: Reconstructed  
> Source basis: surviving Sprint references, Architecture Discussion Guide, repository structure specification, and conversation history  
> Confidence: Medium  
> Preservation rule: This file retains its original role. Reconstructed passages are not presented as verbatim recovery.

This guide identifies decisions; it does not make them.

![Decision map](../assets/diagrams/02_gaia_decision_map.png)

```mermaid
flowchart TD
    ID[Identity] --> CORE[Core]
    ID --> DOMAIN[Domain Model]
    CORE --> PLANNER[Planner]
    CORE --> MEMORY[Memory]
    CORE --> REGISTRY[Registry]
    CORE --> CAPABILITY[Capability]
    CAPABILITY --> RESOURCE[Resource Model]
    DOMAIN --> COMM[Communication]
    INFRA[Infrastructure] --> CORE
    INFRA --> MEMORY
    INFRA --> COMM
    REGISTRY --> FUTURE[Future Evolution]
    CAPABILITY --> FUTURE
    CORE --> FUTURE
```

## Critical discussion areas

1. Operational identity of GAIA and practical meaning of local-first.
2. Core boundary and build-versus-reuse for orchestration.
3. Explicit versus implicit planner.
4. Role, correction and deletion semantics of memory.
5. Scope and shape of registries.
6. Capability, permission, approval and resource models.
7. Home Assistant as adapter, domain, source of truth or external runtime.
8. Telegram and communication-state ownership.
9. Infrastructure boundaries across 1070, 3090, Raspberry Pi and NAS.
10. Evolution process for collaborators, domains and external protocols.
