#!/usr/bin/env bash
set -euo pipefail

# Starts mock_token_service for CI usage and waits for health endpoint
PORT=${1:-8001}
python -u scripts/mock_token_service.py --port "$PORT" &
PID=$!
echo "mock_token_service pid=$PID"

for i in $(seq 1 15); do
  if curl -sSf "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
    echo "mock service ready"
    exit 0
  fi
  sleep 1
done

echo "mock service failed to start"
kill $PID || true
exit 1
