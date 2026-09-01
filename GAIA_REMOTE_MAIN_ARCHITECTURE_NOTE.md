# GAIA REMOTE MAIN ARCHITECTURE NOTE

## Core Roles and Responsibilities

### 3090 Role
- Primary local inference/compute node
- Main Qwen/local model workload
- Engineering workload
- OpenCode integration
- ON-DEMAND compute (prefer powered off when not required)

### 1070 Role
- ALWAYS-ON utility/edge node
- OpenClaw/node/runtime support
- Browser/automation/lightweight services
- Secondary/background workloads
- Not the primary LLM host

### QNAP Role
- Persistent storage, backup, archive
- Optional future knowledge/memory storage
- NOT a primary compute node
- NOT a required dependency for GAIA runtime

### Remote Main Role
- Small portable semantic/control baseline
- Identity, governance, and durable architecture semantics
- Durable agent/engineer contracts
- Selected knowledge/provenance rules
- References to implementation/evidence where useful

### Memory Role
- Future memory architecture may be:
  Human → GAIA entry point → GAIA semantic baseline → knowledge/memory retrieval → agent orchestration → tools/runtime
- Not implemented now, but serves as semantic memory/reference for online sessions

### OpenClaw Role
- Gateway/runtime support
- Integration with 1070 always-on node
- Primary runtime coordination

### OpenCode Role
- Engineering workload and development environment
- Integration with 3090 compute node
- Development operations

### Orchestration Role
- Coordination between 3090, 1070, and QNAP components
- Semantic control of the GAIA system
- Runtime orchestration framework

### Git/Linear Role
- Version control and history preservation
- Repository state management
- Documentation baseline synchronization