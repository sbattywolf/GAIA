# Sprint 7 / GAIA 1070 Architecture Plan

## Objective
Build the GAIA 1070 ALWAYS-ON runtime using the accepted 3090 reference as the starting architectural pattern.

## Key Principles
1. Keep OpenClaw FULL
2. Keep one human operator
3. Keep persistent volumes
4. Keep WebUI and OpenClaw sibling services
5. Do not make OpenClaw startup depend on remote 3090 availability
6. Use Ollama-light locally for fallback operation
7. Add remote 3090 Ollama only as a runtime backend
8. Do not stop or modify 3090 native Ollama yet
9. Do not introduce OpenCode yet
10. Do not introduce custom router/message bus

## Service Set
- gaia-1070-ollama (light)
- gaia-1070-openwebui
- gaia-1070-openclaw

## Architecture Overview

### 1070 Service Dependencies
```
gaia-1070-ollama
└── gaia-1070-openwebui
└── gaia-1070-openclaw
```

### Startup Model
1. Ollama-light (local only)
2. OpenWebUI 
3. OpenClaw

The 1070 must boot with 3090 unavailable.

## Volume Layout
- ollama-data: /root/.ollama
- openwebui-data: /app/backend/data
- openclaw-data: /home/node/.openclaw

## Network Configuration
- Dedicated network for 1070 services
- No public exposure except localhost

## Security Boundaries
- All services run in isolated containers
- Persistent volumes are secure and accessible only to respective services
- No direct network exposure beyond localhost

## Migration Notes from 3090
- Remove GPU resources (not needed for 1070)
- Change Ollama to light version
- Update service names from 3090 to 1070
- Remove remote dependencies on 3090 services
- Update credentials to 1070-specific values