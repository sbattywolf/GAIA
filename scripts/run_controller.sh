#!/usr/bin/env bash
# Simple launcher for GAIA controller (for local testing / MyNAS wrapper)
set -euo pipefail
ROOT_DIR="/opt/gaia"
if [ -d "." ] && [ -f "agents/controller_agent.py" ]; then
  ROOT_DIR=$(pwd)
fi
VENV="$ROOT_DIR/.venv"
if [ -d "$VENV" ]; then
  PY="$VENV/bin/python"
else
  PY="python"
fi
export CONTROLLER_POLL=${CONTROLLER_POLL:-10}
export CONTROLLER_BATCH=${CONTROLLER_BATCH:-1}
# optionally run in simulate mode by setting CONTROLLER_SIMULATE=1
# ensure local log dir exists for user
HOME_DIR=${HOME:-$(pwd)}
GAIA_LOG_DIR="$HOME_DIR/.local/share/gaia"
mkdir -p "$GAIA_LOG_DIR"
LOGFILE="$GAIA_LOG_DIR/controller.log"
# By default the launcher will write logs to stdout; to persist to a file in the background,
# set `RUN_AS_SERVICE=1` and the script will append to `$LOGFILE` using nohup.
if [ "${CONTROLLER_SIMULATE:-0}" -eq 1 ]; then
  if [ "${RUN_AS_SERVICE:-0}" -eq 1 ]; then
    nohup $PY agents/controller_agent.py --poll ${CONTROLLER_POLL} --simulate >> "$LOGFILE" 2>&1 &
    echo "Controller started (simulate) -> $LOGFILE"
  else
    $PY agents/controller_agent.py --poll ${CONTROLLER_POLL} --simulate
  fi
else
  if [ "${RUN_AS_SERVICE:-0}" -eq 1 ]; then
    nohup $PY agents/controller_agent.py --poll ${CONTROLLER_POLL} >> "$LOGFILE" 2>&1 &
    echo "Controller started -> $LOGFILE"
  else
    $PY agents/controller_agent.py --poll ${CONTROLLER_POLL}
  fi
fi
