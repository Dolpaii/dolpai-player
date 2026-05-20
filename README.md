# 🎬 Dolpai Player

<p align="center">
  <img src="assets/icons/hicolor/128x128/apps/dolpai-player.png" width="96" alt="Dolpai Player Logo"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-00d4ff?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/python-3.10%2B-00d4ff?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyQt6-6.4%2B-00d4ff?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/VLC-backend-00d4ff?style=for-the-badge&logo=vlcmediaplayer&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ubuntu-26.04%20LTS-00d4ff?style=for-the-badge&logo=ubuntu&logoColor=white"/>
  <img src="https://img.shields.io/badge/license-MIT-00d4ff?style=for-the-badge"/>
</p>

<p align="center">
  <b>A futuristic, cyberpunk-styled video player for Linux.</b><br/>
  Built with Python · PyQt6 · VLC · FFmpeg
</p>

---

## ✨ Features

| | Feature | Details |
|---|---|---|
| 🎥 | Video playback | MP4, MKV, AVI, MOV, WMV, WebM, FLV, TS, and more |
| ⏯ | Controls | Play/Pause, Stop, Skip ±10s |
| 📊 | Progress bar | Click or drag to seek |
| 🔊 | Volume | Slider + mute toggle |
| 🖥 | Fullscreen | Auto-hides controls after 3s |
| 🖱 | Drag & Drop | Drop video or subtitle files onto the window |
| 💬 | Subtitles | External .srt/.ass/.vtt + embedded track toggling |
| 🕐 | Recent videos | Sidebar with last 20 files, right-click menu |
| ⌨️ | Shortcuts | Full keyboard control |
| 🚀 | CLI | `dolpai-player /path/to/video.mp4` |

---

## ⌨️ Keyboard Shortcuts

| Key | Action | Key | Action |
|---|---|---|---|
| `Space` | Play / Pause | `F` | Toggle Fullscreen |
| `←` | Skip back 10s | `Esc` | Exit Fullscreen |
| `→` | Skip forward 10s | `S` | Stop |
| `↑` | Volume +5 | `C` | Toggle Subtitles |
| `↓` | Volume −5 | `Ctrl+O` | Open File |
| `M` | Mute / Unmute | `Ctrl+Q` | Quit |

---

## 🚀 Installation

### Ubuntu / Debian (recommended)

```bash
git clone https://github.com/Dolpaii/dolpai-player.git
cd dolpai-player
bash install.sh
```

### Manual

```bash
sudo apt install python3-pyqt6 python3-pyqt6.qtsvg python3-vlc vlc ffmpeg libxcb-cursor0
git clone https://github.com/Dolpaii/dolpai-player.git
cd dolpai-player
python3 main.py
```

### Verify dependencies

```bash
python3 scripts/check_deps.py
```

---

## ▶️ Running

```bash
python3 main.py                        # launch
python3 main.py /path/to/video.mp4    # open file directly
bash run.sh                            # launcher script
```

---

## 📦 Distribution Packages

| Format | Build command | Install |
|---|---|---|
| `.deb` | `bash packaging/deb/build-deb.sh` | `sudo dpkg -i dolpai-player_1.0.0_all.deb` |
| AppImage | `bash packaging/appimage/build-appimage.sh` | `chmod +x *.AppImage && ./DolpaiPlayer-*.AppImage` |
| Flatpak | `flatpak-builder build packaging/flatpak/io.github.dolpaii.dolpai_player.yml` | `flatpak install` |
| Snap | `snapcraft` (in `packaging/snap/`) | `snap install dolpai-player` |

Build all at once:
```bash
bash scripts/build_release.sh
```

---

## 🗂 Project Structure

```
dolpai-player/
├── main.py                        # Entry point
├── version.py                     # Single source of version info
├── ui/
│   ├── main_window.py             # Main window, layout, drag-drop, keyboard
│   ├── controls.py                # Bottom controls bar
│   ├── splash.py                  # Startup splash screen
│   └── styles.py                  # QSS stylesheets & colour palette
├── player/
│   ├── vlc_player.py              # VLC backend (Qt signals)
│   └── recent_videos.py           # JSON-backed recent files
├── assets/
│   ├── logo.py                    # Embedded SVG logo
│   └── icons/hicolor/             # PNG icons 16px–512px + SVG
├── packaging/
│   ├── appstream/                 # AppStream metadata (Flathub/GNOME Software)
│   ├── flatpak/                   # Flatpak manifest
│   ├── snap/                      # Snapcraft config
│   └── deb/                       # Debian package structure
├── scripts/
│   ├── check_deps.py              # Dependency validator
│   ├── generate_icons.py          # Icon generator
│   └── build_release.sh           # Full release builder
├── dolpai-player.desktop          # Desktop launcher entry
├── install.sh                     # One-command Ubuntu installer
├── run.sh                         # Quick launch script
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE                        # MIT
└── README.md
```

---

## 🔧 Tech Stack

- **Python 3.10+**
- **PyQt6** — UI framework
- **python-vlc** — VLC media engine bindings
- **FFmpeg** — extended codec support
- **Optimised for Ubuntu / Debian Linux**

---

## 🤖 Extending with AI

The clean `player/` ↔ `ui/` separation makes AI features easy to add:

```python
# Auto-subtitles with Whisper
# player/ai_subtitles.py
from player.vlc_player import VLCPlayer
# hook into VLCPlayer.media_opened signal

# Smart recommendations
# player/recommender.py
from player.recent_videos import load_recent
# analyse watch history, suggest next video
```

---

## 📄 License

MIT © 2026 [Dolpaii](https://github.com/Dolpaii) — see [LICENSE](LICENSE)
