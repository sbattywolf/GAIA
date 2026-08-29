# GAIA 3090 Model Serving Stack

This directory contains the canonical configuration for the GAIA 3090 model-serving stack.

## Overview

This stack provides a self-contained, reproducible configuration for running Ollama and Open WebUI on the 3090 target hardware.

## Components

- **gaia-3090-ollama**: Ollama service with GPU access
- **gaia-3090-openwebui**: Open WebUI frontend

## Configuration Structure

```
gaia_3090_model_stack/
├── compose.yaml          # Canonical Docker Compose configuration
├── .env.example          # Environment variable placeholders
├── README.md             # This file
├── config/               # Service-specific configurations (if needed)
├── secrets/              # Secret management (if needed)
└── scripts/              # Start/stop/status scripts
```

## Services

### Ollama Service
- Container: `gaia-3090-ollama`
- Image: `ollama/ollama:latest`
- Port: `11434` (internal only)
- Volume: `ollama-data` (persistent model storage)

### Open WebUI Service
- Container: `gaia-3090-openwebui`
- Image: `ghcr.io/open-webui/open-webui:main`
- Port: `3000` (host-exposed)
- Volume: `openwebui-data` (persistent data storage)
- Depends on: `gaia-3090-ollama`

## Network
- Name: `gaia-3090-model-stack`
- Driver: `bridge`

## Usage

1. Copy `.env.example` to `.env`
2. Fill in actual secret values in `.env`
3. Run: `docker compose -f compose.yaml up`

## Security
- Secrets are referenced via environment variables (not embedded)
- All secrets must be set in the local `.env` file
- No real secrets are stored in this repository

## Persistence
- Ollama models are stored in the `ollama-data` volume
- Open WebUI data is stored in the `openwebui-data` volume
