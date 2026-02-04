#!/usr/bin/env bash
set -euo pipefail

token="${1:-}"
if [ -z "$token" ]; then
  echo "Usage: $0 <token>" >&2
  exit 2
fi

# Default endpoint: GitHub API user (useful if token is a PAT). Set SMOKE_ENDPOINT to override.
endpoint="${SMOKE_ENDPOINT:-https://api.github.com/user}"

echo "Running smoke check against $endpoint"
status=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $token" "$endpoint" || echo "000")
if [ "$status" = "200" ]; then
  echo "Smoke check OK (HTTP 200)"
  exit 0
else
  echo "Smoke check failed: HTTP $status"
  exit 3
fi
