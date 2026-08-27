# POC-001 Architecture

## Overview
This document outlines the architectural boundaries and components for POC-001, comparing direct OpenCode integration against OpenClaw ACP integration with OpenCode.

## GAIA Layer (Authoritative)
- **Semantic Contract**: Core behavioral framework that defines what agents can do
- **Architect Knowledge**: GAIA's core architectural principles and governance rules
- **Project Knowledge**: Current project information and documentation subset
- **GAIA Skill Library**: Collection of skills designed for compatibility with GAIA contracts
- **Governance**: Authority over agent selection, replacement, and operational boundaries

## Developer Agent Layer (Replaceable)
- **OpenCode**: Primary candidate developer agent that will execute the bounded task
- **OpenHands**: Secondary candidate for comparison
- **Cline**: Tertiary candidate for comparison

## Runtime/Control Plane Layer (Replaceable)
- **OpenClaw**: Potential operational substrate that can host developer agents
- **ACP (Agent Control Plane)**: Component within OpenClaw that manages agent operations

## Boundary Definitions

### GAIA Authority Boundaries
1. **Semantic Contract**: Defines what operations are allowed
2. **Knowledge Authority**: Controls access to project knowledge
3. **Skill Library**: Governs what capabilities can be used
4. **Capability Requirements**: Determines what permissions are needed
5. **Governance**: Makes decisions about agent selection and replacement

### Developer Agent Boundaries  
1. **Execution Environment**: Where the agent runs (3090 with Ollama)
2. **Permission Model**: What operations the agent can perform
3. **Skill Interface**: How skills are invoked and used
4. **Knowledge Injection**: How project knowledge is provided to the agent

### Runtime Layer Boundaries
1. **Gateway**: Interface for communication channels
2. **Composition Layer**: Integration of different skills/plugins
3. **Session Management**: Handling of user sessions
4. **Policy Enforcement**: Ensuring capability policies are followed

## POC-A Architecture (Direct)
```
[GAIA]
   ↓ Semantic Contract
[OpenCode] 
   ↓ Permission Model
[Ollama]
   ↓ Local Execution
[3090]
```

## POC-B Architecture (With OpenClaw)
```
[GAIA]
   ↓ Semantic Contract  
[OpenClaw]
   ↓ ACP Layer
[OpenCode]
   ↓ Permission Model
[Ollama]
   ↓ Local Execution
[3090]
```

## Key Architectural Considerations

### 1. Routing and Session Handling
- POC-A: Direct routing from GAIA to OpenCode
- POC-B: Routing through OpenClaw ACP to OpenCode

### 2. Policy Boundary Enforcement
- Both architectures must maintain GAIA's capability policy
- OpenCode must respect the READ + WORKSPACE_WRITE + TEST_EXECUTION profile

### 3. Skill Integration
- Skills must be properly projected from GAIA to OpenCode
- Adapter layer may be required for skill translation

### 4. Knowledge Injection
- Project knowledge must be injected appropriately in both architectures
- Provenance must be preserved in both cases

### 5. Evidence Collection
- Both architectures must provide structured evidence of execution
- Failure handling should be consistent between approaches

## Expected Outcomes
The POC will determine whether OpenClaw provides sufficient value to justify an additional runtime layer, focusing on:
- Architectural complexity reduction
- Operational overhead
- Replaceability maintenance
- Policy boundary enforcement