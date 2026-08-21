# GAIA 1070 Local Model Runtime

Minimal Docker Compose configuration for the GAIA Domestic Agent / Home Collaborator experimentation on the physical 1070.

## Overview

This setup provides a minimal isolated Ollama runtime environment specifically for the 1070 target hardware. It includes:

- Ollama service with GPU access
- qwen2.5-coder:14b model (smallest suitable existing model)
- Proper resource configuration for the 1070's GPU

## Configuration

### Model Selection
- **Selected Model**: `qwen2.5-coder:14b` 
- **Rationale**: Smallest suitable existing model, previously benchmarked and used on 3090
- **Size**: Approximately 15GB (as per ZEUS documentation)
- **Architecture**: 14B parameter model optimized for coding tasks

### Resource Requirements
- **GPU**: NVIDIA GPU with sufficient VRAM (tested on RTX 3090 with 24GB)
- **VRAM**: Minimum ~15GB available for model loading
- **RAM**: Minimum 16GB system RAM recommended

## Commands

### Start the runtime:
```bash
docker-compose up -d
```

### Check container status:
```bash
docker-compose ps
```

### View logs:
```bash
docker-compose logs
```

### Stop the runtime:
```bash
docker-compose down
```

### Validate setup:
```bash
./validate.sh
```

## Validation Process

The validation sequence ensures:
1. Container is running
2. Ollama service is reachable  
3. qwen2.5-coder:14b model is available
4. Model responds to minimal prompt

## Safety Considerations

- Only one model is loaded (no additional inference processes)
- GPU access is properly configured for NVIDIA 1070
- Resource consumption is minimized
- No ZEUS or production components are modified
- No secrets or credentials are included in this configuration

## Transfer to 1070

This configuration is intended to be transferred and used on the physical 1070 host for experimentation. The setup has been tested on the 3090 engineering host to ensure compatibility.