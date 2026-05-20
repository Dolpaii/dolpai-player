"""
Dolpai Player — Store Screenshot Generator
Creates placeholder store screenshots showing the UI design.
Run: python3 scripts/generate_screenshots.py

Output: assets/screenshots/*.png
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont, QPen
from PyQt6.QtCore import Qt, QRect, QRectF

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "screenshots")


def draw_screenshot(width: int, height: int, title: str, subtitle: str) -> QPixmap:
    """Draw a branded placeholder screenshot."""
    px = QPixmap(width, height)
    px.fill(QColor("#0a0a0f"))

    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    # ── Background gradient ────────────────────────────────────────────
    grad = QLinearGradient(0, 0, 0, height)
    grad.setColorAt(0.0, QColor("#0f0f1a"))
    grad.setColorAt(1.0, QColor("#0a0a0f"))
    p.fillRect(0, 0, width, height, grad)

    # ── Simulated menu bar ─────────────────────────────────────────────
    p.fillRect(0, 0, width, 28, QColor("#0f0f1a"))
    p.setPen(QColor("#1a3a4a"))
    p.drawLine(0, 28, width, 28)
    menu_font = QFont("Ubuntu", 10)
    p.setFont(menu_font)
    p.setPen(QColor("#6a8fa8"))
    for i, item in enumerate(["File", "View", "Playback", "Subtitles"]):
        p.drawText(QRect(10 + i * 80, 0, 70, 28), Qt.AlignmentFlag.AlignCenter, item)

    # ── Recent panel (left sidebar) ────────────────────────────────────
    sidebar_w = 200
    p.fillRect(0, 28, sidebar_w, height - 28, QColor("#0f0f1a"))
    p.setPen(QColor("#1a3a4a"))
    p.drawLine(sidebar_w, 28, sidebar_w, height)

    p.setPen(QColor("#00d4ff"))
    label_font = QFont("Ubuntu", 8, QFont.Weight.Bold)
    p.setFont(label_font)
    p.drawText(QRect(14, 36, sidebar_w - 14, 20), Qt.AlignmentFlag.AlignVCenter, "RECENT")
    p.setPen(QColor("#1a3a4a"))
    p.drawLine(0, 58, sidebar_w, 58)

    recent_font = QFont("Ubuntu", 9)
    p.setFont(recent_font)
    recent_items = ["movie_trailer.mp4", "documentary.mkv", "short_film.avi",
                    "music_video.webm", "lecture.mp4"]
    for i, item in enumerate(recent_items):
        y = 66 + i * 30
        if i == 0:
            p.fillRect(4, y - 2, sidebar_w - 8, 26, QColor("#004466"))
            p.setPen(QColor("#00d4ff"))
        else:
            p.setPen(QColor("#6a8fa8"))
        p.drawText(QRect(12, y, sidebar_w - 20, 22), Qt.AlignmentFlag.AlignVCenter, item)

    # ── Video area ─────────────────────────────────────────────────────
    vx = sidebar_w + 1
    vy = 29
    vw = width - sidebar_w - 1
    vh = height - 29 - 90   # leave room for controls

    p.fillRect(vx, vy, vw, vh, QColor("#000000"))

    # Neon glow border on video area
    pen = QPen(QColor("#00d4ff"))
    pen.setWidth(1)
    p.setPen(pen)
    p.drawRect(vx, vy, vw - 1, vh - 1)

    # Centre logo / title in video area
    cx = vx + vw // 2
    cy = vy + vh // 2

    # Glow circle
    for r, alpha in [(80, 15), (60, 25), (40, 40)]:
        glow = QColor(0, 212, 255, alpha)
        p.setBrush(glow)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(cx - r, cy - r - 30, r * 2, r * 2)

    # D letterform
    p.setPen(QPen(QColor("#00d4ff"), 3))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawArc(cx - 30, cy - 60, 60, 60, 90 * 16, 180 * 16)
    p.drawLine(cx - 30, cy - 60, cx - 30, cy)
    p.drawLine(cx - 30, cy, cx, cy)

    title_font = QFont("Ubuntu", 22, QFont.Weight.Bold)
    p.setFont(title_font)
    p.setPen(QColor("#00d4ff"))
    p.drawText(QRect(vx, cy + 20, vw, 40), Qt.AlignmentFlag.AlignCenter, "DOLPAI PLAYER")

    sub_font = QFont("Ubuntu", 11)
    p.setFont(sub_font)
    p.setPen(QColor("#2a4a5a"))
    p.drawText(QRect(vx, cy + 65, vw, 30), Qt.AlignmentFlag.AlignCenter, subtitle)

    # ── Controls bar ───────────────────────────────────────────────────
    ctrl_y = vy + vh
    ctrl_h = 90
    p.fillRect(vx, ctrl_y, vw, ctrl_h, QColor("#12121f"))
    p.setPen(QColor("#1a3a4a"))
    p.drawLine(vx, ctrl_y, width, ctrl_y)

    # Progress bar track
    bar_x = vx + 12
    bar_y = ctrl_y + 14
    bar_w = vw - 24
    p.fillRect(bar_x, bar_y, bar_w, 4, QColor("#1a2a3a"))

    # Progress fill (30%)
    fill_grad = QLinearGradient(bar_x, 0, bar_x + bar_w, 0)
    fill_grad.setColorAt(0.0, QColor("#0080ff"))
    fill_grad.setColorAt(1.0, QColor("#00d4ff"))
    p.fillRect(bar_x, bar_y, int(bar_w * 0.3), 4, fill_grad)

    # Handle
    handle_x = bar_x + int(bar_w * 0.3) - 7
    p.setBrush(QColor("#00d4ff"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(handle_x, bar_y - 5, 14, 14)

    # Time label
    time_font = QFont("Courier New", 9)
    p.setFont(time_font)
    p.setPen(QColor("#6a8fa8"))
    p.drawText(QRect(width - 120, ctrl_y + 8, 108, 20),
               Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
               "00:42 / 02:18")

    # Control buttons row
    btn_y = ctrl_y + 30
    btn_font = QFont("Ubuntu", 13)
    p.setFont(btn_font)

    # OPEN button
    p.fillRect(vx + 12, btn_y, 70, 30, QColor("#1a1a2e"))
    pen2 = QPen(QColor("#004466"))
    pen2.setWidth(1)
    p.setPen(pen2)
    p.drawRoundedRect(vx + 12, btn_y, 70, 30, 6, 6)
    p.setPen(QColor("#00d4ff"))
    small_font = QFont("Ubuntu", 9, QFont.Weight.Bold)
    p.setFont(small_font)
    p.drawText(QRect(vx + 12, btn_y, 70, 30), Qt.AlignmentFlag.AlignCenter, "⊕  OPEN")

    # Play button (circle)
    play_cx = vx + 130
    play_cy = btn_y + 15
    p.setBrush(QColor("#1a1a2e"))
    p.setPen(QPen(QColor("#004466"), 1))
    p.drawEllipse(play_cx - 18, play_cy - 18, 36, 36)
    p.setPen(QColor("#00d4ff"))
    p.setFont(QFont("Ubuntu", 14))
    p.drawText(QRect(play_cx - 18, play_cy - 18, 36, 36), Qt.AlignmentFlag.AlignCenter, "⏸")

    # Skip buttons
    p.setPen(QColor("#6a8fa8"))
    p.setFont(QFont("Ubuntu", 11))
    p.drawText(QRect(vx + 90, btn_y, 36, 30), Qt.AlignmentFlag.AlignCenter, "⏮")
    p.drawText(QRect(vx + 155, btn_y, 36, 30), Qt.AlignmentFlag.AlignCenter, "⏭")
    p.drawText(QRect(vx + 195, btn_y, 36, 30), Qt.AlignmentFlag.AlignCenter, "⏹")

    # Volume
    p.drawText(QRect(vx + 240, btn_y, 30, 30), Qt.AlignmentFlag.AlignCenter, "🔊")
    p.fillRect(vx + 272, btn_y + 13, 80, 3, QColor("#1a2a3a"))
    p.fillRect(vx + 272, btn_y + 13, 55, 3, QColor("#00d4ff"))
    p.setBrush(QColor("#00d4ff"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(vx + 272 + 55 - 5, btn_y + 8, 12, 12)

    # Title in centre
    p.setPen(QColor("#e0f4ff"))
    p.setFont(QFont("Ubuntu", 10))
    p.drawText(QRect(vx + 370, btn_y, vw - 500, 30),
               Qt.AlignmentFlag.AlignCenter, title)

    # CC + Fullscreen buttons
    p.setPen(QPen(QColor("#1a3a4a"), 1))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawRoundedRect(width - 90, btn_y + 4, 28, 22, 4, 4)
    p.setPen(QColor("#2a4a5a"))
    p.setFont(QFont("Ubuntu", 9))
    p.drawText(QRect(width - 90, btn_y + 4, 28, 22), Qt.AlignmentFlag.AlignCenter, "CC")
    p.setPen(QColor("#6a8fa8"))
    p.setFont(QFont("Ubuntu", 14))
    p.drawText(QRect(width - 55, btn_y, 36, 30), Qt.AlignmentFlag.AlignCenter, "⛶")

    p.end()
    return px


def main():
    app = QApplication.instance() or QApplication(sys.argv)
    os.makedirs(OUT_DIR, exist_ok=True)

    shots = [
        ("main.png",       1200, 720,  "movie_trailer.mp4",
         "Open a video file or drag & drop here"),
        ("fullscreen.png", 1920, 1080, "documentary.mkv",
         "Fullscreen mode — move mouse to show controls"),
        ("sidebar.png",    1200, 720,  "short_film.avi",
         "Recent videos sidebar — double-click to play"),
    ]

    for filename, w, h, title, sub in shots:
        path = os.path.join(OUT_DIR, filename)
        px = draw_screenshot(w, h, title, sub)
        px.save(path, "PNG")
        size_kb = os.path.getsize(path) // 1024
        print(f"  ✓  {filename:<20} {w}x{h}  ({size_kb} KB)")

    print(f"\nScreenshots saved to: assets/screenshots/")


if __name__ == "__main__":
    main()
