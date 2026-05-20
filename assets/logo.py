"""
Dolpai Player - Embedded Logo
SVG logo rendered to QPixmap at runtime — no external image files needed.
Requires: python3-pyqt6.qtsvg  (apt install python3-pyqt6.qtsvg)
"""

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QByteArray


# Stylised "D" with a dolphin-wave arc and neon cyan/blue gradient
LOGO_SVG = b"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="#00d4ff" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#0a0a0f" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="dGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#0080ff"/>
      <stop offset="100%" stop-color="#00d4ff"/>
    </linearGradient>
  </defs>

  <!-- Soft background glow -->
  <circle cx="60" cy="60" r="55" fill="url(#glow)"/>

  <!-- Outer decorative ring -->
  <circle cx="60" cy="60" r="52" fill="none"
          stroke="#00d4ff" stroke-width="1" stroke-opacity="0.3"/>

  <!-- Main D letterform -->
  <path d="M 32 25 L 32 95 L 55 95
           C 80 95 92 80 92 60
           C 92 40 80 25 55 25 Z"
        fill="none" stroke="url(#dGrad)" stroke-width="5"
        stroke-linejoin="round" stroke-linecap="round"/>

  <!-- Inner D echo -->
  <path d="M 44 38 L 44 82 L 54 82
           C 72 82 80 72 80 60
           C 80 48 72 38 54 38 Z"
        fill="none" stroke="#00d4ff" stroke-width="1.5" stroke-opacity="0.35"
        stroke-linejoin="round"/>

  <!-- Dolphin wave arc -->
  <path d="M 44 60 Q 55 48 66 60 Q 77 72 88 60"
        fill="none" stroke="#00d4ff" stroke-width="2.5"
        stroke-linecap="round" stroke-opacity="0.9"/>

  <!-- Centre dot -->
  <circle cx="60" cy="60" r="3"  fill="#00d4ff" opacity="0.85"/>
  <circle cx="60" cy="60" r="6"  fill="none" stroke="#00d4ff"
          stroke-width="1" opacity="0.3"/>

  <!-- Cardinal tick marks -->
  <line x1="60" y1="10"  x2="60" y2="18"  stroke="#00d4ff" stroke-width="1.5" stroke-opacity="0.45"/>
  <line x1="60" y1="102" x2="60" y2="110" stroke="#00d4ff" stroke-width="1.5" stroke-opacity="0.45"/>
  <line x1="10" y1="60"  x2="18" y2="60"  stroke="#00d4ff" stroke-width="1.5" stroke-opacity="0.45"/>
  <line x1="102" y1="60" x2="110" y2="60" stroke="#00d4ff" stroke-width="1.5" stroke-opacity="0.45"/>
</svg>
"""


def get_logo_pixmap(size: int = 80) -> QPixmap:
    """Render the SVG logo to a QPixmap at the requested pixel size."""
    try:
        from PyQt6.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(QByteArray(LOGO_SVG))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.end()
        return pixmap
    except ImportError:
        # Fallback: plain coloured square if QtSvg is not installed
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        from PyQt6.QtGui import QColor, QBrush
        from PyQt6.QtCore import QRectF
        painter.setBrush(QBrush(QColor("#0a0a0f")))
        painter.setPen(QColor("#00d4ff"))
        painter.drawRoundedRect(QRectF(2, 2, size - 4, size - 4), 8, 8)
        from PyQt6.QtGui import QFont
        font = QFont("monospace", size // 4, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#00d4ff"))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "D")
        painter.end()
        return pixmap


def get_window_icon():
    """Return a QIcon suitable for the window title bar."""
    from PyQt6.QtGui import QIcon
    return QIcon(get_logo_pixmap(64))
