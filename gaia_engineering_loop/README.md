# GAIA Engineering Loop

This directory contains the implementation of the autonomous engineering loop framework for GAIA.

## Architecture Overview

The engineering loop follows a layered architecture:

1. **GAIA AI ENGINEER** - High-level decision making
2. **ORCHESTRATOR** - Supervision, classification, recovery  
3. **TARGET ADAPTER** - Interface to different execution modes
4. **TRANSPORT** - Execution mechanism (SSH, etc.)
5. **TARGET RUNNER** - Actual validation execution
6. **EVIDENCE / RESULT** - Structured output and reporting

## Components

### Phase 1: Local Simulation (Current)
- `gaia_orchestrator.sh` - Core orchestration with failure classification and recovery
- `gaia_target_adapter.sh` - Target execution interface  
- `inventory_utils.sh` - Inventory management utilities
- Target inventory structure in `gaia_target_inventory/`

### Phase 2: Framework Consolidation
- Complete integration of all components
- Enhanced error handling and retry policies

### Phase 3: SSH Transport
- Secure shell transport implementation
- Connection management and authentication

### Phase 4: Remote Execution
- Actual target execution via transport layer

## Failure Classification

The orchestrator implements clear failure taxonomy:

1. **TRANSPORT_FAILURE** - SSH timeouts, connection issues, DNS failures
2. **ORCHESTRATION_FAILURE** - Local wrapper/process failures  
3. **TARGET_EXECUTION_FAILURE** - Runner crashes, unexpected exit codes
4. **TARGET_VALIDATION_RESULT** - PASS, FAIL, BLOCKED, UNKNOWN, INVALID

## Recovery Strategy

- Transport failures: retry with bounded attempts
- Execution failures: inspect and decide on recovery
- Persistent failures: escalate to human intervention