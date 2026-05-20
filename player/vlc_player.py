"""
Dolpai Player - VLC Backend
Wraps python-vlc and emits Qt signals so the UI stays fully decoupled.
"""

import os
import vlc
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class VLCPlayer(QObject):
    """
    Signals
    -------
    position_changed(float)   0.0 – 1.0
    time_changed(int)         current time in ms
    duration_changed(int)     total duration in ms
    state_changed(str)        'playing' | 'paused' | 'stopped' | 'ended'
    volume_changed(int)       0 – 100
    media_opened(str)         path of the newly opened file
    error_occurred(str)       human-readable error message
    """

    position_changed = pyqtSignal(float)
    time_changed     = pyqtSignal(int)
    duration_changed = pyqtSignal(int)
    state_changed    = pyqtSignal(str)
    volume_changed   = pyqtSignal(int)
    media_opened     = pyqtSignal(str)
    error_occurred   = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # VLC instance — pass args as a list (the correct python-vlc API)
        self._instance = vlc.Instance([
            "--no-xlib",            # avoid X11 threading issues on Linux
            "--quiet",
            "--no-video-title-show",
        ])
        self._player: vlc.MediaPlayer = self._instance.media_player_new()
        self._current_path: str = ""
        self._is_seeking = False
        self._last_state = "stopped"

        # Poll VLC state every 250 ms
        self._timer = QTimer(self)
        self._timer.setInterval(250)
        self._timer.timeout.connect(self._poll)
        self._timer.start()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def open(self, path: str):
        """Open a media file and start playing immediately."""
        if not os.path.isfile(path):
            self.error_occurred.emit(f"File not found: {path}")
            return
        media = self._instance.media_new(path)
        self._player.set_media(media)
        self._current_path = path
        self._player.play()
        self.media_opened.emit(path)

    def set_window(self, win_id: int):
        """Attach VLC video output to a native X11 window handle."""
        if os.name == "posix":
            self._player.set_xwindow(win_id)

    def play(self):
        self._player.play()

    def pause(self):
        self._player.pause()

    def toggle_play_pause(self):
        if self._player.is_playing():
            self._player.pause()
        else:
            self._player.play()

    def stop(self):
        self._player.stop()

    def seek(self, position: float):
        """Seek to a fractional position 0.0 – 1.0."""
        if self._player.get_length() > 0:
            self._player.set_position(max(0.0, min(1.0, position)))

    def seek_ms(self, ms: int):
        """Seek to an absolute time in milliseconds."""
        self._player.set_time(max(0, ms))

    def skip(self, seconds: int):
        """Skip forward (positive) or backward (negative) by N seconds."""
        current = self._player.get_time()
        if current >= 0:
            self._player.set_time(max(0, current + seconds * 1000))

    def set_volume(self, volume: int):
        vol = max(0, min(100, volume))
        self._player.audio_set_volume(vol)
        self.volume_changed.emit(vol)

    def get_volume(self) -> int:
        v = self._player.audio_get_volume()
        return max(0, v)

    def get_duration_ms(self) -> int:
        return max(0, self._player.get_length())

    def get_time_ms(self) -> int:
        return max(0, self._player.get_time())

    def get_position(self) -> float:
        pos = self._player.get_position()
        return max(0.0, float(pos)) if pos is not None else 0.0

    def is_playing(self) -> bool:
        return bool(self._player.is_playing())

    def current_path(self) -> str:
        return self._current_path

    # ------------------------------------------------------------------
    # Subtitle support
    # ------------------------------------------------------------------

    def load_subtitle(self, path: str):
        """Load an external subtitle file (.srt, .ass, .vtt …)."""
        uri = f"file://{os.path.abspath(path)}"
        self._player.add_slave(vlc.MediaSlaveType.subtitle, uri, True)

    def set_subtitle_track(self, track_id: int):
        self._player.video_set_spu(track_id)

    def get_subtitle_tracks(self) -> list:
        """Return list of (id, name) tuples for available subtitle tracks."""
        tracks = self._player.video_get_spu_description()
        if not tracks:
            return []
        result = []
        for t in tracks:
            tid  = t[0]
            name = t[1].decode("utf-8", errors="replace") if isinstance(t[1], bytes) else str(t[1])
            result.append((tid, name))
        return result

    def toggle_subtitles(self):
        """Toggle subtitle display on / off."""
        current = self._player.video_get_spu()
        if current == -1:
            tracks = self.get_subtitle_tracks()
            if len(tracks) > 1:
                self._player.video_set_spu(tracks[1][0])
        else:
            self._player.video_set_spu(-1)

    # ------------------------------------------------------------------
    # Seek state (called by controls bar)
    # ------------------------------------------------------------------

    def begin_seek(self):
        self._is_seeking = True

    def end_seek(self):
        self._is_seeking = False

    # ------------------------------------------------------------------
    # Internal polling
    # ------------------------------------------------------------------

    def _poll(self):
        """Emit position / state signals every 250 ms."""
        if not self._is_seeking:
            self.position_changed.emit(self.get_position())
            self.time_changed.emit(self.get_time_ms())
            dur = self.get_duration_ms()
            if dur > 0:
                self.duration_changed.emit(dur)

        state = self._player.get_state()
        state_map = {
            vlc.State.Playing:        "playing",
            vlc.State.Paused:         "paused",
            vlc.State.Stopped:        "stopped",
            vlc.State.Ended:          "ended",
            vlc.State.Error:          "error",
            vlc.State.NothingSpecial: "stopped",
            vlc.State.Opening:        "opening",
            vlc.State.Buffering:      "buffering",
        }
        new_state = state_map.get(state, "stopped")
        if new_state != self._last_state:
            self._last_state = new_state
            self.state_changed.emit(new_state)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def cleanup(self):
        self._timer.stop()
        self._player.stop()
        self._player.release()
        self._instance.release()
