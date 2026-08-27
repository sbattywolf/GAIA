# GAIA — STR-3 — POC-001-A — OPENCODE CONFIGURATION DISCOVERY ONLY

## OpenCode 1.18.23 Configuration Discovery

### Configuration Files Discovered
- `~/.config/opencode/opencode.jsonc` - Contains MCP configuration for Ollama (incorrect approach)
- Temporary probe file created during testing but removed

### Configuration Precedence
OpenCode 1.18.23 reads configuration files in the following order:
1. `~/.config/opencode/opencode.json`
2. `~/.opencode/config/opencode.json` 
3. `./opencode.json` (project-local)

### Environment Variables
No relevant environment variables found (`OPENCODE_CONFIG`, `OPENCODE_CONFIG_CONTENT`, etc.)

### Provider Schema Compatibility
The provider schema for `@ai-sdk/openai-compatible` is supported in OpenCode 1.18.23.
The configuration format used in the POC is correct according to official documentation.

### Model Discovery
- `opencode models` command shows standard OpenCode models but does **NOT** show `ollama/qwen3-coder:30b`
- This indicates that the custom provider configuration is not being loaded by OpenCode

### Endpoint Verification
- Ollama endpoint (`http://localhost:11434/api/tags`) returns qwen3-coder:30b model
- OpenAI-compatible endpoint (`http://localhost:11434/v1/models`) returns qwen3-coder:30b model
- Both endpoints are working correctly

### Remaining Blocker
The primary blocker is that OpenCode 1.18.23 does not recognize the custom provider configuration in `~/.config/opencode/opencode.jsonc`. The existing configuration uses MCP approach which is incorrect for Ollama integration, and needs to be updated to use the `@ai-sdk/openai-compatible` provider approach.

### Recommended Next Step
The configuration file at `~/.config/opencode/opencode.jsonc` must be updated with the correct OpenAI-compatible provider format that matches the official documentation. The current MCP-based configuration prevents proper model discovery and integration.

