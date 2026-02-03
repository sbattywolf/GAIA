#!/usr/bin/env bash
# Install GAIA systemd unit for session runner.
# Usage: sudo ./scripts/install_gaia_service.sh /path/to/GAIA [service_user]

set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 /path/to/GAIA [service_user]" >&2
  exit 2
fi

GAIA_PATH="$1"
SERVICE_USER="${2:-$(whoami)}"
SERVICE_NAME="gaia_session.service"
UNIT_SRC="$GAIA_PATH/scripts/gaia_session.service"
UNIT_DST="/etc/systemd/system/$SERVICE_NAME"

if [ ! -f "$UNIT_SRC" ]; then
  echo "Unit template not found at $UNIT_SRC" >&2
  exit 2
fi

if [ $(id -u) -ne 0 ]; then
  echo "This script must be run as root (sudo) to install systemd unit." >&2
  exit 2
fi

# copy and inline paths
sed \
  -e "s|/path/to/GAIA|$GAIA_PATH|g" \
  -e "s|Environment=PYTHONPATH=/path/to/GAIA|Environment=PYTHONPATH=$GAIA_PATH|g" \
  -e "s|EnvironmentFile=/path/to/GAIA/.tmp/telegram.env|EnvironmentFile=$GAIA_PATH/.tmp/telegram.env|g" \
  "$UNIT_SRC" > "$UNIT_DST"

systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"
echo "Installed and started $SERVICE_NAME"
echo "Check status: systemctl status $SERVICE_NAME" 
