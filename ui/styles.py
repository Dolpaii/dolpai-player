"""
Dolpai Player - UI Styles
All QSS stylesheets for the futuristic cyberpunk dark theme.
"""

# Main color palette
COLORS = {
    "bg_primary":    "#0a0a0f",
    "bg_secondary":  "#0f0f1a",
    "bg_panel":      "#12121f",
    "bg_control":    "#1a1a2e",
    "bg_hover":      "#1e1e35",
    "neon_cyan":     "#00d4ff",
    "neon_blue":     "#0080ff",
    "neon_purple":   "#7b2fff",
    "neon_dim":      "#004466",
    "text_primary":  "#e0f4ff",
    "text_secondary":"#6a8fa8",
    "text_dim":      "#2a4a5a",
    "border":        "#1a3a4a",
    "border_glow":   "#00d4ff",
    "slider_groove": "#1a2a3a",
    "slider_handle": "#00d4ff",
}

MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['bg_primary']};
    }}
    QWidget {{
        background-color: {COLORS['bg_primary']};
        color: {COLORS['text_primary']};
        font-family: 'Segoe UI', 'Ubuntu', 'Noto Sans', sans-serif;
        font-size: 13px;
    }}
    QToolTip {{
        background-color: {COLORS['bg_control']};
        color: {COLORS['neon_cyan']};
        border: 1px solid {COLORS['neon_dim']};
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 11px;
    }}
"""

VIDEO_FRAME_STYLE = f"""
    QFrame#videoFrame {{
        background-color: #000000;
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
    }}
"""

CONTROLS_BAR_STYLE = f"""
    QWidget#controlsBar {{
        background-color: {COLORS['bg_panel']};
        border-top: 1px solid {COLORS['border']};
        border-radius: 0px 0px 12px 12px;
    }}
"""

PROGRESS_SLIDER_STYLE = f"""
    QSlider#progressSlider {{
        height: 18px;
    }}
    QSlider#progressSlider::groove:horizontal {{
        height: 4px;
        background: {COLORS['slider_groove']};
        border-radius: 2px;
        margin: 0px;
    }}
    QSlider#progressSlider::sub-page:horizontal {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['neon_blue']},
            stop:1 {COLORS['neon_cyan']}
        );
        border-radius: 2px;
    }}
    QSlider#progressSlider::handle:horizontal {{
        background: {COLORS['neon_cyan']};
        border: 2px solid {COLORS['bg_primary']};
        width: 14px;
        height: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }}
    QSlider#progressSlider::handle:horizontal:hover {{
        background: #ffffff;
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }}
"""

VOLUME_SLIDER_STYLE = f"""
    QSlider#volumeSlider {{
        height: 18px;
        max-width: 90px;
        min-width: 70px;
    }}
    QSlider#volumeSlider::groove:horizontal {{
        height: 3px;
        background: {COLORS['slider_groove']};
        border-radius: 2px;
    }}
    QSlider#volumeSlider::sub-page:horizontal {{
        background: {COLORS['neon_cyan']};
        border-radius: 2px;
    }}
    QSlider#volumeSlider::handle:horizontal {{
        background: {COLORS['neon_cyan']};
        border: 2px solid {COLORS['bg_primary']};
        width: 12px;
        height: 12px;
        margin: -5px 0;
        border-radius: 6px;
    }}
    QSlider#volumeSlider::handle:horizontal:hover {{
        background: #ffffff;
    }}
"""

CONTROL_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {COLORS['text_secondary']};
        border: none;
        border-radius: 6px;
        padding: 6px;
        font-size: 16px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['bg_hover']};
        color: {COLORS['neon_cyan']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['neon_dim']};
        color: #ffffff;
    }}
"""

PLAY_BUTTON_STYLE = f"""
    QPushButton#playButton {{
        background-color: {COLORS['bg_control']};
        color: {COLORS['neon_cyan']};
        border: 1px solid {COLORS['neon_dim']};
        border-radius: 20px;
        padding: 8px;
        font-size: 18px;
        min-width: 40px;
        min-height: 40px;
        max-width: 40px;
        max-height: 40px;
    }}
    QPushButton#playButton:hover {{
        background-color: {COLORS['neon_dim']};
        border-color: {COLORS['neon_cyan']};
        color: #ffffff;
    }}
    QPushButton#playButton:pressed {{
        background-color: {COLORS['neon_blue']};
    }}
"""

TIME_LABEL_STYLE = f"""
    QLabel#timeLabel {{
        color: {COLORS['text_secondary']};
        font-size: 11px;
        font-family: 'Courier New', monospace;
        padding: 0 4px;
        min-width: 95px;
    }}
"""

