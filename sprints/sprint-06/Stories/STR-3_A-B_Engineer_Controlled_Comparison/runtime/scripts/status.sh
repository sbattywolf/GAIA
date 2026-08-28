#!/bin/bash

# GAIA 3090 Model Serving Stack - Status Script
#
# Checks the status of the canonical 3090 model-serving stack.

echo "Checking GAIA 3090 Model Serving Stack status..."

# Change to the directory containing this script
cd "$(dirname "$0")/.."

# Check if the canonical stack is running
if docker compose -f compose.yaml ps --format "table {{.Names}}\t{{.Status}}" | grep -q "gaia-3090"; then
    echo "Canonical 3090 stack is running:"
    docker compose -f compose.yaml ps --format "table {{.Names}}\t{{.Status}}"
else
    echo "Canonical 3090 stack is not running"
fi

# Check for any legacy containers that might interfere
echo ""
echo "Legacy containers (if any):"
docker ps -a --filter "name=gaia-ollama-1070\|open-webui-temp" --format "table {{.Names}}\t{{.Status}}"
