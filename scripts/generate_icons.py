"""
Dolpai Player — Icon Generator
Generates PNG icons at all required sizes for Linux desktop integration.
Run: python3 scripts/generate_icons.py

Output: assets/icons/hicolor/<size>x<size>/apps/dolpai-player.png
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtSvg import QSvgRenderer

# All sizes required by the hicolor icon theme spec
ICON_SIZES = [16, 22, 24, 32, 48, 64, 96, 128, 256, 512]

LOGO_SVG = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#0f0f1a"/>
      <stop offset="100%" stop-color="#0a0a0f"/>
    </radialGradient>
    <linearGradient id="dg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#0080ff"/>
      <stop offset="100%" stop-color="#00d4ff"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#00d4ff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#00d4ff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- App background -->
  <rect width="512" height="512" rx="96" fill="url(#bg)"/>

  <!-- Glow -->
  <circle cx="256" cy="256" r="220" fill="url(#glow)"/>

  <!-- Outer ring -->
  <circle cx="256" cy="256" r="210" fill="none"
          stroke="#00d4ff" stroke-width="3" stroke-opacity="0.35"/>

  <!-- Main D letterform -->
  <path d="M 130 100 L 130 412 L 230 412
           C 360 412 400 340 400 256
           C 400 172 360 100 230 100 Z"
        fill="none" stroke="url(#dg)" stroke-width="22"
        stroke-linejoin="round" stroke-linecap="round"/>

  <!-- Inner D echo -->
  <path d="M 180 158 L 180 354 L 228 354
           C 316 354 348 308 348 256
           C 348 204 316 158 228 158 Z"
        fill="none" stroke="#00d4ff" stroke-width="6" stroke-opacity="0.3"
        stroke-linejoin="round"/>

  <!-- Dolphin wave arc -->
  <path d="M 180 256 Q 230 196 280 256 Q 330 316 380 256"
        fill="none" stroke="#00d4ff" stroke-width="11"
        stroke-linecap="round" stroke-opacity="0.95"/>

  <!-- Centre dot -->
  <circle cx="256" cy="256" r="14" fill="#00d4ff" opacity="0.9"/>
  <circle cx="256" cy="256" r="26" fill="none"
          stroke="#00d4ff" stroke-width="3" opacity="0.3"/>

  <!-- Cardinal ticks -->
  <line x1="256" y1="42"  x2="256" y2="74"  stroke="#00d4ff" stroke-width="5" stroke-opacity="0.4"/>
  <line x1="256" y1="438" x2="256" y2="470" stroke="#00d4ff" stroke-width="5" stroke-opacity="0.4"/>
  <line x1="42"  y1="256" x2="74"  y2="256" stroke="#00d4ff" stroke-width="5" stroke-opacity="0.4"/>
  <line x1="438" y1="256" x2="470" y2="256" stroke="#00d4ff" stroke-width="5" stroke-opacity="0.4"/>
</svg>
"""


def generate_icons():
    app = QApplication.instance() or QApplication(sys.argv)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_base = os.path.join(base, "assets", "icons", "hicolor")

    renderer = QSvgRenderer(QByteArray(LOGO_SVG))

    for size in ICON_SIZES:
        out_dir = os.path.join(icons_base, f"{size}x{size}", "apps")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "dolpai-player.png")

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.end()
        pixmap.save(out_path, "PNG")
        print(f"  ✓  {size:>3}x{size:<3}  →  {out_path}")

    # Also write a scalable SVG
    svg_dir = os.path.join(icons_base, "scalable", "apps")
    os.makedirs(svg_dir, exist_ok=True)
    svg_path = os.path.join(svg_dir, "dolpai-player.svg")
    with open(svg_path, "wb") as f:
        f.write(LOGO_SVG)
    print(f"  ✓  SVG      →  {svg_path}")

    print(f"\nAll icons written to: assets/icons/hicolor/")


if __name__ == "__main__":
    generate_icons()
