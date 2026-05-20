#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Dolpai Player — Release Builder
# Builds all distribution formats and creates a release/ folder
# Usage: bash scripts/build_release.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION=$(python3 -c "import sys; sys.path.insert(0,'$ROOT_DIR'); from version import VERSION; print(VERSION)")
RELEASE_DIR="$ROOT_DIR/release"

CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo -e "${CYAN}"
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║   Dolpai Player — Release Builder v${VERSION}    ║"
echo "  ╚══════════════════════════════════════════════╝"
echo -e "${NC}"

mkdir -p "$RELEASE_DIR"

# ── Step 1: Generate icons ────────────────────────────────────────────────────
echo -e "${CYAN}[1/4] Generating icons...${NC}"
python3 "$SCRIPT_DIR/generate_icons.py"

# ── Step 2: Build .deb ───────────────────────────────────────────────────────
echo -e "${CYAN}[2/4] Building .deb package...${NC}"
if command -v dpkg-deb >/dev/null 2>&1; then
    bash "$ROOT_DIR/packaging/deb/build-deb.sh"
else
    echo -e "${YELLOW}  dpkg-deb not found, skipping .deb build${NC}"
    echo -e "  Install with: sudo apt install dpkg-dev"
fi

# ── Step 3: Build AppImage ────────────────────────────────────────────────────
echo -e "${CYAN}[3/4] Building AppImage...${NC}"
bash "$ROOT_DIR/packaging/appimage/build-appimage.sh" || {
    echo -e "${YELLOW}  AppImage build skipped (appimagetool not available)${NC}"
}

# ── Step 4: Create source tarball ────────────────────────────────────────────
echo -e "${CYAN}[4/4] Creating source tarball...${NC}"
TARBALL="$RELEASE_DIR/dolpai-player-${VERSION}.tar.gz"
tar -czf "$TARBALL" \
    --exclude=".git" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude="release" \
    --exclude="packaging/deb/dolpai-player_*" \
    --exclude="packaging/appimage/AppDir" \
    --exclude="packaging/appimage/appimagetool*" \
    -C "$(dirname "$ROOT_DIR")" \
    "$(basename "$ROOT_DIR")"

echo -e "${GREEN}"
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║   Release build complete!                    ║"
echo "  ╚══════════════════════════════════════════════╝"
echo -e "${NC}"
echo "  Release files in: $RELEASE_DIR"
echo ""
ls -lh "$RELEASE_DIR" 2>/dev/null || true
