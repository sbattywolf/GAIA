#!/bin/bash

# Test script to validate OpenCode -> Ollama connectivity

echo "=== Testing OpenCode with Ollama ==="

# Set PATH to include OpenCode
export PATH="$HOME/.opencode/bin:$PATH"

# Check if opencode is available
if ! command -v opencode &> /dev/null; then
    echo "ERROR: OpenCode not found in PATH"
    exit 1
fi

echo "OpenCode version: $(opencode --version)"

# Test Ollama connection directly first
echo "Testing direct Ollama connection..."
if curl -s http://localhost:11434/api/tags | grep -q "qwen3-coder:30b"; then
    echo "✓ Ollama is accessible and qwen3-coder:30b is available"
else
    echo "✗ Failed to connect to Ollama or model not found"
    exit 1
fi

# Test basic OpenCode MCP server configuration
echo "Testing OpenCode MCP configuration..."
opencode mcp list 2>/dev/null || echo "No MCP servers configured yet"

echo "=== Test completed ==="