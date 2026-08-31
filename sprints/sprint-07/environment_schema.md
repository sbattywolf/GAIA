# GAIA 1070 Environment Variable Schema

## Core Variables

### Open WebUI Secret Key
WEBUI_SECRET_KEY=<set-locally>

### OpenClaw Gateway Token (1070)
OPENCLAW_GATEWAY_TOKEN_1070=<set-locally>

## Service Configuration

### Ollama Settings
OLLAMA_HOST=0.0.0.0
OLLAMA_KEEP_ALIVE=5m

### OpenWebUI Settings
OLLAMA_BASE_URL=http://gaia-1070-ollama:11434
ENABLE_SIGNUP=false

## Network Configuration

### Service Ports
- gaia-1070-openwebui: 127.0.0.1:3000:8080
- gaia-1070-openclaw: 127.0.0.1:18789:18789

## Volume Mounts
- ollama-data: /root/.ollama
- openwebui-data: /app/backend/data
- openclaw-data: /home/node/.openclaw