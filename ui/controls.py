"""
Dolpai Player - Controls Bar
Bottom bar: progress slider, play/pause, skip, volume, time label,
            title, subtitle toggle, fullscreen button.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QSlider, QLabel, QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal

from ui.styles import (
    CONTROL_BUTTON_STYLE, PLAY_BUTTON_STYLE,
    PROGRESS_SLIDER_STYLE, VOLUME_SLIDER_STYLE,
    TIME_LABEL_STYLE, TITLE_LABEL_STYLE,
    SUBTITLE_BUTTON_STYLE, COLORS,
)


def _icon_btn(icon: str, tooltip: str, object_name: str = "") -> QPushButton:
    """Create a small fixed-size icon button."""
    btn = QPushButton(icon)
    btn.setToolTip(tooltip)
    btn.setStyleSheet(CONTROL_BUTTON_STYLE)
    btn.setFixedSize(36, 36)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    if object_name:
        btn.setObjectName(object_name)
    return btn


class ControlsBar(QWidget):
    """
    Emits signals upward so the main window can talk to the player.

    Signals
    -------
    play_pause_clicked
    stop_clicked
    skip_back_clicked(int seconds)
    skip_fwd_clicked(int seconds)
    seek_started
    seek_changed(float 0-1)
    seek_released(float 0-1)
    volume_changed(int 0-100)
    fullscreen_clicked
    subtitle_clicked
    open_file_clicked
    """

    play_pause_clicked = pyqtSignal()
    stop_clicked       = pyqtSignal()
    skip_back_clicked  = pyqtSignal(int)
    skip_fwd_clicked   = pyqtSignal(int)
    seek_started       = pyqtSignal()
    seek_changed       = pyqtSignal(float)
    seek_released      = pyqtSignal(float)
    volume_changed     = pyqtSignal(int)
    fullscreen_clicked = pyqtSignal()
    subtitle_clicked   = pyqtSignal()
    open_file_clicked  = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("controlsBar")
        self._last_volume = 80
        self._build_ui()

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 8, 12, 10)
        root.setSpacing(6)

        # ── Row 1: progress slider + time label ────────────────────────
        progress_row = QHBoxLayout()
        progress_row.setSpacing(8)

        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setObjectName("progressSlider")
        self.progress_slider.setRange(0, 10000)
        self.progress_slider.setValue(0)
        self.progress_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.progress_slider.setStyleSheet(PROGRESS_SLIDER_STYLE)
        self.progress_slider.sliderPressed.connect(self.seek_started)
        self.progress_slider.sliderMoved.connect(
            lambda v: self.seek_changed.emit(v / 10000.0)
        )
        self.progress_slider.sliderReleased.connect(
            lambda: self.seek_released.emit(self.progress_slider.value() / 10000.0)
        )

        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setStyleSheet(TIME_LABEL_STYLE)
        self.time_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        progress_row.addWidget(self.progress_slider)
        progress_row.addWidget(self.time_label)
        root.addLayout(progress_row)

        # ── Row 2: buttons ─────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(4)

        # Open file
        self.open_btn = QPushButton("⊕  OPEN")
        self.open_btn.setObjectName("openButton")
        self.open_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS['bg_control']};
                color: {COLORS['neon_cyan']};
                border: 1px solid {COLORS['neon_dim']};
                border-radius: 7px;
                padding: 5px 12px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['neon_dim']};
                border-color: {COLORS['neon_cyan']};
                color: #ffffff;
            }}
            QPushButton:pressed {{
                background-color: {COLORS['neon_blue']};
            }}
            """
        )
        self.open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_btn.clicked.connect(self.open_file_clicked)
        btn_row.addWidget(self.open_btn)

        btn_row.addSpacing(8)

        # Skip back 10 s
        self.skip_back_btn = _icon_btn("⏮ 10", "Skip back 10s  [←]")
        self.skip_back_btn.clicked.connect(lambda: self.skip_back_clicked.emit(10))
        btn_row.addWidget(self.skip_back_btn)

        # Play / Pause (larger, highlighted)
        self.play_btn = QPushButton("▶")
        self.play_btn.setObjectName("playButton")
        self.play_btn.setStyleSheet(PLAY_BUTTON_STYLE)
        self.play_btn.setToolTip("Play / Pause  [Space]")
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.clicked.connect(self.play_pause_clicked)
        btn_row.addWidget(self.play_btn)

        # Skip forward 10 s
        self.skip_fwd_btn = _icon_btn("10 ⏭", "Skip forward 10s  [→]")
        self.skip_fwd_btn.clicked.connect(lambda: self.skip_fwd_clicked.emit(10))
        btn_row.addWidget(self.skip_fwd_btn)

        # Stop
        self.stop_btn = _icon_btn("⏹", "Stop  [S]")
        self.stop_btn.clicked.connect(self.stop_clicked)
        btn_row.addWidget(self.stop_btn)

        btn_row.addSpacing(8)

        # Volume icon / mute toggle
        self.vol_btn = _icon_btn("🔊", "Mute / Unmute  [M]")
        self.vol_btn.clicked.connect(self._toggle_mute)
        btn_row.addWidget(self.vol_btn)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.volume_slider.setStyleSheet(VOLUME_SLIDER_STYLE)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        btn_row.addWidget(self.volume_slider)

        btn_row.addStretch()

        # Title label (centred, expands)
        self.title_label = QLabel("No media loaded")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setStyleSheet(TITLE_LABEL_STYLE)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        btn_row.addWidget(self.title_label)

        btn_row.addStretch()

        # Subtitle toggle
        self.sub_btn = QPushButton("CC")
        self.sub_btn.setObjectName("subtitleButton")
        self.sub_btn.setStyleSheet(SUBTITLE_BUTTON_STYLE)
        self.sub_btn.setToolTip("Toggle subtitles  [C]")
        self.sub_btn.setCheckable(True)
        self.sub_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sub_btn.clicked.connect(self.subtitle_clicked)
        btn_row.addWidget(self.sub_btn)

        # Fullscreen
        self.fs_btn = _icon_btn("⛶", "Fullscreen  [F]")
        self.fs_btn.clicked.connect(self.fullscreen_clicked)
        btn_row.addWidget(self.fs_btn)

        root.addLayout(btn_row)

    # ------------------------------------------------------------------
    # Public update methods (called by MainWindow)
    # ------------------------------------------------------------------

    def set_playing(self, playing: bool):
        self.play_btn.setText("⏸" if playing else "▶")

    def set_position(self, position: float):
        """Update slider without firing seek signals."""
        if not self.progress_slider.isSliderDown():
            self.progress_slider.blockSignals(True)
            self.progress_slider.setValue(int(position * 10000))
            self.progress_slider.blockSignals(False)

    def set_time_display(self, current_ms: int, total_ms: int):
        self.time_label.setText(
            f"{_fmt_time(current_ms)} / {_fmt_time(total_ms)}"
        )

    def set_title(self, title: str):
        if len(title) > 60:
            title = title[:57] + "…"
        self.title_label.setText(title)

    def set_volume_display(self, volume: int):
        self.volume_slider.blockSignals(True)
        self.volume_slider.setValue(volume)
        self.volume_slider.blockSignals(False)
        self._update_vol_icon(volume)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _on_volume_changed(self, value: int):
        if value > 0:
            self._last_volume = value
        self._update_vol_icon(value)
        self.volume_changed.emit(value)

    def _toggle_mute(self):
        if self.volume_slider.value() > 0:
            self._last_volume = self.volume_slider.value()
            self.volume_slider.setValue(0)
        else:
            self.volume_slider.setValue(self._last_volume)

    def _update_vol_icon(self, volume: int):
        if volume == 0:
            self.vol_btn.setText("🔇")
        elif volume < 40:
            self.vol_btn.setText("🔉")
        else:
            self.vol_btn.setText("🔊")


# ------------------------------------------------------------------
# Utility
# ------------------------------------------------------------------

def _fmt_time(ms: int) -> str:
    """Format milliseconds → MM:SS or HH:MM:SS."""
    s = max(0, ms) // 1000
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{sec:02d}"
    return f"{m:02d}:{sec:02d}"
