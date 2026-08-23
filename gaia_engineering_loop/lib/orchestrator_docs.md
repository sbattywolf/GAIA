# GAIA Engineering Loop Orchestrator

## Purpose

The orchestrator provides supervision, classification, and recovery for the engineering loop. It handles failures gracefully without stopping the entire loop.

## Failure Categories

### 1. TRANSPORT_FAILURE
- SSH timeouts or connection refused
- DNS resolution issues  
- Authentication failures
- **Recovery**: Retry with bounded attempts

### 2. ORCHESTRATION_FAILURE  
- Local wrapper script failures
- Process invocation errors
- Evidence collection failures
- **Recovery**: Retry if safely possible

### 3. TARGET_EXECUTION_FAILURE
- Runner crashes or exits with error codes
- Target environment issues during execution
- **Recovery**: Depends on specific failure type

### 4. TARGET_VALIDATION_RESULT
- PASS, FAIL, BLOCKED, UNKNOWN, INVALID
- **Action**: Process result and decide next loop iteration

## Event Format

All events follow this JSON structure:
```json
{
  "event": "EVENT_TYPE",
  "layer": "layer_name", 
  "retryable": true/false,
  "component": "component_name",
  "reason": "failure_reason",
  "exit_code": 0
}
```

## Recovery Policy

1. **Recoverable failures**: Attempt retry with bounded attempts
2. **Non-recoverable failures**: Escalate to next level of decision making  
3. **Semantic results**: Process and return appropriate exit codes

## Integration Points

- Connects to target adapters for execution
- Communicates with transport layer for connection management
- Works with evidence collection systems
- Integrates with Git commit system for state persistence