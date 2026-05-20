# Contributing to Dolpai Player

Thank you for your interest in contributing!

## Getting Started

```bash
git clone https://github.com/Dolpaii/dolpai-player.git
cd dolpai-player
sudo apt install python3-pyqt6 python3-pyqt6.qtsvg python3-vlc vlc ffmpeg
python3 scripts/check_deps.py   # verify your environment
python3 main.py                 # run the app
```

## Project Structure

```
ui/           — All PyQt6 widgets and stylesheets
player/       — VLC backend and data management (no UI imports)
assets/       — Embedded resources (logo, icons)
scripts/      — Developer utilities
packaging/    — Distribution packaging (deb, AppImage, Flatpak, Snap)
```

## Code Style

- Follow the existing pattern: `player/` has zero UI imports, `ui/` has zero VLC imports
- Use Qt signals to communicate between layers
- Keep functions short and focused
- Add a docstring to every class and public method

## Submitting Changes

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test: `python3 main.py`
5. Check deps still work: `python3 scripts/check_deps.py`
6. Open a Pull Request against `main`

## Reporting Bugs

Open an issue at https://github.com/Dolpaii/dolpai-player/issues

Include:
- Ubuntu/Linux version (`lsb_release -a`)
- Python version (`python3 --version`)
- Steps to reproduce
- Error output (run from terminal: `python3 main.py`)
