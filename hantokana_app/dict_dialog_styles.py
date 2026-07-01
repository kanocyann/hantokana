from .ui_styles import (
    ACCENT_COLOR,
    APP_BACKGROUND_COLOR,
    BORDER_COLOR,
    BORDER_SOFT_COLOR,
    PRIMARY_COLOR,
    PRIMARY_HOVER_COLOR,
    PRIMARY_PRESSED_COLOR,
    SECONDARY_COLOR,
    SECONDARY_HOVER_COLOR,
    SECONDARY_PRESSED_COLOR,
    SURFACE_ALT_COLOR,
    SURFACE_COLOR,
    TEXT_COLOR,
    TEXT_MUTED_COLOR,
)


PATH_LABEL_STYLE = """
QLabel {
    color: #667085;
    font-size: 12px;
}
"""


PANEL_FRAME_STYLE = """
QFrame {
    background-color: #ffffff;
    border: 1px solid #dbe3ea;
    border-radius: 12px;
}
"""


FORM_LABEL_STYLE = """
QLabel {
    border: none;
    font-size: 13px;
    color: #111827;
    font-weight: 600;
    margin-bottom: 2px;
    padding-left: 0px;
}
"""


FORM_LABEL_SPACED_STYLE = """
QLabel {
    border: none;
    font-size: 13px;
    color: #111827;
    font-weight: 600;
    margin-top: 8px;
    margin-bottom: 2px;
    padding-left: 0px;
}
"""


COMPACT_LINE_EDIT_STYLE = """
QLineEdit {
    border: 1px solid #dbe3ea;
    border-radius: 10px;
    padding: 8px 10px;
    background-color: white;
    font-size: 13px;
    min-height: 24px;
}
QLineEdit:focus {
    border-color: #2f7d67;
}
"""


SEARCH_LINE_EDIT_STYLE = """
QLineEdit {
    border: 1px solid #dbe3ea;
    border-radius: 10px;
    padding: 9px 11px;
    background-color: white;
    font-size: 13px;
    min-height: 24px;
}
QLineEdit:focus {
    border-color: #2f7d67;
}
"""


DICT_LIST_STYLE = """
QListWidget {
    border: 1px solid #dbe3ea;
    border-radius: 12px;
    background-color: white;
    font-size: 13px;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid #eef2f6;
    background: transparent;
    border-radius: 8px;
    margin: 2px 4px;
}
QListWidget::item:selected {
    background-color: #e8f5ef;
    color: #1f6f58;
    border: 1px solid #2f7d67;
    border-radius: 8px;
    margin: 1px 3px;
}
QListWidget::item:hover {
    background-color: #f6f8fb;
}
"""


MATCH_COUNT_LABEL_STYLE = """
QLabel {
    color: #667085;
    font-size: 12px;
    padding: 0 10px;
    min-width: 112px;
    text-align: center;
}
"""


FILTER_BUTTON_STYLE = """
QPushButton {
    background-color: #f7f9fb;
    color: #344054;
    border: 1px solid #dbe3ea;
    border-radius: 10px;
    padding: 6px 12px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #eef7f3;
    border-color: #2f7d67;
}
QPushButton:pressed {
    background-color: #e0efe9;
}
QPushButton:checked {
    background-color: #2f7d67;
    color: white;
    border-color: #2f7d67;
}
"""


PAGE_INFO_LABEL_STYLE = """
QLabel {
    color: #2f7d67;
    font-size: 12px;
    padding: 0 10px;
    min-width: 110px;
    text-align: center;
}
"""


PAGE_SIZE_LABEL_STYLE = """
QLabel {
    color: #667085;
    font-size: 12px;
    padding-right: 3px;
}
"""


PAGINATION_BUTTON_STYLE = """
QPushButton {
    background-color: #f7f9fb;
    color: #344054;
    border: 1px solid #dbe3ea;
    border-radius: 10px;
    padding: 4px 8px;
    font-size: 12px;
    min-width: 66px;
}
QPushButton:hover {
    background-color: #eef7f3;
    border-color: #2f7d67;
    color: #2f7d67;
}
QPushButton:pressed {
    background-color: #e0efe9;
}
QPushButton:disabled {
    background-color: #f5f7fa;
    color: #c2c8d0;
    border-color: #e7ebef;
}
"""


