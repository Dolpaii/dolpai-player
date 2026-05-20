#!/usr/bin/env bash
# Dolpai Player - Quick launcher
# Usage: bash run.sh [/path/to/video.mp4]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate venv if it exists (created by install.sh --venv mode)
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

exec python3 "$SCRIPT_DIR/main.py" "$@"
