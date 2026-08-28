# POC-001 Capability Mapping

## Overview
This document maps GAIA capabilities to OpenCode permissions for the first POC, establishing the foundation for capability policy enforcement.

## GAIA Capabilities and OpenCode Permissions

### READ
- **GAIA Capability**: Read access to files, configurations, and project structure
- **OpenCode Permission**: File system read operations
- **Mapping**: Direct permission mapping - OpenCode can read all necessary project files
- **Verification**: Confirmed through OpenCode documentation on file access permissions

### WORKSPACE_WRITE
- **GAIA Capability**: Write access to workspace for controlled modifications
- **OpenCode Permission**: File system write operations with restrictions  
- **Mapping**: OpenCode must be configured to allow write operations within designated workspace boundaries
- **Verification**: OpenCode's permission model supports granular workspace controls

### TEST_EXECUTION
- **GAIA Capability**: Execution of tests and validation procedures
- **OpenCode Permission**: Shell/terminal execution capabilities for test runs
- **Mapping**: OpenCode's shell integration allows controlled test execution
- **Verification**: OpenCode documentation shows support for command execution

## Denied Capabilities (Explicitly Restricted)

### git push
- **GAIA Capability**: Remote code delivery
- **OpenCode Permission**: Not available - explicitly denied
- **Mapping**: OpenCode configuration blocks git operations

### git commit  
- **GAIA Capability**: Local code commit operations
- **OpenCode Permission**: Not available - explicitly denied
- **Mapping**: OpenCode configuration blocks git operations

### remote delivery
- **GAIA Capability**: External system code delivery
- **OpenCode Permission**: Not available - explicitly denied
- **Mapping**: OpenCode operates within local boundaries only

### destructive filesystem operations
- **GAIA Capability**: Potentially harmful file system modifications  
- **OpenCode Permission**: Restricted through permission model
- **Mapping**: OpenCode permissions are configured to prevent destructive operations

## Permission Granularity

### File System Permissions
- Read: Full project directory access
- Write: Limited workspace directory access  
- Execute: Shell command execution capabilities
- Delete: Not permitted (destructive operations blocked)

### Network Permissions
- Local network: Permitted for Ollama communication
- External network: Restricted to prevent unauthorized connections

### Model/Provider Permissions
- Local model access: Enabled for Ollama integration
- Cloud provider access: Disabled by default
- Model switching: Configurable through OpenCode settings

## Adapter Requirements

### Skill Projection Adapter
```
GAIA Skill → [Adapter] → OpenCode Skill
```
- **Purpose**: Translate GAIA skills into OpenCode-compatible operations
- **Implementation**: Configuration-based mapping of skill capabilities
- **Verification**: OpenCode's skill architecture supports adapter patterns

### Knowledge Injection Adapter  
```
GAIA Knowledge → [Adapter] → OpenCode Knowledge
```
- **Purpose**: Provide project knowledge to OpenCode in compatible format
- **Implementation**: Configuration file injection or API-based knowledge transfer
- **Verification**: OpenCode documentation shows knowledge configuration options

## Security Considerations

### Boundary Enforcement
- All mappings must be explicitly configured to prevent permission escalation
- OpenCode's permission model acts as a security boundary for GAIA authority
- Regular verification of permission settings is required

### Audit Trail
- Each capability mapping should have clear documentation of why it's needed
- Permission settings should be version-controlled and traceable
- Configuration changes must be auditable for security compliance

## Validation Plan

1. **Configuration Review**: Verify OpenCode permissions match GAIA capabilities
2. **Execution Testing**: Test that denied capabilities are properly restricted  
3. **Permission Verification**: Confirm mapping accuracy through actual operation
4. **Security Audit**: Ensure no unauthorized access paths exist