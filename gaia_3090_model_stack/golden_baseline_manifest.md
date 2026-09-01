# GAIA-3090 GOLDEN BASELINE

## REAL HOST
- hostname: sbatta30-System-Product-Name
- Docker context: default
- GPU: NVIDIA GeForce RTX 3090

## 3090 CONTAINERS
- OpenClaw: gaia-3090-openclaw
- Ollama: gaia-3090-ollama  
- OpenWebUI: gaia-3090-openwebui

## RUNNING IMAGE DIGESTS
- OpenClaw: sha256:a1244a907a20cde7553389386aa2c70af44f9713ae87011c69ee5a6039caafd3
- Ollama: sha256:9e7d782e99880c70f9563c51633da875ca605518a8f8d95c2532bda70a027b7a
- OpenWebUI: sha256:ce4f44a04ce411f33aa6ae44ee91dec03f05fe17e937524edf94018c59845d54

## VERSIONS
- OpenClaw: 2026.7.1
- Ollama: 0.33.2
- OpenWebUI: main

## MODELS
- llama3.2:1b-instruct-fp16 (2.5 GB)

## COMPOSE
### Captured:
- image: ollama/ollama:latest
- image: openclaw/openclaw:latest
- image: ghcr.io/open-webui/open-webui:main
- ports: 18789/tcp, 3000/tcp (mapped to localhost)
- networks: gaia_3090_model_stack_gaia-3090-model-stack (bridge)
- mounts: 
  - ollama-data → /root/.ollama
  - openclaw-data → /home/node/.openclaw
  - openwebui-data → /app/backend/data
- GPU reservations: nvidia, count: -1
- restart policies: unless-stopped
- healthchecks: configured

### Pin patch prepared:
```
services:
  gaia-3090-ollama:
    image: ollama/ollama@sha256:9e7d782e99880c70f9563c51633da875ca605518a8f8d95c2532bda70a027b7a
  gaia-3090-openclaw:
    image: openclaw/openclaw@sha256:a1244a907a20cde7553389386aa2c70af44f9713ae87011c69ee5a6039caafd3
  gaia-3090-openwebui:
    image: ghcr.io/open-webui/open-webui@sha256:ce4f44a04ce411f33aa6ae44ee91dec03f05fe17e937524edf94018c59845d54
```

### Pin patch applied: NO

## 1070
- touched: NO

## PAIRING
- attempted: NO

## GIT
- commit: NO
- push: NO

## STATUS
3090 GOLDEN BASELINE CAPTURED