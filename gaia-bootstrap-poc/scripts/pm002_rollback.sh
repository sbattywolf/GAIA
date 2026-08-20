#!/usr/bin/env bash
set -euo pipefail
STATE_DIR="${GAIA_PM002_STATE_DIR:-${TMPDIR:-/tmp}/gaia-pm002}"
mkdir -p "${STATE_DIR}"
rm -f "${STATE_DIR}/disabled"
rm -f "${STATE_DIR}/ready"
printf 'enabled\n' > "${STATE_DIR}/state"
echo "PM-002 restored to the known-good enabled state; no external read performed."
