#!/usr/bin/env bash
# Robust daemon runner: restart on exit, log to comms/daemon.stdout.log
COMMS_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$COMMS_DIR/../.." && pwd)"
PYTHON="$ROOT_DIR/.venv/Scripts/python.exe"
DAEMON="$COMMS_DIR/daemon.py"
LOG="$COMMS_DIR/daemon.stdout.log"

while true; do
    echo "[run_daemon] starting daemon at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
    "$PYTHON" "$DAEMON" --loop --interval 30 >> "$LOG" 2>&1
    EXIT=$?
    echo "[run_daemon] daemon exited with code $EXIT at $(date -u +%Y-%m-%dT%H:%M:%SZ); restarting in 5s" >> "$LOG"
    sleep 5
done
