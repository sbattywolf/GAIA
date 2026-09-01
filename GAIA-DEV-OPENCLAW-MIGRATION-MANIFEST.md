# GAIA-DEV OpenClaw Migration Manifest

## 1. Scope

This document outlines the migration of the GAIA E2 Engineer from its current VS Code/Copilot-like environment to an OpenClaw/OpenCode runtime environment, maintaining all existing GAIA semantics and boundaries while leveraging OpenClaw's orchestration capabilities.

## 2. Source E2

The source E2 engineer is defined in `.github/agents/GAIA-E2-Engineer-Qwen3-30B.agent.md` with:
- Model: qwen3-coder:30b
- Tools: read, search, edit, execute
- Operating mode: bounded implementation and validation
- Authorization: E2 implementation handoff and validation tests
- Workspace: repository-local only
- Stop conditions: architectural boundary violations, unauthorized changes

## 3. GAIA-Dev Definition

GAIA-Dev will be the OpenClaw agent that:
- Preserves all existing E2 behavior and boundaries
- Maintains GAIA's identity, semantics, and authority boundaries
- Operates as a specialized collaborator within the GAIA ecosystem
- Delegates to OpenCode for software engineering tasks
- Remains under OpenClaw's orchestration control

## 4. OpenClaw Mapping

| E2 source concept | Current meaning | OpenClaw mapping | Notes |
|-------------------|----------------|------------------|-------|
| Identity | GAIA E2 Engineer Qwen3-30B agent | OpenClaw agent identity | DIRECT |
| Description | Bounded GAIA E2 local engineer | OpenClaw agent with GAIA semantics | DIRECT |
| Mission | Execute bounded implementation and validation | OpenClaw agent executing validated tasks | DIRECT |
| Model | qwen3-coder:30b | OpenClaw node supporting model runtime | DIRECT |
| Workspace | Repository-local only | OpenClaw workspace with repository access | ADAPTATION REQUIRED |
| Tools | read, search, edit, execute | OpenClaw tool permissions for GAIA operations | DIRECT |
| Permissions | Bounded by E2 scope | OpenClaw agent permissions with GAIA boundaries | DIRECT |
| Skills | gaia-collaborator-intent, gaia-collaborator-ambiguity, etc. | OpenClaw skill integration | DIRECT |
| Scope | E2 implementation and validation only | OpenClaw agent scope with E2 boundaries | DIRECT |
| Stop conditions | Architectural violations, unauthorized changes | OpenClaw enforcement of GAIA boundaries | DIRECT |
| Validation | E2 acceptance tests | OpenClaw validation execution | DIRECT |
| Evidence | Implementation evidence discipline | OpenClaw evidence collection | DIRECT |
| Authorization | E2 handoff and validation | OpenClaw authorization with GAIA approval | DIRECT |
| Git restrictions | No autonomous commit/push | OpenClaw git access control | DIRECT |
| Safety rules | Bounded responsibility, no architecture changes | OpenClaw safety enforcement | DIRECT |

## 5. OpenCode Mapping

| E2 responsibility | OpenCode capability | Fit | Gap |
|-------------------|---------------------|-----|-----|
| Repository inspection | File system access | DIRECT | NONE |
| Search | Code and documentation search | DIRECT | NONE |
| File editing | Code modification | DIRECT | NONE |
| Shell execution | Command-line operations | DIRECT | NONE |
| Test execution | Testing framework | DIRECT | NONE |
| Git operations | Version control | DIRECT | NONE |
| Branch strategy | Repository management | DIRECT | NONE |
| Coding model | Software development | DIRECT | NONE |
| Context | Session context | DIRECT | NONE |
| Permissions | Access control | DIRECT | NONE |
| MCP | Model communication protocol | DIRECT | NONE |
| Plugin system | Extension capabilities | DIRECT | NONE |
| Agent/sub-agent behavior | Collaborator patterns | DIRECT | NONE |
| Approval/confirmation | Validation mechanisms | DIRECT | NONE |
| Workspace isolation | Containerized environments | DIRECT | NONE |

