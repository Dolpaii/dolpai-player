#!/usr/bin/env bash
# Dolpai Player — universal launcher
# Works from: direct run, .deb install, snap (via bin/launcher wrapper)

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

# If running inside a snap, SNAP is set by snapd
if [ -n "$SNAP" ]; then
    export PYTHONPATH="$SNAP/usr/lib/python3/dist-packages"
    export VLC_PLUGIN_PATH="$SNAP/usr/lib/x86_64-linux-gnu/vlc/plugins"
    export XDG_CONFIG_HOME="${SNAP_USER_COMMON}/.config"
    exec python3 "$SNAP/app/main.py" "$@"
fi

# If running from a venv
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

exec python3 "$SCRIPT_DIR/main.py" "$@"
