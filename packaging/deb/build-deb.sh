#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Dolpai Player — .deb Package Builder
# Produces: dolpai-player_1.0.0_all.deb
# Requirements: sudo apt install dpkg-dev
# ─────────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
VERSION="1.0.0"
PKG_DIR="$SCRIPT_DIR/dolpai-player_${VERSION}_all"
OUTPUT_DIR="$ROOT_DIR/release"

CYAN='\033[0;36m'; GREEN='\033[0;32m'; NC='\033[0m'

echo -e "${CYAN}Building dolpai-player_${VERSION}_all.deb...${NC}"

# ── Build directory structure ─────────────────────────────────────────────────
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/lib/dolpai-player"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/usr/share/metainfo"
mkdir -p "$OUTPUT_DIR"

# Icon sizes
for size in 16 22 24 32 48 64 96 128 256 512; do
    mkdir -p "$PKG_DIR/usr/share/icons/hicolor/${size}x${size}/apps"
done
mkdir -p "$PKG_DIR/usr/share/icons/hicolor/scalable/apps"

# ── DEBIAN control files ──────────────────────────────────────────────────────
cp "$SCRIPT_DIR/DEBIAN/control"  "$PKG_DIR/DEBIAN/control"
cp "$SCRIPT_DIR/DEBIAN/postinst" "$PKG_DIR/DEBIAN/postinst"
cp "$SCRIPT_DIR/DEBIAN/postrm"   "$PKG_DIR/DEBIAN/postrm"
chmod 755 "$PKG_DIR/DEBIAN/postinst" "$PKG_DIR/DEBIAN/postrm"

# ── Application files ─────────────────────────────────────────────────────────
cp "$ROOT_DIR/main.py"    "$PKG_DIR/usr/lib/dolpai-player/"
cp "$ROOT_DIR/version.py" "$PKG_DIR/usr/lib/dolpai-player/"
cp -r "$ROOT_DIR/ui"      "$PKG_DIR/usr/lib/dolpai-player/"
cp -r "$ROOT_DIR/player"  "$PKG_DIR/usr/lib/dolpai-player/"
cp -r "$ROOT_DIR/assets"  "$PKG_DIR/usr/lib/dolpai-player/"

# Remove __pycache__ from package
find "$PKG_DIR" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PKG_DIR" -name "*.pyc"       -delete 2>/dev/null || true

# ── Launcher ─────────────────────────────────────────────────────────────────
cp "$SCRIPT_DIR/usr/bin/dolpai-player" "$PKG_DIR/usr/bin/dolpai-player"
chmod 755 "$PKG_DIR/usr/bin/dolpai-player"

# ── Desktop + metadata ────────────────────────────────────────────────────────
cp "$SCRIPT_DIR/usr/share/applications/dolpai-player.desktop" \
   "$PKG_DIR/usr/share/applications/"
cp "$ROOT_DIR/packaging/appstream/io.github.dolpaii.dolpai_player.metainfo.xml" \
   "$PKG_DIR/usr/share/metainfo/"

# ── Icons ─────────────────────────────────────────────────────────────────────
for size in 16 22 24 32 48 64 96 128 256 512; do
    src="$ROOT_DIR/assets/icons/hicolor/${size}x${size}/apps/dolpai-player.png"
    if [ -f "$src" ]; then
        cp "$src" "$PKG_DIR/usr/share/icons/hicolor/${size}x${size}/apps/dolpai-player.png"
    fi
done
cp "$ROOT_DIR/assets/icons/hicolor/scalable/apps/dolpai-player.svg" \
   "$PKG_DIR/usr/share/icons/hicolor/scalable/apps/dolpai-player.svg"

# ── Build .deb ────────────────────────────────────────────────────────────────
dpkg-deb --build --root-owner-group "$PKG_DIR" \
         "$OUTPUT_DIR/dolpai-player_${VERSION}_all.deb"

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  .deb package built successfully!                    ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo "  Output: $OUTPUT_DIR/dolpai-player_${VERSION}_all.deb"
echo "  Size:   $(du -sh "$OUTPUT_DIR/dolpai-player_${VERSION}_all.deb" | cut -f1)"
echo ""
echo "  Install with:"
echo "    sudo dpkg -i dolpai-player_${VERSION}_all.deb"
echo "    sudo apt-get install -f   # fix any missing deps"
