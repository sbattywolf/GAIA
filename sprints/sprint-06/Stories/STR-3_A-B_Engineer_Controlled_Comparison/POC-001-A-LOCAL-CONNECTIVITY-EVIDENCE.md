# POC-001-A LOCAL CONNECTIVITY EVIDENCE

## CURRENT VERIFIED STATE

### Architecture Under Test
GAIA workspace
    ↓
OpenCode 1.18.23
    ↓
Ollama 0.32.13
    ↓
qwen3-coder:30b (30.5B parameters, 18GB)
    ↓
NVIDIA RTX 3090

### Ollama Status
- Ollama is running on port 11434 (standard port)
- Available models include:
  - qwen3-coder:30b (30.5B parameters, 18GB) - **Target model**
  - qwen2.5-coder:7b
  - qwen3:8b
  - gpt-oss:20b
  - llama3.2:3b
  - And others

### Direct Ollama Baseline Test Results
✅ Ollama API is accessible at http://localhost:11434
✅ Model qwen3-coder:30b is available and can process requests
✅ Direct model response test successful with "TEST SUCCESS"

## CONFIGURATION CHANGE

### OpenCode MCP Configuration Attempted
- Added Ollama as MCP server: `opencode mcp add ollama --url http://localhost:11434`
- Result: MCP server added but shows as "failed" with error:
  - SSE error: Invalid content type, expected "text/event-stream"
  - URL: http://localhost:11434

### Alternative Configuration Method
- OpenCode supports `--model` flag for direct model specification
- Attempted: `opencode run --model ollama/qwen3-coder:30b "Test message"`
- Result: Error occurred with "Unexpected server error"

## CONNECTIVITY RESULT

### Direct Ollama Connection
✅ Verified: Ollama is accessible and qwen3-coder:30b model is available

### OpenCode to Ollama Connection
❌ **PARTIAL**: OpenCode can reach Ollama API but cannot successfully utilize the model through OpenCode's interface

## PERFORMANCE OBSERVATION

### Direct Model Test
- Latency: ~1.4 seconds for model processing (including load time)
- Response: "TEST SUCCESS"
- Model loading time observed in response details

### Resource Usage
- GPU utilization: Not directly measurable without additional tools
- VRAM usage: Not directly measurable without additional tools  
- RAM usage: Not directly measurable without additional tools

## SECURITY / PERMISSION OBSERVATION

✅ Local access only (no cloud connectivity required)
✅ No Git mutations performed
✅ Workspace boundary maintained
✅ No changes to GAIA framework or OpenClaw

## UNKNOWN

- How to properly configure OpenCode for Ollama integration
- Specific requirements for MCP server compatibility with Ollama
- Whether the model is being loaded correctly in OpenCode's context

## INFERENCE

Based on available documentation and error messages:
1. Ollama API is working correctly and the qwen3-coder:30b model is accessible
2. OpenCode can communicate with Ollama but there appears to be a compatibility issue with how OpenCode expects the MCP protocol to work with Ollama
3. The error suggests Ollama's API doesn't provide the expected "text/event-stream" content type for the MCP protocol

## FUTURE PROPOSAL

### Immediate Steps
1. Investigate if there's a specific Ollama MCP server implementation or plugin
2. Check documentation for OpenCode-Ollama integration patterns
3. Determine if model loading behavior is different when used through OpenCode vs direct API

### Long-term Implementation
Consider implementing GAIA endpoint registry pattern to explicitly manage:
- OLLAMA_HOST (localhost)
- OLLAMA_PORT (11434)
- OLLAMA_ENDPOINT (http://localhost:11434/api)  
- OPENCODE_PROVIDER_ENDPOINT (to be configured for GAIA integration)

## GATE STATUS

**OPENCODE_LOCAL_MODEL_CONNECTIVITY_PARTIAL**

OpenCode can reach Ollama and confirm the model is available, but cannot successfully utilize the model through OpenCode's interface due to MCP protocol incompatibility.