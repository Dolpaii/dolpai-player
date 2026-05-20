# Dolpai Player — Publishing Checklist

## ✅ Pre-publish Validation

### Code & App
- [x] App launches without errors: `python3 main.py`
- [x] Dependency check passes: `python3 scripts/check_deps.py`
- [x] All Python files pass syntax check
- [x] Drag & drop works
- [x] Subtitles load correctly
- [x] Fullscreen auto-hide works
- [x] Recent videos persist across restarts
- [x] Keyboard shortcuts all functional
- [x] Volume/mute works
- [x] CLI file argument works: `python3 main.py video.mp4`

### Metadata
- [x] `version.py` — single source of truth for version
- [x] `packaging/appstream/*.metainfo.xml` — AppStream 1.0 compliant
- [x] `metadata_license` set to `FSFAP` (correct for metadata)
- [x] `project_license` set to `MIT`
- [x] `<content_rating type="oars-1.1">` — fully filled
- [x] `<launchable>` matches `.desktop` filename
- [x] `<releases>` has correct date and version
- [x] `<developer id>` set correctly
- [x] `<update_contact>` set

### Desktop Integration
- [x] `.desktop` file valid (no `TryExec` pointing to missing binary)
- [x] `StartupWMClass=dolpai-player` set
- [x] `MimeType` covers all supported video formats
- [x] `Categories=AudioVideo;Video;Player;`
- [x] Icon exists at all required sizes (16→512 + SVG)

### Icons
- [x] 16x16, 22x22, 24x24, 32x32, 48x48 — toolbar/panel sizes
- [x] 64x64, 96x96, 128x128 — app launcher sizes
- [x] 256x256, 512x512 — store/HiDPI sizes
- [x] scalable SVG — vector source

### Screenshots
- [x] `assets/screenshots/main.png` — 1200×720 (default)
- [x] `assets/screenshots/fullscreen.png` — 1920×1080
- [x] `assets/screenshots/sidebar.png` — 1200×720
- [ ] Upload real screenshots after first run (replace placeholders)

---

## 📦 Snap Store

### Build
```bash
sudo snap install snapcraft --classic
cd dolpai-player
snapcraft
```

### Validate
```bash
review-tools.snap-review dolpai-player_1.0.0_amd64.snap
```

### Checklist
- [x] `snap/snapcraft.yaml` — `base: core24`
- [x] `grade: stable`
- [x] `confinement: strict`
- [x] `license: MIT`
- [x] `contact`, `issues`, `source-code`, `website` URLs set
- [x] `extensions: [gnome]` — handles Qt/Wayland/X11 automatically
- [x] No `hardware-observe` plug (requires manual review)
- [x] `audio-playback` plug for sound
- [x] `home` + `removable-media` for file access
- [x] `VLC_PLUGIN_PATH` set in launcher
- [x] `XDG_CONFIG_HOME` redirected to `$SNAP_USER_COMMON`
- [x] `__pycache__` stripped from snap in `override-build`
- [x] Desktop + icons + metainfo included in snap

### Publish
```bash
# Register name (one time)
snapcraft register dolpai-player

# Upload
snapcraft upload dolpai-player_1.0.0_amd64.snap --release=stable

# Or push to edge first for testing
snapcraft upload dolpai-player_1.0.0_amd64.snap --release=edge
```

---

## 🏪 Ubuntu App Center (AppStream / .deb)

### Build .deb
```bash
sudo apt install dpkg-dev
bash packaging/deb/build-deb.sh
```

### Validate
```bash
sudo apt install appstream
appstreamcli validate packaging/appstream/io.github.dolpaii.dolpai_player.metainfo.xml
lintian release/dolpai-player_1.0.0_all.deb
```

### Checklist
- [x] AppStream metainfo XML valid
- [x] `<launchable>` matches installed `.desktop` filename
- [x] OARS content rating complete
- [x] Screenshots referenced in metainfo
- [x] `.deb` installs to `/usr/lib/dolpai-player/`
- [x] Binary at `/usr/bin/dolpai-player`
- [x] `postinst` updates desktop/icon/MIME databases
- [ ] Submit to Ubuntu App Center: https://snapcraft.io/store (via snap)
  or via Launchpad PPA: https://launchpad.net/

---

## 🐧 Flathub

### Checklist
- [x] `packaging/flatpak/io.github.dolpaii.dolpai_player.yml` manifest
- [x] AppStream metainfo included
- [x] App ID uses reverse-DNS: `io.github.dolpaii.dolpai_player`
- [ ] Replace `sha256: placeholder` with real SHA256 of python-vlc tarball
- [ ] Test build: `flatpak-builder --force-clean build-dir packaging/flatpak/*.yml`
- [ ] Fork https://github.com/flathub/flathub
- [ ] Submit PR with manifest to flathub repo

---

## 🏷️ GitHub Release

```bash
# Tag the release
git tag -a v1.0.0 -m "Dolpai Player v1.0.0 — Initial public release"
git push origin v1.0.0
```

Then on GitHub:
1. Go to https://github.com/Dolpaii/dolpai-player/releases/new
2. Tag: `v1.0.0`
3. Title: `Dolpai Player v1.0.0`
4. Body: paste contents of `STORE_DESCRIPTION.md`
5. Attach: `dolpai-player_1.0.0_all.deb`, `DolpaiPlayer-1.0.0-x86_64.AppImage`

---

## 🔒 Security Review

- [x] No hardcoded credentials or tokens in source
- [x] No network requests at startup
- [x] Config stored in `~/.config/dolpai-player/` (user-owned)
- [x] No `sudo` required to run
- [x] MIT license — open source, no restrictions
- [x] Token removed from git remote URL after push
