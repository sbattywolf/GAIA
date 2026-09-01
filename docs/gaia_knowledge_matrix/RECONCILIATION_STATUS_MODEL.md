# GAIA Reconciliation Status Model

## Overview

This document proposes a refined reconciliation status model to better distinguish between semantic authority, evidence status, and implementation status. This separation is necessary to avoid confusing implementation existence with architectural invariance.

## Proposed Status Dimensions

### Semantic Status
- `CURRENT` - The concept is actively defined and used in current architecture
- `DURABLE` - The concept has proven stability and is foundational 
- `REFINED` - The concept has been updated or improved from earlier versions
- `SUPERSEDED` - The concept has been replaced by a newer alternative
- `UNKNOWN` - The semantic status cannot be determined

### Evidence Status
- `CONFIRMED` - There is clear, direct evidence supporting the claim
- `PARTIAL` - Evidence exists but is incomplete or partial
- `HISTORICAL` - Evidence is from historical sources only, no current validation
- `IMPLEMENTATION-ONLY` - Evidence exists only in implementation, not documented
- `UNKNOWN` - The evidence status cannot be determined

### Implementation Status
- `RUNNING` - The technology is currently operational and running
- `PRESENT` - The technology is available and can be used
- `PROTOTYPE` - The technology is in prototype phase
- `ABSENT` - The technology is not implemented or present
- `UNKNOWN` - The implementation status cannot be determined

## Examples from Current Matrix

### Ollama Integration
- **Semantic Status**: CURRENT
- **Evidence Status**: CONFIRMED  
- **Implementation Status**: RUNNING

### OpenWebUI Integration
- **Semantic Status**: CURRENT
- **Evidence Status**: CONFIRMED
- **Implementation Status**: RUNNING

### OpenClaw Integration
- **Semantic Status**: CURRENT
- **Evidence Status**: HISTORICAL
- **Implementation Status**: RUNNING

### Architectural Critique
- **Semantic Status**: DURABLE
- **Evidence Status**: HISTORICAL
- **Implementation Status**: ABSENT

### Memory Role Validation
- **Semantic Status**: CURRENT
- **Evidence Status**: PARTIAL
- **Implementation Status**: PROTOTYPE

## Rationale

This model allows us to distinguish:
1. That a technology is currently running (implementation status)
2. That GAIA defines a semantic requirement for this technology (semantic status)  
3. That the concept is defined and documented (evidence status)
4. That a concept is foundational to GAIA's architecture (semantic status)

This separation prevents confusing implementation existence with architectural invariance.

**Important clarification**: 
- Semantic Status describes the status of a GAIA concept/requirement, NOT whether GAIA depends on a specific technology
- A technology can be RUNNING while its Semantic Status is UNKNOWN if GAIA may replace it without changing the underlying semantic requirement
- Historical evidence should not be confused with current semantic authority
- Implementation presence should not be confused with architectural necessity