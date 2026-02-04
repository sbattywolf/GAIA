#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-127.0.0.1}
PORT=${2:-5432}
TRIES=${3:-30}

echo "Waiting for Postgres at ${HOST}:${PORT} (up to ${TRIES} tries)"
for i in $(seq 1 $TRIES); do
  if pg_isready -h "$HOST" -p "$PORT" >/dev/null 2>&1; then
    echo "Postgres is ready"
    exit 0
  fi
  sleep 2
done

echo "Postgres did not become ready in time" >&2
exit 1
