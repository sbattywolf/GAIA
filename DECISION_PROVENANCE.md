# GAIA Engineering Loop - Decision Provenance

## Phase 2 Implementation Decisions

### AI_DECISIONS

1. **Transport Implementation Approach**
   - Decision: Use shell-based SSH transport with Python adapter
   - Reason: Reuse existing manual SSH path, user-space first approach, minimal dependencies
   - Evidence: Manual SSH connection works with alias configuration

2. **Key Authentication Method**
   - Decision: Prefer SSH key authentication over password authentication
   - Reason: Security and automation requirements for engineering loop
   - Evidence: SSH configuration shows IdentityFile directive

### FRAMEWORK_DECISIONS

1. **No Sudo Requirement**
   - Decision: Normal user execution only, no sudo runtime dependency
   - Reason: Security boundary preservation, avoid privilege escalation
   - Evidence: Configuration enforces user-space execution

2. **Target Execution Model**
   - Decision: Read-only execution for Phase 2 validation
   - Reason: Focus on transport discovery and implementation first
   - Evidence: Transport design supports read-only operations

3. **Retry Logic Implementation**
   - Decision: Implement retry logic in orchestrator with max 3 attempts
   - Reason: Handle transient transport failures gracefully
   - Evidence: Orchestrator script includes retry mechanism

### SHARED_DECISIONS

1. **Connection Timeout Handling**
   - AI proposes: Retry up to 3 times for connection errors
   - Framework enforces: Max 3 attempts, timeout limits
   - Evidence: Both orchestrator and transport layer include timeout handling

2. **Failure Classification**
   - AI proposes: Categorize failures by component (transport, orchestration, target)
   - Framework enforces: Structured result format with retryability indicators
   - Evidence: Both layers implement structured failure reporting

### HUMAN_DECISIONS

1. **SSH Key Authentication Fix**
   - Decision: Requires manual intervention to fix SSH key authentication
   - Reason: No automated way to provide password for key setup
   - Evidence: SSH connection requires password authentication

## Boundary Observations

### What appears naturally AI-driven:
- Transport failure diagnosis and recovery strategy
- Execution flow planning
- Test case generation for different failure modes

### What appears naturally deterministic:
- Retry limits enforcement
- Target identity validation
- Result schema definition
- Security boundary enforcement

### What remains ambiguous:
- When to retry vs when to escalate
- How to determine if a failure is truly transient
- Whether to continue with current approach or switch to alternatives

## Failures Observed

1. **SSH Key Authentication Failure**
   - Classification: Transport failure
   - Recovery: Manual key setup required
   - Evidence: SSH connection requires password authentication

2. **Python Import Failure**
   - Classification: Environment issue
   - Recovery: System package management required
   - Evidence: Python import fails due to system-managed packages

## Next Action

Continue with Phase 3 implementation focused on:
- Real 1070 read-only execution capability
- Remote target execution testing
- Recovery/resume behavior implementation