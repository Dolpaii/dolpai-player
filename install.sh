#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Dolpai Player — Ubuntu/Linux Installer
# Tested on Ubuntu 22.04 / 24.04 / 25.04
# Usage:  bash install.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ██████╗  ██████╗ ██╗     ██████╗  █████╗ ██╗"
echo "  ██╔══██╗██╔═══██╗██║     ██╔══██╗██╔══██╗██║"
echo "  ██║  ██║██║   ██║██║     ██████╔╝███████║██║"
echo "  ██║  ██║██║   ██║██║     ██╔═══╝ ██╔══██║██║"
echo "  ██████╔╝╚██████╔╝███████╗██║     ██║  ██║██║"
echo "  ╚═════╝  ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝"
echo -e "  PLAYER  v1.0.0${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── 1. System packages ────────────────────────────────────────────────────────
echo -e "${CYAN}[1/3] Installing system packages...${NC}"
sudo apt-get update -qq
sudo apt-get install -y \
    python3 \
    python3-pyqt6 \
    python3-pyqt6.qtsvg \
    python3-vlc \
    vlc \
    ffmpeg \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    --no-install-recommends

echo -e "${GREEN}      ✓ System packages installed${NC}"

# ── 2. Verify Python imports work ─────────────────────────────────────────────
echo -e "${CYAN}[2/3] Verifying Python dependencies...${NC}"

python3 - <<'PYCHECK'
import sys
errors = []

try:
    import PyQt6.QtWidgets
except ImportError as e:
    errors.append(f"PyQt6: {e}")

try:
    import PyQt6.QtSvg
except ImportError as e:
    errors.append(f"PyQt6.QtSvg: {e}")

try:
    import vlc
except ImportError as e:
    errors.append(f"python-vlc: {e}")

if errors:
    print("MISSING DEPENDENCIES:")
    for err in errors:
        print(f"  ✗ {err}")
    sys.exit(1)
else:
    print("  ✓ PyQt6 OK")
    print("  ✓ PyQt6.QtSvg OK")
    print("  ✓ python-vlc OK")
PYCHECK

echo -e "${GREEN}      ✓ All dependencies verified${NC}"

# ── 3. Desktop launcher ───────────────────────────────────────────────────────
echo -e "${CYAN}[3/3] Installing desktop launcher...${NC}"

DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/128x128/apps"
DESKTOP_FILE="$DESKTOP_DIR/dolpai-player.desktop"

mkdir -p "$DESKTOP_DIR" "$ICON_DIR"

# Generate a simple PNG icon using Python (no external tools needed)
python3 - "$ICON_DIR/dolpai-player.png" <<'PYICON'
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QPen, QFont
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtSvg import QSvgRenderer

app = QApplication(sys.argv)
output_path = sys.argv[1]

SVG = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="24" fill="#0a0a0f"/>
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0080ff"/>
      <stop offset="100%" stop-color="#00d4ff"/>
    </linearGradient>
  </defs>
  <path d="M 34 26 L 34 102 L 58 102 C 86 102 98 84 98 64 C 98 44 86 26 58 26 Z"
        fill="none" stroke="url(#g)" stroke-width="6"
        stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M 46 64 Q 58 50 70 64 Q 82 78 94 64"
        fill="none" stroke="#00d4ff" stroke-width="3"
        stroke-linecap="round"/>
  <circle cx="64" cy="64" r="4" fill="#00d4ff"/>
</svg>
"""

renderer = QSvgRenderer(QByteArray(SVG))
pixmap = QPixmap(128, 128)
pixmap.fill(Qt.GlobalColor.transparent)
painter = QPainter(pixmap)
painter.setRenderHint(QPainter.RenderHint.Antialiasing)
renderer.render(painter)
painter.end()
pixmap.save(output_path, "PNG")
print(f"  ✓ Icon saved to {output_path}")
PYICON

# Write .desktop file
cat > "$DESKTOP_FILE" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=Dolpai Player
GenericName=Video Player
Comment=Futuristic cyberpunk video player powered by VLC
Exec=python3 ${SCRIPT_DIR}/main.py %F
Icon=dolpai-player
Terminal=false
Categories=AudioVideo;Video;Player;GTK;
MimeType=video/mp4;video/x-matroska;video/x-msvideo;video/quicktime;video/webm;video/x-flv;video/mpeg;video/ogg;
Keywords=video;player;vlc;media;
StartupNotify=true
StartupWMClass=dolpai-player
DESKTOP

chmod +x "$DESKTOP_FILE"

# Register MIME types and update icon cache
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
xdg-mime default dolpai-player.desktop video/mp4 2>/dev/null || true

echo -e "${GREEN}      ✓ Desktop launcher installed${NC}"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Dolpai Player installed successfully!  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Launch:  ${CYAN}python3 ${SCRIPT_DIR}/main.py${NC}"
echo -e "  Or:      ${CYAN}bash ${SCRIPT_DIR}/run.sh${NC}"
echo -e "  Or search 'Dolpai' in your app launcher"
echo ""
