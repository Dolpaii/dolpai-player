"""
Dolpai Player - Splash Screen
Frameless startup screen with logo, animated progress bar, and neon glow border.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPen

from ui.styles import SPLASH_STYLE, COLORS
from assets.logo import get_logo_pixmap


class SplashScreen(QWidget):
    """
    Shown for ~2 seconds on startup.
    Emits `finished` when the main window should appear.
    """

    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._build_ui()
        self._start_animation()

    def _setup_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.SplashScreen
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(420, 320)
        self.setStyleSheet(SPLASH_STYLE)

        # Centre on primary screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width()  - self.width())  // 2,
            (screen.height() - self.height()) // 2,
        )

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo
        logo_label = QLabel()
        logo_label.setPixmap(get_logo_pixmap(90))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title = QLabel("DOLPAI")
        title.setObjectName("splashTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        sub = QLabel("PLAYER")
        sub.setObjectName("splashSub")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub)

        layout.addSpacing(16)

        # Animated progress bar
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(3)
        layout.addWidget(self._progress)

        # Version line
        version = QLabel("v1.0.0  ·  Powered by VLC")
        version.setObjectName("splashVersion")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

    def _start_animation(self):
        """Tick the progress bar from 0 → 100 over ~1.8 s, then emit finished."""
        self._value = 0
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(18)   # ~55 fps
        self._anim_timer.timeout.connect(self._tick)
        self._anim_timer.start()

    def _tick(self):
        self._value += 1
        self._progress.setValue(self._value)
        if self._value >= 100:
            self._anim_timer.stop()
            QTimer.singleShot(150, self._finish)

    def _finish(self):
        self.close()
        self.finished.emit()

    # ------------------------------------------------------------------
    # Custom paint: rounded dark card + top neon glow line
    # ------------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dark rounded background
        painter.setBrush(QColor(COLORS["bg_primary"]))
        painter.setPen(QColor(COLORS["neon_dim"]))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 16, 16)

        # Top neon glow line
        grad = QLinearGradient(0, 0, self.width(), 0)
        grad.setColorAt(0.0, QColor(0, 0, 0, 0))
        grad.setColorAt(0.5, QColor(COLORS["neon_cyan"]))
        grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        pen = QPen(grad, 1.5)
        painter.setPen(pen)
        painter.drawLine(16, 1, self.width() - 16, 1)
