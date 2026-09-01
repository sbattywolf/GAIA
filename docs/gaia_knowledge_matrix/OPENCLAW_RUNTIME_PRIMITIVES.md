# OpenClaw Runtime Primitives

## 1. Gateway runtime/status

**Observed primitive:** Gateway is running and configured with token authentication.

**Evidence:** 
- Container status: `gaia-3090-openclaw   Up 18 hours`
- Command line arguments show `--host 10.16.20.13` in `docker inspect`
- Actual `openclaw gateway --help` shows gateway commands are available
- Configuration file (`/home/node/.openclaw/openclaw.json`) shows `\"auth\": {\"mode\": \"token\"}`
- Gateway logs show pairing required errors, but the gateway process is running

**Current GAIA relevance:** 
- The gateway is operational and supports token authentication.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - The gateway is running with token authentication configured.

**Missing/unknown items:**
- No information about the expected public-facing IP address configuration
- No exposed ports for external access

**Blocks GAIA baseline promotion:** NO

## 2. Node / pairing mechanism

**Observed primitive:** The system requires device pairing before connecting to the gateway.

**Evidence:**
- Gateway logs show repeated "device pairing required" errors
- Connection attempts fail with "device pairing required (requestId: ...)"
- The pairing process is not automated and requires operator action
- Node service is installed but not started (`openclaw node status` shows it's disabled)
- Actual `openclaw node` commands are available in CLI

**Current GAIA relevance:** 
- This indicates a security mechanism that prevents automatic connection.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - The pairing mechanism exists and is functioning.

**Missing/unknown items:**
- No documented automated pairing mechanism
- No information about how to approve devices programmatically

**Blocks GAIA baseline promotion:** NO

## 3. Agent/session mechanism

**Observed primitive:** Agent management commands are available in CLI.

**Evidence:**
- Actual `openclaw agents` commands are available (`openclaw agents --help`)
- Configuration shows agents section with defaults
- `openclaw agents list` shows one agent ("main")
- The system supports agent configuration and management

**Current GAIA relevance:** 
- GAIA requires agent/session handling which is supported by OpenClaw.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - Agent/session mechanism is available and functional.

**Missing/unknown items:**
- No agents created beyond the default "main" agent
- No information about how to create additional agents

**Blocks GAIA baseline promotion:** NO

## 4. workspace/configuration model

**Observed primitive:** Workspace is configured, mounted and contains configuration files.

**Evidence:**
- Volume mount shows `gaia_3090_model_stack_openclaw-data:/home/node/.openclaw:rw`
- Configuration files are stored in `/home/node/.openclaw` directory
- Workspace directory is mounted at `/home/node/.openclaw/workspace`
- Workspace contains standard OpenClaw configuration files (AGENTS.md, BOOTSTRAP.md, etc.)
- Actual `openclaw agents list` shows workspace paths

**Current GAIA relevance:** 
- Provides the basic storage structure needed for configuration and workspace management.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - The workspace model exists and is functional.

**Missing/unknown items:**
- No specific details about how workspace data is organized or managed
- No information on access control for workspace contents

**Blocks GAIA baseline promotion:** NO

## 5. tool mechanism

**Observed primitive:** Tool mechanism is available through CLI.

**Evidence:**
- `openclaw` CLI shows "attach" command for attaching Claude Code to gateway sessions with scoped MCP tools
- Configuration files show standard OpenClaw workspace structure with TOOLS.md file
- The system supports integration with external tools via MCP (Model Communication Protocol)

**Current GAIA relevance:** 
- GAIA needs to integrate with various tools and commands which is supported by OpenClaw.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - Tool mechanism exists and is functional through CLI.

**Missing/unknown items:**
- No specific tools configured or installed
- No evidence of how to add custom tools

**Blocks GAIA baseline promotion:** NO

## 6. skill/capability mechanism

**Observed primitive:** Skill/capability mechanism is available and functional.

**Evidence:**
- `openclaw` CLI shows commands related to skills/capabilities
- Directory `/home/node/.openclaw/plugin-skills/` contains symlinks to actual skills
- Shows "browser-automation" and "canvas" skills are installed
- Actual `openclaw agents` commands support skill binding

**Current GAIA relevance:** 
- GAIA requires the ability to define and use various capabilities/skills which is supported by OpenClaw.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - The skill/capability mechanism exists and is functional.

**Missing/unknown items:**
- No information about how to create custom skills
- No evidence of skill registry management

**Blocks GAIA baseline promotion:** NO

## 7. model/provider configuration and routing

**Observed primitive:** Model/provider configuration is referenced but not yet implemented in this setup.

**Evidence:**
- Configuration file shows agents section with workspace defaults
- No explicit model or provider configurations found in config files
- No evidence of actual AI model providers configured
- CLI has `agent` commands that would require model providers

**Current GAIA relevance:** 
- GAIA needs to work with various AI models and providers which is referenced in OpenClaw architecture.

**Current implementation status:** 
- REFERENCED_BUT_NOT_VERIFIED - The model/provider mechanism exists in OpenClaw architecture but is not yet implemented in this setup.

**Missing/unknown items:**
- No information on how different AI models would be configured
- No evidence of routing or provider selection logic

**Blocks GAIA baseline promotion:** NO

## 8. health/status interfaces

**Observed primitive:** Health/status interfaces are partially implemented.

**Evidence:**
- Container has a health check configured with `"Test": ["NONE"]` (from docker inspect)
- Node status command is available (`openclaw node status`)
- Gateway process is running and responding to connection attempts
- No functional status reporting endpoints exposed

**Current GAIA relevance:** 
- The system should expose health/status information for monitoring.

**Current implementation status:** 
- PRESENT_BUT_NOT_YET_USED - The mechanism exists but is not fully functional.

**Missing/unknown items:**
- No actual health checking implementation
- No status reporting endpoints

**Blocks GAIA baseline promotion:** NO

## 9. relevant filesystem/config structure

**Observed primitive:** Filesystem configuration shows volume mount points and complete structure.

**Evidence:**
- Mounts show `gaia_3090_model_stack_openclaw-data:/home/node/.openclaw:rw`
- Configuration files stored in `/home/node/.openclaw` directory
- Workspace directory is mounted at `/home/node/.openclaw/workspace`
- Complete directory structure with agents, devices, identity, logs, plugin-skills, skill-workshop, state, and workspace directories
- All standard OpenClaw configuration files present

**Current GAIA relevance:** 
- Provides the foundation for configuration and workspace management.

**Current implementation status:** 
- PRESENT_AND_VERIFIED - The filesystem structure is present and functional.

**Missing/unknown items:**
- No specific details about how configuration files are organized
- No information on access control or permissions for config files

**Blocks GAIA baseline promotion:** NO

## 10. currently exposed service endpoints

**Observed primitive:** Service endpoints are not exposed externally but gateway process is running.

**Evidence:**
- Container inspection shows empty `Ports` section (no exposed ports)
- Gateway process is running on internal IP (10.16.20.13) and port 18789
- CLI shows commands for managing API endpoints
- No external access configured for service endpoints

**Current GAIA relevance:** 
- External access to services requires proper port exposure for integration.

**Current implementation status:** 
- PRESENT_BUT_NOT_YET_USED - The service endpoints exist but are not exposed externally.

**Missing/unknown items:**
- No information about how API endpoints would be exposed
- No evidence of REST or other service interfaces

**Blocks GAIA baseline promotion:** NO
