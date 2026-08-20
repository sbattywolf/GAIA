#!/usr/bin/env bash
set -euo pipefail
STATE_DIR="${GAIA_PM002_STATE_DIR:-${TMPDIR:-/tmp}/gaia-pm002}"
mkdir -p "${STATE_DIR}"
rm -f "${STATE_DIR}/ready"
printf 'disabled\n' > "${STATE_DIR}/disabled"
echo "PM-002 disabled; future start/read commands are blocked."
