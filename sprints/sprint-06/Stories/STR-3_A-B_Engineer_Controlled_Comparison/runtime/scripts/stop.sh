#!/bin/bash

# GAIA 3090 Model Serving Stack - Stop Script
#
# Stops the canonical 3090 model-serving stack.
# This script ensures only the canonical containers are stopped.

set -e

echo "Stopping GAIA 3090 Model Serving Stack..."

# Change to the directory containing this script
cd "$(dirname "$0")/.."

# Stop the canonical stack using Docker Compose
docker compose -f compose.yaml down

echo "GAIA 3090 Model Serving Stack stopped successfully."
