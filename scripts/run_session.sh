#!/usr/bin/env bash
# Launcher for GAIA session_progress_runner
# Ensures single-instance via PID file, rotates logs, and runs the runner with PYTHONPATH set.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PIDFILE="$ROOT/.tmp/session_progress.pid"
LOGDIR="$ROOT/.tmp/logs"
LOGFILE="$LOGDIR/session_progress.log"
ENVFILE="$ROOT/.tmp/telegram.env"
PYTHON_EXEC="$(which python3 || which python)"

mkdir -p "$ROOT/.tmp"
mkdir -p "$LOGDIR"

if [ -f "$PIDFILE" ]; then
  oldpid=$(cat "$PIDFILE" 2>/dev/null || echo "")
  if [ -n "$oldpid" ]; then
    if kill -0 "$oldpid" 2>/dev/null; then
      echo "session_progress_runner already running (pid=$oldpid)" >&2
      exit 0
    else
      echo "stale pidfile found, removing" >&2
      rm -f "$PIDFILE"
    fi
  fi
fi

# rotate log if >5MB
if [ -f "$LOGFILE" ] && [ $(stat -c%s "$LOGFILE") -gt $((5*1024*1024)) ]; then
  mv "$LOGFILE" "$LOGFILE.$(date +%Y%m%dT%H%M%S)"
fi

echo "Starting session_progress_runner..." >> "$LOGFILE"

export PYTHONPATH="$ROOT"
if [ -f "$ENVFILE" ]; then
  # load simple KEY=VALUE lines into environment for the process
  set -a
  # shellcheck disable=SC1090
  . "$ENVFILE"
  set +a
fi

nohup "$PYTHON_EXEC" "$ROOT/scripts/session_progress_runner.py" --interval 600 --duration 3600 >> "$LOGFILE" 2>&1 &
pid=$!
echo $pid > "$PIDFILE"
echo "session_progress_runner started pid=$pid" >> "$LOGFILE"

exit 0
