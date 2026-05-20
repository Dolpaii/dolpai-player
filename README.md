# 🎬 Dolpai Player

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-00d4ff?style=for-the-badge&logo=github"/>
  <img src="https://img.shields.io/badge/python-3.10%2B-00d4ff?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyQt6-6.4%2B-00d4ff?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/VLC-backend-00d4ff?style=for-the-badge&logo=vlcmediaplayer&logoColor=white"/>
  <img src="https://img.shields.io/badge/platform-Ubuntu%20%2F%20Linux-00d4ff?style=for-the-badge&logo=linux&logoColor=white"/>
  <img src="https://img.shields.io/badge/license-MIT-00d4ff?style=for-the-badge"/>
</p>

<p align="center">
  <b>A futuristic, cyberpunk-styled video player for Linux — built with Python, PyQt6 and VLC.</b><br/>
  Premium dark UI · Neon cyan/blue glow · Smooth animations · Drag & drop · Subtitle support
</p>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎥 Video playback | MP4, MKV, AVI, MOV, WMV, WebM, TS, FLV, and more |
| ⏯ Controls | Play/Pause, Stop, Skip ±10s |
| 📊 Progress bar | Click or drag to seek anywhere |
| 🔊 Volume | Slider + mute toggle |
| 🖥 Fullscreen | Auto-hides controls after 3s, shows on mouse move |
| 🖱 Drag & Drop | Drop a video or subtitle file directly onto the window |
| 💬 Subtitles | Load external .srt/.ass/.vtt or toggle embedded tracks |
| 🕐 Recent videos | Sidebar with last 20 files, right-click context menu |
| ⌨️ Keyboard shortcuts | Full keyboard control (see table below) |
| 🚀 CLI open | `python3 main.py /path/to/video.mp4` |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| `Space` | Play / Pause |
| `←` / `→` | Skip ±10 seconds |
| `↑` / `↓` | Volume +5 / −5 |
| `M` | Mute / Unmute |
| `F` | Toggle Fullscreen |
| `Esc` | Exit Fullscreen |
| `S` | Stop |
| `C` | Toggle Subtitles |
| `Ctrl+O` | Open File |
| `Ctrl+R` | Toggle Recent Panel |
| `Ctrl+Shift+S` | Load Subtitle File |
| `Ctrl+Q` | Quit |

---

## 🚀 Installation (Ubuntu / Debian)

### One-command install

```bash
git clone https://github.com/Dolpaii/dolpai-player.git
cd dolpai-player
bash install.sh
```

This will:
- Install system packages (`vlc`, `ffmpeg`, `python3-pyqt6`, `python3-vlc`)
- Verify all Python imports work
- Create a `.desktop` launcher so Dolpai Player appears in your app menu

### Manual install

```bash
sudo apt install python3 python3-pyqt6 python3-pyqt6.qtsvg python3-vlc vlc ffmpeg libxcb-cursor0
git clone https://github.com/Dolpaii/dolpai-player.git
cd dolpai-player
python3 main.py
```

---

## ▶️ Running

```bash
# From the project folder
python3 main.py

# Open a specific file directly
python3 main.py /path/to/video.mp4

# Using the launcher script
bash run.sh
bash run.sh /path/to/video.mp4
```

---

## 🗂 Project Structure

```
dolpai-player/
├── main.py                  # Entry point — splash screen + main window
├── ui/
│   ├── main_window.py       # Main window, layout, drag-drop, keyboard
│   ├── controls.py          # Bottom controls bar widget
│   ├── splash.py            # Startup splash screen with animated bar
│   └── styles.py            # All QSS stylesheets & colour palette
├── player/
│   ├── vlc_player.py        # VLC backend wrapper (Qt signals-based)
│   └── recent_videos.py     # JSON-backed recent files (~/.config/dolpai-player/)
├── assets/
│   └── logo.py              # Embedded SVG logo — no external image files
├── dolpai-player.desktop    # Linux desktop launcher entry
├── install.sh               # One-shot Ubuntu/Debian installer
├── run.sh                   # Quick launch script
├── requirements.txt         # Python package list
└── LICENSE                  # MIT
```

---

## 🔧 Tech Stack

- **Python 3.10+**
- **PyQt6** — UI framework
- **python-vlc** — VLC media engine bindings
- **FFmpeg** — extended codec support via VLC
- **Optimised for Ubuntu / Debian Linux**

---

## 🤖 Extending with AI Features

The clean `player/` ↔ `ui/` separation makes it easy to add AI capabilities:

```
player/ai_subtitles.py    → auto-generate subtitles (Whisper)
player/scene_detect.py    → hook into VLCPlayer.time_changed signal
player/recommender.py     → extend recent_videos.py with smart suggestions
main.py                   → add voice command listener
```

---

## 📄 License

MIT © 2026 [Dolpaii](https://github.com/Dolpaii)
