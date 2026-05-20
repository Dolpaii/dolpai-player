"""
Dolpai Player — Dependency Validator
Run before launching to give clear error messages instead of cryptic tracebacks.
Usage: python3 scripts/check_deps.py
"""

import sys
import subprocess
import shutil

CYAN  = "\033[0;36m"
GREEN = "\033[0;32m"
RED   = "\033[0;31m"
YELLOW= "\033[1;33m"
NC    = "\033[0m"

REQUIRED_PYTHON = (3, 10)

checks = []   # (name, ok, fix_hint)


def check(name, test_fn, fix):
    try:
        ok = test_fn()
    except Exception:
        ok = False
    checks.append((name, ok, fix))
    return ok


# ── Python version ────────────────────────────────────────────────────────────
check(
    f"Python >= {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}",
    lambda: sys.version_info >= REQUIRED_PYTHON,
    "sudo apt install python3"
)

# ── PyQt6 ─────────────────────────────────────────────────────────────────────
def _check_pyqt6():
    import PyQt6.QtWidgets
    return True

check("PyQt6",
      _check_pyqt6,
      "sudo apt install python3-pyqt6")

# ── PyQt6.QtSvg ───────────────────────────────────────────────────────────────
def _check_qtsvg():
    import PyQt6.QtSvg
    return True

check("PyQt6.QtSvg (logo rendering)",
      _check_qtsvg,
      "sudo apt install python3-pyqt6.qtsvg")

# ── python-vlc ────────────────────────────────────────────────────────────────
def _check_vlc():
    import vlc
    return True

check("python-vlc",
      _check_vlc,
      "sudo apt install python3-vlc")

# ── VLC binary ────────────────────────────────────────────────────────────────
check("vlc (system binary)",
      lambda: shutil.which("vlc") is not None,
      "sudo apt install vlc")

# ── libvlc shared library ─────────────────────────────────────────────────────
def _check_libvlc():
    result = subprocess.run(
        ["ldconfig", "-p"], capture_output=True, text=True
    )
    return "libvlc.so" in result.stdout

check("libvlc.so",
      _check_libvlc,
      "sudo apt install libvlc-dev")

# ── ffmpeg ────────────────────────────────────────────────────────────────────
check("ffmpeg",
      lambda: shutil.which("ffmpeg") is not None,
      "sudo apt install ffmpeg")

# ── libxcb-cursor (needed by Qt on some systems) ──────────────────────────────
def _check_xcb_cursor():
    result = subprocess.run(
        ["ldconfig", "-p"], capture_output=True, text=True
    )
    return "libxcb-cursor" in result.stdout

check("libxcb-cursor0",
      _check_xcb_cursor,
      "sudo apt install libxcb-cursor0")


# ── Report ────────────────────────────────────────────────────────────────────
print()
print(f"  {CYAN}Dolpai Player — Dependency Check{NC}")
print(f"  {'─' * 44}")

all_ok = True
missing_fixes = []

for name, ok, fix in checks:
    status = f"{GREEN}✓{NC}" if ok else f"{RED}✗{NC}"
    print(f"  {status}  {name}")
    if not ok:
        all_ok = False
        missing_fixes.append((name, fix))

print()

if all_ok:
    print(f"  {GREEN}All dependencies satisfied. Ready to launch!{NC}")
    print()
    sys.exit(0)
else:
    print(f"  {RED}Missing dependencies:{NC}")
    print()
    for name, fix in missing_fixes:
        print(f"  {YELLOW}{name}{NC}")
        print(f"    → {fix}")
        print()
    print(f"  Run the installer to fix all at once:")
    print(f"    {CYAN}bash install.sh{NC}")
    print()
    sys.exit(1)
