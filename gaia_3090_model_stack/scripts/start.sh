#!/bin/bash

# GAIA 3090 Model Serving Stack - Start Script
#
# Starts the canonical 3090 model-serving stack.
# This script ensures only the canonical containers are started.

set -e

echo "Starting GAIA 3090 Model Serving Stack..."

# Change to the directory containing this script
cd "$(dirname "$0")/.."

# Start the canonical stack using Docker Compose
docker compose -f compose.yaml up -d

echo "GAIA 3090 Model Serving Stack started successfully."
echo "Open WebUI at: http://localhost:3000"
echo "Ollama API at: http://localhost:11434"
