# GAIA 1070 Service Map

## Services Overview

### gaia-1070-ollama
- **Type**: Ollama (light)
- **Purpose**: Local LLM inference engine
- **Port**: 11434 (internal)
- **Volume**: ollama-data (/root/.ollama)
- **Network**: gaia-1070-model-stack

### gaia-1070-openwebui
- **Type**: Open WebUI
- **Purpose**: Web interface for interacting with LLMs
- **Port**: 127.0.0.1:3000:8080 (localhost only)
- **Volume**: openwebui-data (/app/backend/data)
- **Network**: gaia-1070-model-stack
- **Dependency**: gaia-1070-ollama (healthy)

### gaia-1070-openclaw
- **Type**: OpenClaw Gateway
- **Purpose**: Code generation and execution service
- **Port**: 127.0.0.1:18789:18789 (localhost only)
- **Volume**: openclaw-data (/home/node/.openclaw)
- **Network**: gaia-1070-model-stack
- **Dependency**: gaia-1070-ollama (healthy)

## Startup Order
1. gaia-1070-ollama (local LLM engine)
2. gaia-1070-openwebui (web interface)
3. gaia-1070-openclaw (code execution service)

## Persistence
All services use named volumes for persistent data:
- ollama-data: Persistent storage for Ollama models and settings
- openwebui-data: Persistent storage for Open WebUI data
- openclaw-data: Persistent storage for OpenClaw state and workspace

## Security
- All ports are localhost-only (127.0.0.1)
- No public network exposure
- Services run in isolated containers with proper restart policies
- Health checks ensure service availability