#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Dolpai Player — AppImage Builder
# Produces: DolpaiPlayer-1.0.0-x86_64.AppImage
#
# Requirements:
#   sudo apt install python3 python3-pyqt6 python3-pyqt6.qtsvg python3-vlc vlc ffmpeg
#   wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
# ─────────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$SCRIPT_DIR/AppDir"
VERSION="1.0.0"
OUTPUT="$ROOT_DIR/release/DolpaiPlayer-${VERSION}-x86_64.AppImage"

CYAN='\033[0;36m'; GREEN='\033[0;32m'; NC='\033[0m'

echo -e "${CYAN}Building Dolpai Player AppImage v${VERSION}...${NC}"

# ── Clean previous build ──────────────────────────────────────────────────────
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/lib/dolpai-player"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/metainfo"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/scalable/apps"
mkdir -p "$ROOT_DIR/release"

# ── Copy application source ───────────────────────────────────────────────────
echo -e "${CYAN}[1/5] Copying application files...${NC}"
cp "$ROOT_DIR/main.py"    "$BUILD_DIR/usr/lib/dolpai-player/"
cp "$ROOT_DIR/version.py" "$BUILD_DIR/usr/lib/dolpai-player/"
cp -r "$ROOT_DIR/ui"      "$BUILD_DIR/usr/lib/dolpai-player/"
cp -r "$ROOT_DIR/player"  "$BUILD_DIR/usr/lib/dolpai-player/"
cp -r "$ROOT_DIR/assets"  "$BUILD_DIR/usr/lib/dolpai-player/"

# ── Launcher script ───────────────────────────────────────────────────────────
echo -e "${CYAN}[2/5] Creating launcher...${NC}"
cat > "$BUILD_DIR/usr/bin/dolpai-player" << 'LAUNCHER'
#!/usr/bin/env bash
SELF="$(readlink -f "$0")"
HERE="${SELF%/*}"
export PYTHONPATH="$HERE/../lib/dolpai-player:$PYTHONPATH"
exec python3 "$HERE/../lib/dolpai-player/main.py" "$@"
LAUNCHER
chmod +x "$BUILD_DIR/usr/bin/dolpai-player"

# ── Desktop + metadata ────────────────────────────────────────────────────────
echo -e "${CYAN}[3/5] Installing desktop integration...${NC}"
cp "$ROOT_DIR/dolpai-player.desktop" \
   "$BUILD_DIR/usr/share/applications/dolpai-player.desktop"
cp "$ROOT_DIR/packaging/appstream/io.github.dolpaii.dolpai_player.metainfo.xml" \
   "$BUILD_DIR/usr/share/metainfo/"

# ── Icons ─────────────────────────────────────────────────────────────────────
echo -e "${CYAN}[4/5] Installing icons...${NC}"
cp "$ROOT_DIR/assets/icons/hicolor/256x256/apps/dolpai-player.png" \
   "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/dolpai-player.png"
cp "$ROOT_DIR/assets/icons/hicolor/scalable/apps/dolpai-player.svg" \
   "$BUILD_DIR/usr/share/icons/hicolor/scalable/apps/dolpai-player.svg"

# AppImage requires icon + desktop at root of AppDir
cp "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/dolpai-player.png" \
   "$BUILD_DIR/dolpai-player.png"
cp "$BUILD_DIR/usr/share/applications/dolpai-player.desktop" \
   "$BUILD_DIR/dolpai-player.desktop"

# AppRun entry point
cat > "$BUILD_DIR/AppRun" << 'APPRUN'
#!/usr/bin/env bash
SELF="$(readlink -f "$0")"
HERE="${SELF%/*}"
export PYTHONPATH="$HERE/usr/lib/dolpai-player:$PYTHONPATH"
exec python3 "$HERE/usr/lib/dolpai-player/main.py" "$@"
APPRUN
chmod +x "$BUILD_DIR/AppRun"

# ── Build AppImage ────────────────────────────────────────────────────────────
echo -e "${CYAN}[5/5] Building AppImage...${NC}"

APPIMAGETOOL="$SCRIPT_DIR/appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
    echo "Downloading appimagetool..."
    wget -q "https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage" \
         -O "$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
fi

ARCH=x86_64 "$APPIMAGETOOL" "$BUILD_DIR" "$OUTPUT"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  AppImage built successfully!                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "  Output: $OUTPUT"
echo "  Size:   $(du -sh "$OUTPUT" | cut -f1)"
echo ""
echo "  Users can run it with:"
echo "    chmod +x DolpaiPlayer-${VERSION}-x86_64.AppImage"
echo "    ./DolpaiPlayer-${VERSION}-x86_64.AppImage"
