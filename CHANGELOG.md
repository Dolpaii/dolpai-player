# Changelog

All notable changes to Dolpai Player are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-05-20

### Added
- Full VLC-powered video playback (MP4, MKV, AVI, MOV, WebM, FLV, TS, and more)
- Futuristic cyberpunk dark UI with neon cyan/blue glow accents (PyQt6)
- Animated splash screen with embedded SVG logo
- Play/Pause, Stop, Skip ±10s controls
- Drag-and-drop support for video and subtitle files
- External subtitle support (.srt, .ass, .ssa, .vtt, .sub)
- Embedded subtitle track toggling
- Recent videos sidebar (last 20 files, persisted to `~/.config/dolpai-player/`)
- Right-click context menu on recent videos list
- Fullscreen mode with 3-second auto-hide controls
- Volume slider with mute toggle
- Complete keyboard shortcut set (Space, ←/→, ↑/↓, M, F, S, C, Esc)
- Menu bar (File, View, Playback, Subtitles)
- CLI file argument: `python3 main.py /path/to/video.mp4`
- One-command Ubuntu/Debian installer (`bash install.sh`)
- Desktop launcher (`.desktop` file) for app menu integration
- AppStream metadata for software centre discovery
- Multi-size icon set (16px → 512px + scalable SVG)
- Dependency validator (`python3 scripts/check_deps.py`)
- Packaging support: .deb, AppImage, Flatpak, Snap

---

## Roadmap

### [1.1.0] — Planned
- [ ] AI-powered auto-subtitle generation (Whisper integration)
- [ ] Playlist support
- [ ] Chapter navigation
- [ ] Playback speed control (0.5× – 2×)
- [ ] Audio track selection
- [ ] Screenshot capture

### [1.2.0] — Planned
- [ ] Smart video recommendations based on watch history
- [ ] Voice command support
- [ ] Hardware-accelerated decoding (VAAPI/VDPAU)
- [ ] Picture-in-picture mode
