#!/bin/bash

echo "=== GAIA 3090 ↔ 1070 Integration Test ==="
echo ""

echo "1. Checking system status:"
echo "   - GAIA-3090 (this system):"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" | head -5
echo ""
echo "   - GAIA-1070 (remote system):"
ssh gaia-1070 "docker ps --format table {{.Names}}t{{.Image}}t{{.Status}}" 2>/dev/null || echo "   Could not connect to GAIA-1070"

echo ""
echo "2. Verifying qwen3:4b availability on 1070:"
ssh gaia-1070 "docker compose exec gaia-1070-ollama ollama list" 2>/dev/null | grep -i qwen3 || echo "   Could not verify model on GAIA-1070"

echo ""
echo "3. Checking OpenClaw versions:"
echo "   - GAIA-3090:"
docker inspect gaia-3090-openclaw | grep -A 1 -B 1 "org.opencontainers.image.version" 2>/dev/null || echo "   Could not determine version"
echo ""
echo "   - GAIA-1070:"
ssh gaia-1070 "docker inspect gaia-1070-openclaw | grep -A 1 -B 1 org.opencontainers.image.version" 2>/dev/null || echo "   Could not determine version"

echo ""
echo "=== Integration Test Complete ==="

