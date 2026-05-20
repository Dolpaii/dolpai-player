"""
Dolpai Player - Recent Videos Manager
Persists and retrieves recently played video paths using a JSON file.
"""

import json
import os
from pathlib import Path


# Store recent videos in ~/.config/dolpai-player/
CONFIG_DIR = Path.home() / ".config" / "dolpai-player"
RECENT_FILE = CONFIG_DIR / "recent.json"
MAX_RECENT = 20


def _ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_recent() -> list[str]:
    """Load the list of recent video paths. Returns [] if none saved."""
    _ensure_config_dir()
    if not RECENT_FILE.exists():
        return []
    try:
        with open(RECENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Filter out paths that no longer exist
        return [p for p in data if os.path.isfile(p)]
    except (json.JSONDecodeError, OSError):
        return []


def save_recent(paths: list[str]):
    """Persist the recent video list to disk."""
    _ensure_config_dir()
    try:
        with open(RECENT_FILE, "w", encoding="utf-8") as f:
            json.dump(paths[:MAX_RECENT], f, indent=2)
    except OSError:
        pass  # Non-critical — silently ignore write errors


def add_recent(path: str) -> list[str]:
    """
    Add a video path to the top of the recent list.
    Removes duplicates and trims to MAX_RECENT.
    Returns the updated list.
    """
    recent = load_recent()
    # Remove if already present (move to top)
    recent = [p for p in recent if p != path]
    recent.insert(0, path)
    recent = recent[:MAX_RECENT]
    save_recent(recent)
    return recent


def clear_recent():
    """Clear all recent videos."""
    save_recent([])
