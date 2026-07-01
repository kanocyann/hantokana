APP_BACKGROUND_COLOR = "#f4f6f8"
SURFACE_COLOR = "#ffffff"
SURFACE_ALT_COLOR = "#f9fbfc"
BORDER_COLOR = "#dbe3ea"
BORDER_SOFT_COLOR = "#e6ebf0"
TEXT_COLOR = "#111827"
TEXT_MUTED_COLOR = "#667085"
PRIMARY_COLOR = "#2f7d67"
PRIMARY_HOVER_COLOR = "#3b9378"
PRIMARY_PRESSED_COLOR = "#256352"
SECONDARY_COLOR = "#eef2f6"
SECONDARY_HOVER_COLOR = "#e5edf4"
SECONDARY_PRESSED_COLOR = "#dbe7ef"
ACCENT_COLOR = "#2563eb"
SUCCESS_COLOR = "#16a34a"
WARNING_COLOR = "#d97706"
DANGER_COLOR = "#dc2626"


def _button_style(background, hover, pressed, text_color="white", border_color=None,
                  min_width=100, padding="8px 16px", radius=10, font_size=13, weight=600):
    border_color = border_color or background
    return f"""
QPushButton {{
    background-color: {background};
    color: {text_color};
    border: 1px solid {border_color};
    border-radius: {radius}px;
    padding: {padding};
    min-width: {min_width}px;
    font-size: {font_size}px;
    font-weight: {weight};
}}
QPushButton:hover {{
    background-color: {hover};
    border-color: {hover};
}}
QPushButton:pressed {{
    background-color: {pressed};
    border-color: {pressed};
}}
QPushButton:disabled {{
    background-color: #d8dde3;
    border-color: #d8dde3;
    color: #8c95a0;
}}
QPushButton:focus {{
    outline: none;
}}
"""


APP_STYLE_SHEET = f"""
QWidget {{
    color: {TEXT_COLOR};
    background-color: {APP_BACKGROUND_COLOR};
    font-size: 13px;
}}

QMainWindow, QDialog {{
    background-color: {APP_BACKGROUND_COLOR};
}}

QLabel {{
    background: transparent;
    color: {TEXT_COLOR};
}}

QLabel[muted="true"] {{
    color: {TEXT_MUTED_COLOR};
}}

QLabel[title="true"] {{
    font-size: 18px;
    font-weight: 700;
    color: {TEXT_COLOR};
}}

QLabel[section="true"] {{
    font-size: 14px;
    font-weight: 600;
    color: {TEXT_COLOR};
}}

QLabel[badge="true"] {{
    background-color: {SECONDARY_COLOR};
    color: #344054;
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 12px;
}}

QFrame[card="true"] {{
    background-color: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 14px;
}}

QFrame[softCard="true"] {{
    background-color: {SURFACE_ALT_COLOR};
    border: 1px solid {BORDER_SOFT_COLOR};
    border-radius: 14px;
}}

QFrame[strip="true"] {{
    background-color: {SURFACE_ALT_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 12px;
}}

QLineEdit, QTextEdit, QComboBox {{
    background-color: {SURFACE_COLOR};
    color: {TEXT_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    selection-background-color: #d7efe8;
    selection-color: {TEXT_COLOR};
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border-color: {PRIMARY_COLOR};
}}

QLineEdit {{
    padding: 8px 10px;
}}

QTextEdit {{
    padding: 10px 12px;
}}

QComboBox {{
    padding: 7px 30px 7px 10px;
}}

QComboBox::drop-down {{
    border: none;
    width: 22px;
}}

QComboBox QAbstractItemView {{
    background-color: {SURFACE_COLOR};
    color: {TEXT_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    selection-background-color: #d7efe8;
    selection-color: {TEXT_COLOR};
    outline: none;
}}

QMenuBar {{
    background-color: {APP_BACKGROUND_COLOR};
    border-bottom: 1px solid {BORDER_COLOR};
}}

QMenuBar::item {{
    padding: 6px 10px;
    margin: 2px 2px;
    border-radius: 8px;
    background: transparent;
}}

QMenuBar::item:selected {{
    background-color: #eef7f3;
    color: {PRIMARY_COLOR};
}}

QMenu {{
    background-color: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 14px;
    border-radius: 6px;
}}

QMenu::item:selected {{
    background-color: #eef7f3;
    color: {PRIMARY_COLOR};
}}

QMenu::separator {{
    height: 1px;
    background-color: {BORDER_COLOR};
    margin: 4px 8px;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background-color: #b9c4cf;
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {PRIMARY_COLOR};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background-color: #b9c4cf;
    border-radius: 5px;
    min-width: 20px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {PRIMARY_COLOR};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QToolTip {{
    background-color: {SURFACE_COLOR};
    color: {TEXT_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 6px 8px;
}}

QRadioButton {{
    spacing: 8px;
    color: {TEXT_COLOR};
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 1px solid #b7c0cb;
    background-color: {SURFACE_COLOR};
}}

QRadioButton::indicator:checked {{
    border-color: {PRIMARY_COLOR};
    background: qradialgradient(cx:0.5, cy:0.5, radius:0.42, fx:0.5, fy:0.5,
                                stop:0.0 {PRIMARY_COLOR}, stop:0.65 {PRIMARY_COLOR}, stop:0.7 white);
}}

QRadioButton::indicator:hover {{
    border-color: {PRIMARY_HOVER_COLOR};
}}

QCheckBox {{
    color: {TEXT_COLOR};
    spacing: 8px;
}}

QSplitter::handle {{
    background-color: {BORDER_COLOR};
}}

QSplitter::handle:horizontal {{
    width: 6px;
    margin: 8px 0px;
    border-radius: 3px;
}}

QSplitter::handle:vertical {{
    height: 6px;
    margin: 0px 8px;
    border-radius: 3px;
}}
"""


