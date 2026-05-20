"""
Dolpai Player - Main Window
Assembles video frame, recent panel, controls bar, and menu bar.
Connects UI signals to the VLC backend.
"""

import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QListWidget, QListWidgetItem,
    QFileDialog, QSizePolicy, QApplication, QMessageBox,
    QMenu,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QAction, QKeySequence, QDragEnterEvent, QDropEvent

from ui.styles import get_full_stylesheet, COLORS
from ui.controls import ControlsBar
from assets.logo import get_window_icon
from player.vlc_player import VLCPlayer
from player.recent_videos import add_recent, load_recent, clear_recent, save_recent


# Supported file extensions
VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv",
    ".webm", ".m4v", ".ts", ".mpg", ".mpeg", ".3gp",
    ".ogv", ".rm", ".rmvb", ".divx",
}
SUBTITLE_EXTENSIONS = {".srt", ".ass", ".ssa", ".vtt", ".sub"}


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dolpai Player")
        self.setWindowIcon(get_window_icon())
        self.setMinimumSize(900, 580)
        self.resize(1200, 720)
        self.setStyleSheet(get_full_stylesheet())
        self.setAcceptDrops(True)
        # Required so mouse-move events reach mouseMoveEvent in fullscreen
        self.setMouseTracking(True)

        # Backend
        self._player = VLCPlayer(self)
        self._is_fullscreen = False
        self._recent = load_recent()

        # Auto-hide controls timer (fullscreen only)
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._auto_hide_controls)

        self._build_menu()
        self._build_ui()
        self._connect_signals()
        self._refresh_recent_list()

    # ──────────────────────────────────────────────────────────────────
    # Menu bar
    # ──────────────────────────────────────────────────────────────────

    def _build_menu(self):
        mb = self.menuBar()

        # File
        file_menu = mb.addMenu("File")
        self._add_action(file_menu, "Open File…",        "Ctrl+O",       self._open_file_dialog)
        self._add_action(file_menu, "Load Subtitle…",    "Ctrl+Shift+S", self._open_subtitle_dialog)
        file_menu.addSeparator()
        self._add_action(file_menu, "Clear Recent Videos", None,          self._clear_recent)
        file_menu.addSeparator()
        self._add_action(file_menu, "Quit",              "Ctrl+Q",       self.close)

        # View
        view_menu = mb.addMenu("View")
        self._add_action(view_menu, "Toggle Fullscreen",    "F",       self._toggle_fullscreen)
        self._add_action(view_menu, "Toggle Recent Panel",  "Ctrl+R",  self._toggle_recent_panel)

        # Playback
        pb_menu = mb.addMenu("Playback")
        self._add_action(pb_menu, "Play / Pause",       "Space",  self._player.toggle_play_pause)
        self._add_action(pb_menu, "Stop",               "S",      self._player.stop)
        pb_menu.addSeparator()
        self._add_action(pb_menu, "Skip Forward 10s",   "Right",  lambda: self._player.skip(10))
        self._add_action(pb_menu, "Skip Back 10s",      "Left",   lambda: self._player.skip(-10))
        pb_menu.addSeparator()
        self._add_action(pb_menu, "Volume Up",          "Up",     self._volume_up)
        self._add_action(pb_menu, "Volume Down",        "Down",   self._volume_down)
        self._add_action(pb_menu, "Mute / Unmute",      "M",      self._toggle_mute)

        # Subtitles
        sub_menu = mb.addMenu("Subtitles")
        self._add_action(sub_menu, "Toggle Subtitles",      "C",    self._toggle_subtitles)
        self._add_action(sub_menu, "Load Subtitle File…",   None,   self._open_subtitle_dialog)

    def _add_action(self, menu, label, shortcut, slot):
        act = QAction(label, self)
        if shortcut:
            act.setShortcut(QKeySequence(shortcut))
        act.triggered.connect(slot)
        menu.addAction(act)

    # ──────────────────────────────────────────────────────────────────
    # UI layout
    # ──────────────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left: recent panel
        self._recent_panel = self._make_recent_panel()
        main_layout.addWidget(self._recent_panel)

        # Right: video + controls
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Video frame (VLC renders into this)
        self._video_frame = QFrame()
        self._video_frame.setObjectName("videoFrame")
        self._video_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._video_frame.setStyleSheet(
            "QFrame#videoFrame { background-color: #000000; }"
        )

        # Drag-and-drop overlay (child of video frame)
        self._drop_overlay = QLabel("⊕  DROP VIDEO HERE", self._video_frame)
        self._drop_overlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._drop_overlay.setStyleSheet(
            f"""
            QLabel {{
                background-color: rgba(0, 212, 255, 0.08);
                color: {COLORS['neon_cyan']};
                border: 2px dashed {COLORS['neon_cyan']};
                border-radius: 12px;
                font-size: 20px;
                font-weight: 600;
                letter-spacing: 3px;
            }}
            """
        )
        self._drop_overlay.hide()

        # Placeholder shown when no video is loaded
        self._placeholder = QLabel(self._video_frame)
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet(
            f"color: {COLORS['text_dim']}; font-size: 14px; letter-spacing: 2px;"
        )
        self._placeholder.setText(
            "DOLPAI PLAYER\n\n"
            "Open a video file or drag & drop here\n\n"
            "Ctrl+O  ·  Supported: MP4, MKV, AVI, MOV…"
        )

        right_layout.addWidget(self._video_frame)

        # Controls bar
        self._controls = ControlsBar()
        right_layout.addWidget(self._controls)

        main_layout.addWidget(right)

        # Attach VLC output after the widget has a real window handle
        QTimer.singleShot(200, self._attach_vlc_window)

    def _make_recent_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("recentPanel")
        panel.setFixedWidth(200)
        panel.setStyleSheet(
            f"""
            QWidget#recentPanel {{
                background-color: {COLORS['bg_secondary']};
                border-right: 1px solid {COLORS['border']};
            }}
            """
        )
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("RECENT")
        title.setStyleSheet(
            f"""
            QLabel {{
                color: {COLORS['neon_cyan']};
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 3px;
                padding: 14px 14px 8px 14px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            """
        )
        layout.addWidget(title)

        self._recent_list = QListWidget()
        self._recent_list.setStyleSheet(
            f"""
            QListWidget {{
                background-color: transparent;
                border: none;
                outline: none;
                padding: 4px 2px;
            }}
            QListWidget::item {{
                color: {COLORS['text_secondary']};
                border-radius: 5px;
                padding: 7px 10px;
                margin: 1px 4px;
                font-size: 11px;
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['bg_hover']};
                color: {COLORS['text_primary']};
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['neon_dim']};
                color: {COLORS['neon_cyan']};
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg_primary']};
                width: 5px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['border']};
                border-radius: 3px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {COLORS['neon_dim']};
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{ height: 0px; }}
            """
        )
        self._recent_list.itemDoubleClicked.connect(self._open_recent_item)
        self._recent_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._recent_list.customContextMenuRequested.connect(self._recent_context_menu)
        layout.addWidget(self._recent_list)

        return panel

    # ──────────────────────────────────────────────────────────────────
    # Signal wiring
    # ──────────────────────────────────────────────────────────────────

    def _connect_signals(self):
        c = self._controls
        p = self._player

        # Controls → Player
        c.play_pause_clicked.connect(p.toggle_play_pause)
        c.stop_clicked.connect(p.stop)
        c.skip_back_clicked.connect(lambda s: p.skip(-s))
        c.skip_fwd_clicked.connect(lambda s: p.skip(s))
        c.seek_started.connect(p.begin_seek)
        c.seek_changed.connect(p.seek)
        c.seek_released.connect(self._on_seek_released)
        c.volume_changed.connect(p.set_volume)
        c.fullscreen_clicked.connect(self._toggle_fullscreen)
        c.subtitle_clicked.connect(self._toggle_subtitles)
        c.open_file_clicked.connect(self._open_file_dialog)

        # Player → UI
        p.position_changed.connect(c.set_position)
        p.time_changed.connect(self._on_time_changed)
        p.duration_changed.connect(self._on_duration_changed)
        p.state_changed.connect(self._on_state_changed)
        p.volume_changed.connect(c.set_volume_display)
        p.media_opened.connect(self._on_media_opened)
        p.error_occurred.connect(self._on_error)

        # Initial volume
        p.set_volume(80)

    # ──────────────────────────────────────────────────────────────────
    # VLC window attachment
    # ──────────────────────────────────────────────────────────────────

    def _attach_vlc_window(self):
        win_id = int(self._video_frame.winId())
        self._player.set_window(win_id)

    # ──────────────────────────────────────────────────────────────────
    # File opening
    # ──────────────────────────────────────────────────────────────────

    def _open_file_dialog(self):
        exts = " ".join(f"*{e}" for e in sorted(VIDEO_EXTENSIONS))
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", str(Path.home()),
            f"Video Files ({exts});;All Files (*)",
        )
        if path:
            self._load_video(path)

    def _open_subtitle_dialog(self):
        exts = " ".join(f"*{e}" for e in sorted(SUBTITLE_EXTENSIONS))
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Subtitle File", str(Path.home()),
            f"Subtitle Files ({exts});;All Files (*)",
        )
        if path:
            self._player.load_subtitle(path)
            self._controls.sub_btn.setChecked(True)

    def _load_video(self, path: str):
        """Open a video file and update recent list."""
        self._placeholder.hide()
        self._player.open(path)
        self._recent = add_recent(path)
        self._refresh_recent_list()

    # ──────────────────────────────────────────────────────────────────
    # Player signal handlers
    # ──────────────────────────────────────────────────────────────────

    @pyqtSlot(int)
    def _on_time_changed(self, ms: int):
        self._controls.set_time_display(ms, self._player.get_duration_ms())

    @pyqtSlot(int)
    def _on_duration_changed(self, ms: int):
        self._controls.set_time_display(self._player.get_time_ms(), ms)

    @pyqtSlot(str)
    def _on_state_changed(self, state: str):
        self._controls.set_playing(state == "playing")
        if state == "ended":
            self._controls.set_position(0.0)
            self._controls.set_time_display(0, self._player.get_duration_ms())

    @pyqtSlot(str)
    def _on_media_opened(self, path: str):
        name = os.path.basename(path)
        self.setWindowTitle(f"{name}  —  Dolpai Player")
        self._controls.set_title(name)

    @pyqtSlot(str)
    def _on_error(self, msg: str):
        QMessageBox.warning(self, "Dolpai Player — Error", msg)

    @pyqtSlot(float)
    def _on_seek_released(self, position: float):
        self._player.seek(position)
        self._player.end_seek()

    # ──────────────────────────────────────────────────────────────────
    # Volume helpers
    # ──────────────────────────────────────────────────────────────────

    def _volume_up(self):
        vol = min(100, self._player.get_volume() + 5)
        self._player.set_volume(vol)
        self._controls.set_volume_display(vol)

    def _volume_down(self):
        vol = max(0, self._player.get_volume() - 5)
        self._player.set_volume(vol)
        self._controls.set_volume_display(vol)

    def _toggle_mute(self):
        # Delegate to the controls bar's mute logic
        self._controls.vol_btn.click()

    # ──────────────────────────────────────────────────────────────────
    # Subtitles
    # ──────────────────────────────────────────────────────────────────

    def _toggle_subtitles(self):
        self._player.toggle_subtitles()

    # ──────────────────────────────────────────────────────────────────
    # Fullscreen
    # ──────────────────────────────────────────────────────────────────

    def _toggle_fullscreen(self):
        if self._is_fullscreen:
            self.showNormal()
            self._recent_panel.show()
            self.menuBar().show()
            self._controls.show()
            self._is_fullscreen = False
            self._hide_timer.stop()
        else:
            self.showFullScreen()
            self._recent_panel.hide()
            self.menuBar().hide()
            self._is_fullscreen = True
            self._reset_hide_timer()

    def _reset_hide_timer(self):
        if self._is_fullscreen:
            self._controls.show()
            self._hide_timer.start(3000)

    def _auto_hide_controls(self):
        if self._is_fullscreen and self._player.is_playing():
            self._controls.hide()

    # ──────────────────────────────────────────────────────────────────
    # Recent panel
    # ──────────────────────────────────────────────────────────────────

    def _refresh_recent_list(self):
        self._recent_list.clear()
        for path in self._recent:
            name = os.path.basename(path)
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, path)
            item.setToolTip(path)
            self._recent_list.addItem(item)

    def _open_recent_item(self, item: QListWidgetItem):
        path = item.data(Qt.ItemDataRole.UserRole)
        if os.path.isfile(path):
            self._load_video(path)
        else:
            QMessageBox.warning(
                self, "File Not Found",
                f"The file no longer exists:\n{path}"
            )
            self._recent = [p for p in self._recent if p != path]
            save_recent(self._recent)
            self._refresh_recent_list()

    def _recent_context_menu(self, pos):
        item = self._recent_list.itemAt(pos)
        menu = QMenu(self)
        if item:
            path = item.data(Qt.ItemDataRole.UserRole)
            play_act = menu.addAction("▶  Play")
            play_act.triggered.connect(lambda: self._open_recent_item(item))
            menu.addSeparator()
            remove_act = menu.addAction("✕  Remove from list")
            remove_act.triggered.connect(lambda: self._remove_recent(path))
            menu.addSeparator()
        clear_act = menu.addAction("🗑  Clear all recent")
        clear_act.triggered.connect(self._clear_recent)
        menu.exec(self._recent_list.mapToGlobal(pos))

    def _remove_recent(self, path: str):
        self._recent = [p for p in self._recent if p != path]
        save_recent(self._recent)
        self._refresh_recent_list()

    def _clear_recent(self):
        clear_recent()
        self._recent = []
        self._refresh_recent_list()

    def _toggle_recent_panel(self):
        self._recent_panel.setVisible(not self._recent_panel.isVisible())

    # ──────────────────────────────────────────────────────────────────
    # Drag & Drop
    # ──────────────────────────────────────────────────────────────────

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                ext = Path(url.toLocalFile()).suffix.lower()
                if ext in VIDEO_EXTENSIONS or ext in SUBTITLE_EXTENSIONS:
                    event.acceptProposedAction()
                    # Show overlay sized to the video frame
                    vf = self._video_frame
                    self._drop_overlay.setGeometry(
                        vf.mapTo(self.centralWidget(), vf.rect().topLeft()).x(),
                        vf.mapTo(self.centralWidget(), vf.rect().topLeft()).y(),
                        vf.width(), vf.height(),
                    )
                    self._drop_overlay.show()
                    self._drop_overlay.raise_()
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self._drop_overlay.hide()

    def dropEvent(self, event: QDropEvent):
        self._drop_overlay.hide()
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            ext  = Path(path).suffix.lower()
            if ext in VIDEO_EXTENSIONS:
                self._load_video(path)
                event.acceptProposedAction()
                return
            elif ext in SUBTITLE_EXTENSIONS:
                self._player.load_subtitle(path)
                self._controls.sub_btn.setChecked(True)
                event.acceptProposedAction()
                return
        event.ignore()

    # ──────────────────────────────────────────────────────────────────
    # Keyboard shortcuts
    # ──────────────────────────────────────────────────────────────────

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Space:
            self._player.toggle_play_pause()
        elif key == Qt.Key.Key_Right:
            self._player.skip(10)
        elif key == Qt.Key.Key_Left:
            self._player.skip(-10)
        elif key == Qt.Key.Key_Up:
            self._volume_up()
        elif key == Qt.Key.Key_Down:
            self._volume_down()
        elif key == Qt.Key.Key_M:
            self._toggle_mute()
        elif key == Qt.Key.Key_F:
            self._toggle_fullscreen()
        elif key == Qt.Key.Key_S:
            self._player.stop()
        elif key == Qt.Key.Key_C:
            self._toggle_subtitles()
        elif key == Qt.Key.Key_Escape and self._is_fullscreen:
            self._toggle_fullscreen()
        else:
            super().keyPressEvent(event)

        if self._is_fullscreen:
            self._reset_hide_timer()

    def mouseMoveEvent(self, event):
        if self._is_fullscreen:
            self._reset_hide_timer()
        super().mouseMoveEvent(event)

    # ──────────────────────────────────────────────────────────────────
    # Resize: keep placeholder and overlay filling the video frame
    # ──────────────────────────────────────────────────────────────────

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_placeholder"):
            # placeholder is a child of _video_frame, so use local rect
            self._placeholder.setGeometry(self._video_frame.rect())
        if hasattr(self, "_drop_overlay") and self._drop_overlay.isVisible():
            vf = self._video_frame
            self._drop_overlay.setGeometry(
                vf.mapTo(self.centralWidget(), vf.rect().topLeft()).x(),
                vf.mapTo(self.centralWidget(), vf.rect().topLeft()).y(),
                vf.width(), vf.height(),
            )

    # ──────────────────────────────────────────────────────────────────
    # Cleanup
    # ──────────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self._player.cleanup()
        event.accept()