TRANSPARENT_WIDGET_STYLE = """
QWidget {
    background-color: transparent;
    border: none;
}
"""


TABLE_WIDGET_STYLE = """
QTableWidget {
    border: 1px solid #dbe3ea;
    border-radius: 12px;
    background-color: white;
    font-size: 13px;
    selection-background-color: #e8f5ef;
    selection-color: #111827;
    outline: 0;
}
QTableWidget::item {
    padding: 6px;
    border-bottom: 1px solid #eef2f6;
    border: none;
    text-align: center;
    min-height: 30px;
    white-space: normal;
}
QTableWidget::item:selected {
    background-color: #e8f5ef;
    color: #1f6f58;
    border: none;
    outline: none;
}
QTableWidget::item:focus {
    border: none;
    outline: none;
}
QTableWidget:focus {
    outline: none;
    border: 1px solid #dbe3ea;
}
QHeaderView::section {
    background-color: #f6f8fb;
    padding: 7px;
    border: 1px solid #dbe3ea;
    font-weight: 600;
    text-align: center;
}
QTableWidget QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0px;
    border: none;
}
QTableWidget QScrollBar::handle:vertical {
    background-color: #b9c4cf;
    border-radius: 5px;
    min-height: 30px;
    margin: 3px;
}
QTableWidget QScrollBar::handle:vertical:hover {
    background-color: #2f7d67;
}
QTableWidget QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 0px;
    border: none;
}
QTableWidget QScrollBar::handle:horizontal {
    background-color: #b9c4cf;
    border-radius: 5px;
    min-width: 20px;
    margin: 2px;
}
QTableWidget QScrollBar::handle:horizontal:hover {
    background-color: #2f7d67;
}
"""


TABLE_FOCUS_STYLE = """
QTableWidget::item:focus {
    border: 0px;
    outline: none;
}
QTableWidget:focus {
    outline: 0px;
}
QTableWidget QHeaderView::section:vertical {
    background-color: #f6f8fb;
    border: 1px solid #dbe3ea;
    padding: 3px;
    text-align: center;
    font-weight: normal;
}
QTableWidget::item:selected {
    background-color: #e8f5ef;
    color: #1f6f58;
}
QTableWidget QTableCornerButton::section {
    background-color: #f6f8fb;
    border: 1px solid #dbe3ea;
}
"""


TABLE_CORNER_STYLE = """
background-color: #f6f8fb;
border: 1px solid #dbe3ea;
"""


def action_button_style(background, hover, pressed):
    return f"""
        QPushButton {{
            background-color: {background};
            color: white;
            border: 1px solid {background};
            padding: 7px 12px;
            border-radius: 10px;
            font-size: 13px;
            min-width: 84px;
        }}
        QPushButton:hover {{
            background-color: {hover};
            border-color: {hover};
        }}
        QPushButton:pressed {{
            background-color: {pressed};
            border-color: {pressed};
        }}
    """


def page_size_combo_style(arrow_path):
    safe_arrow_path = str(arrow_path).replace("\\", "/")
    return f"""
        QComboBox {{
            border: 1px solid #dbe3ea;
            border-radius: 10px;
            padding: 3px 22px 3px 8px;
            background-color: white;
            font-size: 12px;
            min-width: 60px;
            selection-background-color: #e8f5ef;
            selection-color: #111827;
        }}
        QComboBox:hover {{
            border-color: #2f7d67;
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 20px;
            border: none;
        }}
        QComboBox::down-arrow {{
            image: url("{safe_arrow_path}");
            width: 10px;
            height: 10px;
            margin-right: 5px;
            margin-top: 1px;
        }}
        QComboBox QAbstractItemView {{
            border: 1px solid #dbe3ea;
            border-radius: 10px;
            background-color: white;
            selection-background-color: #e8f5ef;
            selection-color: #111827;
            padding: 2px;
        }}
        QComboBox QAbstractItemView::item {{
            min-height: 20px;
            padding: 2px 6px;
            font-size: 12px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: #eef7f3;
            color: #111827;
        }}
    """