## 6. Skills Mapping

GAIA collaborator skills map directly to OpenClaw:
- gaia-collaborator-intent → OpenClaw intent resolution
- gaia-collaborator-ambiguity → OpenClaw ambiguity handling
- gaia-collaborator-state → OpenClaw state management
- gaia-collaborator-safety → OpenClaw safety enforcement
- gaia-collaborator-tool-selection → OpenClaw tool selection
- gaia-collaborator-home-assistant → OpenClaw Home Assistant adapter

## 7. Tool Policy

E2 tools map to OpenClaw capabilities:
- read → OpenCode file system access with GAIA boundary enforcement
- search → OpenCode search with GAIA scope limits
- edit → OpenCode editing with GAIA validation
- execute → OpenCode execution with GAIA safety rules

## 8. Model Strategy

The qwen3-coder:30b model will be served through:
- Ollama runtime on 3090 (already available)
- OpenClaw node connecting to Ollama service
- OpenCode as the coding harness for software development tasks

## 9. Workspace Strategy

Workspace will be managed by OpenClaw with:
- Repository access through OpenCode
- E2 boundaries enforced via OpenClaw permissions
- Context persistence maintained through OpenClaw sessions
- Validation and evidence collection handled by OpenClaw

## 10. 3090 Runtime Requirements

The 3090 node requires:
- OpenClaw agent runtime (already deployed)
- Ollama service with qwen3-coder:30b model
- OpenCode container for software engineering tasks
- Network connectivity to 1070 Gateway
- Access to repository workspace

## 11. 1070 Gateway Requirements

The 1070 Gateway requires:
- OpenClaw gateway service running
- Ollama service for model serving
- OpenWebUI interface
- Token-based authentication (already configured)
- Network routing for node communications

## 12. Docker Changes

The migration will require:
- Configuration of GAIA-Dev agent definition in OpenClaw
- Integration of OpenCode container with 3090 node
- Update of OpenClaw agent permissions to match E2 boundaries
- Validation of network connectivity between nodes

## 13. Environment Variables

Environment variables needed:
- OPENCLAW_GATEWAY_TOKEN (already configured)
- WEBUI_SECRET_KEY (for OpenWebUI access)
- Model-specific environment variables for qwen3-coder:30b
- Workspace path references for repository access

## 14. Security / Authority

Security approach maintains:
- Human authority preserved over all important decisions
- GAIA boundaries enforced by OpenClaw
- No autonomous architecture changes allowed
- E2 validation tests still required for acceptance
- Secret hygiene maintained through OpenClaw's credential management

## 15. Validation Plan

Validation steps include:
- Verify OpenClaw agent initialization with correct identity
- Confirm qwen3-coder:30b model availability in Ollama
- Validate OpenCode container functionality
- Test E2 boundary enforcement within OpenClaw
- Execute E2 acceptance tests via OpenClaw orchestration
- Verify evidence collection and reporting mechanisms

## 16. Rollback Plan

If migration fails:
- Revert to original VS Code/Copilot environment
- Preserve all E2 validation test results
- Maintain repository state as-is
- Document failure conditions for future analysis
- Ensure no unauthorized changes were made

## 17. Implementation Steps

1. Prepare OpenClaw configuration for GAIA-Dev agent
2. Configure OpenCode container on 3090 node
3. Validate network connectivity between nodes
4. Test model availability (qwen3-coder:30b)
5. Activate GAIA-Dev agent in OpenClaw system
6. Execute E2 validation tests
7. Observe and document behavior
8. Confirm rollback capability

## 18. Open Questions

- How does OpenCode handle repository access permissions?
- What are the specific OpenClaw agent configuration parameters for GAIA-Dev?
- How is evidence collection integrated with OpenClaw's observability features?

## 19. Human Decisions Required

- Final approval to activate GAIA-Dev in OpenClaw environment
- Confirmation of all E2 boundary conditions are maintained
- Authorization to proceed with OpenCode integration
- Validation that all existing E2 tests still pass in new runtime