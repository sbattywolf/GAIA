#!/usr/bin/env bash
# Bootstrap GAIA/Alby development environment (bash)
# Usage:
#   ./scripts/install_env.sh        # create venv, install requirements
#   ./scripts/install_env.sh --recreate
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
if [ "${1:-}" = "--recreate" ]; then
  echo "Removing existing venv: $VENV"
  rm -rf "$VENV"
fi
if [ ! -d "$VENV" ]; then
  echo "Creating venv at $VENV"
  python3 -m venv "$VENV"
else
  echo "Using existing venv at $VENV"
fi
# shellcheck source=/dev/null
. "$VENV/bin/activate"
python -m pip install --upgrade pip
REQ="$ROOT/requirements.txt"
if [ -f "$REQ" ]; then
  pip install -r "$REQ"
else
  echo "requirements.txt not found at $REQ"
fi

echo "Bootstrap complete. Activate with: . $VENV/bin/activate"
echo "Quick smoke test: python -c 'import flask; print(\"flask\", __import__(\"flask\").__version__)'"
