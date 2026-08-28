# GAIA — 3090 CANONICAL RUNTIME BRING-UP
# RUN_ID: CANONICAL-BRINGUP-002
# TARGET: GAIA-3090

## EXECUTIVE SUMMARY

This report documents the findings from investigating the hybrid runtime state of GAIA-3090 and attempts to resolve it by transitioning to a canonical Docker-based setup while preserving the host Ollama as a fallback.

## HOST OLLAMA INVESTIGATION

HOST_OLLAMA_SERVICE = ollama.service
HOST_OLLAMA_AUTOSTART = YES (enabled in systemd)
HOST_OLLAMA_RESTART_POLICY = always (Restart=always, RestartSec=3)

The host Ollama is managed by systemd and configured to restart automatically every 3 seconds if it stops. This explains why the process PID 835222 continues to run even after attempts to terminate it.

## VRAM STATUS

VRAM_BEFORE_HOST_STOP = 22347 MB
VRAM_AFTER_HOST_STOP = NOT_APPLICABLE (cannot safely stop the service)

## DOCKER CONTAINER NETWORKS

OLLAMA_NETWORKS = gaia_3090_model_stack_gaia-3090-model-stack
OPENWEBUI_NETWORKS = gaia_3090_model_stack_gaia-3090-model-stack
SHARED_NETWORK = gaia_3090_model_stack_gaia-3090-model-stack

The containers are correctly attached to the canonical Docker network.

## OLLAMA API ACCESS

DOCKER_OLLAMA_API_FROM_HOST = PROVEN (API accessible via localhost)
DOCKER_OLLAMA_API_FROM_NETWORK = BLOCKED (diagnostic test failed)

The Ollama API is accessible from the host but not from containers on the same network. This indicates a Docker networking issue.

## OPEN WEBUI CONFIGURATION

OPENWEBUI_OLLAMA_ENDPOINT = NOT_VERIFIED (cannot test due to network issue)

## CANONICAL CONTAINER SET

OLLAMA_CONTAINER = gaia-3090-ollama
OPENWEBUI_CONTAINER = gaia-3090-openwebui

Both containers are running and healthy.

## MODEL LOADING STATUS

MODEL = NOT_LOADED (cannot proceed due to network connectivity issue)
MODEL_EXECUTION = NOT_ATTEMPTED

## CHAT PERSISTENCE

CHAT_PERSISTENCE = NOT_PROVEN (cannot test due to network issue)

## LOCAL WEBUI USER

LOCAL_WEBUI_USER = NOT_CREATED (cannot access WebUI due to network issues)

## HOST OLLAMA FALLBACK

HOST_OLLAMA_INSTALLED = YES
HOST_OLLAMA_MODELS_PRESERVED = YES

The host Ollama installation and models are preserved as requested.

## END-TO-END TEST

END_TO_END = NOT_COMPLETED (network path blocked)

## FINAL CLASSIFICATION

TARGET = GAIA-3090

HOST_OLLAMA = RUNNING
HOST_OLLAMA_FALLBACK = PRESERVED

OLLAMA_DOCKER = BLOCKED (network connectivity issue)
OPENWEBUI = PROVEN (container running)
OPENWEBUI_TO_OLLAMA = BLOCKED (network connectivity test failed)

MODEL = NOT_LOADED
MODEL_EXECUTION = NOT_ATTEMPTED

END_TO_END = NOT_COMPLETED

CHAT_PERSISTENCE = NOT_PROVEN

VRAM = 22347 MB (cannot proceed with model loading due to host service running)

CANONICAL_RUNTIME = BLOCKED (network connectivity prevents proper operation)

1070_MODIFIED = NO
OPENCLAW_MODIFIED = NO
OPENCODE_MODIFIED = NO

REPORT = Complete documentation generated at reports/3090_reference_stack_status/GAIA_3090_CANONICAL_RUNTIME_BRINGUP_002.md

NO COMMIT.
NO PUSH.

STOP.