TITLE_LABEL_STYLE = f"""
    QLabel#titleLabel {{
        color: {COLORS['text_primary']};
        font-size: 12px;
        font-weight: 500;
        padding: 0 8px;
    }}
"""

RECENT_PANEL_STYLE = f"""
    QWidget#recentPanel {{
        background-color: {COLORS['bg_secondary']};
        border-right: 1px solid {COLORS['border']};
    }}
    QLabel#recentTitle {{
        color: {COLORS['neon_cyan']};
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        padding: 12px 16px 8px 16px;
        text-transform: uppercase;
    }}
    QListWidget {{
        background-color: transparent;
        border: none;
        outline: none;
        padding: 4px;
    }}
    QListWidget::item {{
        background-color: transparent;
        color: {COLORS['text_secondary']};
        border-radius: 6px;
        padding: 8px 10px;
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
        width: 6px;
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
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""

OPEN_BUTTON_STYLE = f"""
    QPushButton#openButton {{
        background-color: {COLORS['bg_control']};
        color: {COLORS['neon_cyan']};
        border: 1px solid {COLORS['neon_dim']};
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
    }}
    QPushButton#openButton:hover {{
        background-color: {COLORS['neon_dim']};
        border-color: {COLORS['neon_cyan']};
        color: #ffffff;
    }}
    QPushButton#openButton:pressed {{
        background-color: {COLORS['neon_blue']};
    }}
"""

SUBTITLE_BUTTON_STYLE = f"""
    QPushButton#subtitleButton {{
        background-color: transparent;
        color: {COLORS['text_dim']};
        border: 1px solid {COLORS['border']};
        border-radius: 5px;
        padding: 4px 8px;
        font-size: 11px;
    }}
    QPushButton#subtitleButton:hover {{
        border-color: {COLORS['neon_cyan']};
        color: {COLORS['neon_cyan']};
    }}
    QPushButton#subtitleButton:checked {{
        background-color: {COLORS['neon_dim']};
        border-color: {COLORS['neon_cyan']};
        color: {COLORS['neon_cyan']};
    }}
"""

DROP_OVERLAY_STYLE = f"""
    QLabel#dropOverlay {{
        background-color: rgba(0, 212, 255, 0.08);
        color: {COLORS['neon_cyan']};
        border: 2px dashed {COLORS['neon_cyan']};
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 2px;
    }}
"""

MENU_BAR_STYLE = f"""
    QMenuBar {{
        background-color: {COLORS['bg_secondary']};
        color: {COLORS['text_secondary']};
        border-bottom: 1px solid {COLORS['border']};
        padding: 2px;
        font-size: 12px;
    }}
    QMenuBar::item {{
        padding: 4px 10px;
        border-radius: 4px;
    }}
    QMenuBar::item:selected {{
        background-color: {COLORS['bg_hover']};
        color: {COLORS['neon_cyan']};
    }}
    QMenu {{
        background-color: {COLORS['bg_control']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 4px;
    }}
    QMenu::item {{
        padding: 6px 20px 6px 12px;
        border-radius: 4px;
    }}
    QMenu::item:selected {{
        background-color: {COLORS['neon_dim']};
        color: {COLORS['neon_cyan']};
    }}
    QMenu::separator {{
        height: 1px;
        background: {COLORS['border']};
        margin: 4px 8px;
    }}
"""

SPLASH_STYLE = f"""
    QWidget {{
        background-color: {COLORS['bg_primary']};
    }}
    QLabel#splashTitle {{
        color: {COLORS['neon_cyan']};
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 6px;
    }}
    QLabel#splashSub {{
        color: {COLORS['text_secondary']};
        font-size: 12px;
        letter-spacing: 3px;
    }}
    QLabel#splashVersion {{
        color: {COLORS['text_dim']};
        font-size: 10px;
        letter-spacing: 2px;
    }}
    QProgressBar {{
        background-color: {COLORS['bg_control']};
        border: none;
        border-radius: 2px;
        height: 3px;
        text-align: center;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['neon_blue']},
            stop:1 {COLORS['neon_cyan']}
        );
        border-radius: 2px;
    }}
"""

def get_full_stylesheet():
    """Returns the combined stylesheet for the main window."""
    return (
        MAIN_WINDOW_STYLE
        + VIDEO_FRAME_STYLE
        + CONTROLS_BAR_STYLE
        + PROGRESS_SLIDER_STYLE
        + VOLUME_SLIDER_STYLE
        + CONTROL_BUTTON_STYLE
        + PLAY_BUTTON_STYLE
        + TIME_LABEL_STYLE
        + TITLE_LABEL_STYLE
        + RECENT_PANEL_STYLE
        + OPEN_BUTTON_STYLE
        + SUBTITLE_BUTTON_STYLE
        + DROP_OVERLAY_STYLE
        + MENU_BAR_STYLE
    )
