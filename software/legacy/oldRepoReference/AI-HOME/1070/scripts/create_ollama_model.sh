#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
docker exec ollama ollama pull qwen3:8b
docker cp "$BASE/models/zeus-edge/Modelfile" ollama:/tmp/ZeusModelfile
docker exec ollama ollama create zeus-edge:1 -f /tmp/ZeusModelfile
