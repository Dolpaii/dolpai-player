"""
Dolpai Player - Entry Point
Run:  python3 main.py [/optional/path/to/video.mp4]
"""

import sys
import os

# Ensure the project root is always on sys.path regardless of cwd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.splash import SplashScreen
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Dolpai Player")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Dolpai")
    # WM class used by the desktop file StartupWMClass
    app.setDesktopFileName("dolpai-player")

    # ── Splash screen ──────────────────────────────────────────────────
    splash = SplashScreen()
    splash.show()

    main_win = MainWindow()

    def on_splash_done():
        main_win.show()
        # Open a file passed as CLI argument
        if len(sys.argv) > 1:
            path = os.path.abspath(sys.argv[1])
            if os.path.isfile(path):
                main_win._load_video(path)

    splash.finished.connect(on_splash_done)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