SECTION_LABEL_STYLE = """
QLabel {
    font-size: 14px;
    font-weight: 600;
    color: #111827;
    background: transparent;
}
"""


SUBTLE_LABEL_STYLE = """
QLabel {
    font-size: 12px;
    color: #667085;
    background: transparent;
}
"""


BADGE_LABEL_STYLE = """
QLabel {
    background-color: #eef2f6;
    color: #344054;
    border: 1px solid #dbe3ea;
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 12px;
}
"""


MAIN_TEXT_EDIT_STYLE = """
QTextEdit {
    border: 1px solid #dbe3ea;
    border-radius: 12px;
    padding: 12px;
    background-color: white;
    font-size: 13px;
    selection-background-color: #d7efe8;
    selection-color: #111827;
}
QTextEdit:focus {
    border-color: #2f7d67;
}

QTextEdit QScrollBar:vertical {
    background: transparent;
    width: 10px;
    border: none;
}

QTextEdit QScrollBar::handle:vertical {
    background-color: #b9c4cf;
    border-radius: 5px;
    min-height: 20px;
    margin: 2px;
}

QTextEdit QScrollBar::handle:vertical:hover {
    background-color: #2f7d67;
}

QTextEdit QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    border: none;
}

QTextEdit QScrollBar::handle:horizontal {
    background-color: #b9c4cf;
    border-radius: 5px;
    min-width: 20px;
    margin: 2px;
}

QTextEdit QScrollBar::handle:horizontal:hover {
    background-color: #2f7d67;
}
"""


PRIMARY_ACTION_BUTTON_STYLE = _button_style(
    PRIMARY_COLOR,
    PRIMARY_HOVER_COLOR,
    PRIMARY_PRESSED_COLOR,
    text_color="white",
    border_color=PRIMARY_COLOR,
    min_width=112,
    padding="8px 16px",
    radius=10,
    font_size=13,
    weight=600,
)


SECONDARY_ACTION_BUTTON_STYLE = _button_style(
    SECONDARY_COLOR,
    SECONDARY_HOVER_COLOR,
    SECONDARY_PRESSED_COLOR,
    text_color="#344054",
    border_color=BORDER_COLOR,
    min_width=92,
    padding="8px 14px",
    radius=10,
    font_size=13,
    weight=500,
)


TERTIARY_ACTION_BUTTON_STYLE = _button_style(
    "transparent",
    "#eef2f6",
    "#e2e8f0",
    text_color="#344054",
    border_color="transparent",
    min_width=84,
    padding="7px 12px",
    radius=10,
    font_size=12,
    weight=500,
)


MAIN_WINDOW_STYLE_SHEET = """
QMainWindow {
    background-color: #f4f6f8;
}
"""
