# Dolpai Player v1.0.0 — Store Description

## Short description (max 79 chars — Snap Store summary field)
```
Futuristic cyberpunk video player powered by VLC
```

## Long description (Snap Store / Ubuntu App Center)

Dolpai Player is a premium, futuristic video player for Linux with a
cyberpunk-inspired dark UI featuring neon cyan and blue glow accents.
Built with Python, PyQt6, and the VLC media engine for broad format support.

**FEATURES**

🎥 **Video Playback**
Plays MP4, MKV, AVI, MOV, WMV, WebM, FLV, TS, MPG and many more formats
via the battle-tested VLC media engine with FFmpeg codec support.

🖱 **Drag & Drop**
Drop any video or subtitle file directly onto the window to open it instantly.

💬 **Subtitle Support**
Load external subtitle files (.srt, .ass, .ssa, .vtt, .sub) or toggle
embedded subtitle tracks from the menu.

🕐 **Recent Videos**
Sidebar shows your last 20 videos. Right-click for quick actions.

🖥 **Fullscreen Mode**
Clean fullscreen with controls that auto-hide after 3 seconds and
reappear on mouse movement.

⌨️ **Keyboard Shortcuts**
```
Space     Play / Pause        F    Fullscreen
←  →      Skip ±10 seconds    Esc  Exit Fullscreen
↑  ↓      Volume ±5           S    Stop
M         Mute / Unmute       C    Toggle Subtitles
Ctrl+O    Open File           Ctrl+Q  Quit
```

🎨 **Cyberpunk UI**
Premium dark theme with neon cyan/blue glow accents, smooth hover effects,
rounded controls, and an animated splash screen.

---

## Release Notes — v1.0.0 (2026-05-20)

This is the initial public release of Dolpai Player.

### What's new
- Full VLC-powered video playback with FFmpeg codec support
- Futuristic cyberpunk dark UI (PyQt6, neon cyan/blue theme)
- Drag and drop for video and subtitle files
- External subtitle support (.srt, .ass, .vtt) + embedded track toggling
- Recent videos sidebar with right-click context menu
- Fullscreen mode with 3-second auto-hiding controls
- Complete keyboard shortcut set
- Animated splash screen with custom SVG logo
- Volume slider with mute toggle
- Skip forward/backward 10 seconds
- CLI file argument: `dolpai-player /path/to/video.mp4`

### System requirements
- Ubuntu 22.04 LTS or newer (or any modern Debian-based distro)
- Python 3.10+
- 256 MB RAM minimum
- Display resolution 900×580 minimum

### Installation
```bash
# Via snap (recommended)
sudo snap install dolpai-player

# Via .deb
sudo dpkg -i dolpai-player_1.0.0_all.deb

# From source
git clone https://github.com/Dolpaii/dolpai-player.git
cd dolpai-player && bash install.sh
```

---

## Tags / Keywords
video player, vlc, media player, cyberpunk, dark theme, python, pyqt6,
mkv, mp4, avi, subtitles, linux, ubuntu, open source
