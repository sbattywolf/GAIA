# POC-001 Specification

## Objective
Execute the first controlled POC to evaluate OpenCode as a Developer Agent with GAIA framework on NVIDIA 3090 with Ollama.

## Architecture
Two POC variants to compare:

**POC-A: Direct OpenCode**
```
GAIA
 ↓
GAIA Developer Agent Contract
 ↓
OpenCode
 ↓
Ollama
 ↓
3090
```

**POC-B: OpenClaw → ACP → OpenCode**
```
GAIA
 ↓
GAIA Developer Agent Contract
 ↓
OpenClaw
 ↓ ACP
OpenCode
 ↓
Ollama
 ↓
3090
```

## Bounded Coding Task
1. Read repository structure and GAIA context
2. Understand current GAIA project knowledge
3. Apply a minimal GAIA skill (code analysis)
4. Make controlled file modifications
5. Execute tests
6. Collect evidence of execution
7. Verify capability policy compliance
8. Ensure no remote Git mutations

## Target Environment
- Primary: NVIDIA 3090 with local Ollama installation
- Secondary targets: 1070 and QNAP (for architectural modeling only)
- Raspberry Pi: DO NOT TOUCH

## Capability Profile
- READ
- WORKSPACE_WRITE  
- TEST_EXECUTION
- DENY: git push, git commit, remote delivery, destructive filesystem operations

## Software Requirements
- OpenCode (candidate primary developer agent)
- Ollama (local model runtime)
- Existing OpenClaw installation (if available for POC-B)

## Evidence Collection
- Target specifications
- Software versions
- Model/provider information
- Configuration details
- Skills used
- Knowledge subset applied
- Task execution details
- Commands/tools used
- Files changed
- Tests executed
- Results and errors
- Timing/resources
- Git mutation status

## Non-Functional Requirements
- No git operations (add, commit, push, etc.)
- No destructive filesystem operations
- No remote delivery capabilities
- Reproducible task execution
- Clear architectural boundary demonstration