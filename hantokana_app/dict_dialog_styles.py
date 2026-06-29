PATH_LABEL_STYLE = "color: #666666;"

PANEL_FRAME_STYLE = """
    QFrame {
        background-color: #fafafa;
        border: 1px solid #e8e8e8;
        border-radius: 6px;
        padding: 12px;
    }
"""

FORM_LABEL_STYLE = """
    QLabel {
        border: none;
        font-size: 13px;
        color: #333333;
        font-weight: 500;
        margin-bottom: 2px;
        padding-left: 0px;
    }
"""

FORM_LABEL_SPACED_STYLE = """
    QLabel {
        border: none;
        font-size: 13px;
        color: #333333;
        font-weight: 500;
        margin-top: 8px;
        margin-bottom: 2px;
        padding-left: 0px;
    }
"""

COMPACT_LINE_EDIT_STYLE = """
    QLineEdit {
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        padding: 6px 8px;
        background-color: white;
        font-size: 13px;
        min-height: 24px;
        margin: 0px;
    }
    QLineEdit:focus {
        border-color: #73BBA3;
    }
"""

SEARCH_LINE_EDIT_STYLE = """
    QLineEdit {
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        padding: 8px;
        background-color: white;
        font-size: 13px;
        min-height: 24px;
    }
    QLineEdit:focus {
        border-color: #73BBA3;
    }
"""

DICT_LIST_STYLE = """
    QListWidget {
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        background-color: white;
        font-size: 13px;
        padding: 4px;
        outline: none;
    }
    QListWidget::item {
        padding: 8px;
        border-bottom: 1px solid #f0f0f0;
        background: transparent;
        border-radius: 4px;
        margin: 2px 4px;
    }
    QListWidget::item:selected {
        background-color: #E8F5E9;
        color: #73BBA3;
        border: 1px solid #73BBA3;
        border-radius: 6px;
        margin: 1px 3px;
        outline: none;
        text-decoration: none;
    }
    QListWidget::item:selected:focus {
        outline: none;
        border: 1px solid #73BBA3;
    }
    QListWidget::item:hover {
        background-color: #f5f5f5;
        border-radius: 4px;
    }

    QListWidget QScrollBar:vertical {
        background-color: #f0f0f0;
        width: 12px;
        border-radius: 6px;
        margin: 0px;
        border: none;
        position: absolute;
        right: 0px;
    }

    QListWidget QScrollBar::handle:vertical {
        background-color: #c0c0c0;
        border-radius: 6px;
        min-height: 20px;
        margin: 2px;
    }

    QListWidget QScrollBar::handle:vertical:hover {
        background-color: #a0a0a0;
    }

    QListWidget QScrollBar::handle:vertical:pressed {
        background-color: #808080;
    }

    QListWidget QScrollBar::add-line:vertical {
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QListWidget QScrollBar::sub-line:vertical {
        height: 0px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QListWidget QScrollBar::add-page:vertical,
    QListWidget QScrollBar::sub-page:vertical {
        background-color: transparent;
    }

    QListWidget QScrollBar:horizontal {
        background-color: #f0f0f0;
        height: 12px;
        border-radius: 6px;
        margin: 0px;
        border: none;
        position: absolute;
        bottom: 0px;
    }

    QListWidget QScrollBar::handle:horizontal {
        background-color: #c0c0c0;
        border-radius: 6px;
        min-width: 20px;
        margin: 2px;
    }

    QListWidget QScrollBar::handle:horizontal:hover {
        background-color: #a0a0a0;
    }

    QListWidget QScrollBar::handle:horizontal:pressed {
        background-color: #808080;
    }

    QListWidget QScrollBar::add-line:horizontal {
        width: 0px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }

    QListWidget QScrollBar::sub-line:horizontal {
        width: 0px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QListWidget QScrollBar::add-page:horizontal,
    QListWidget QScrollBar::sub-page:horizontal {
        background-color: transparent;
    }
"""

MATCH_COUNT_LABEL_STYLE = """
    QLabel {
        color: #666666;
        font-size: 13px;
        padding: 0 10px;
        min-width: 120px;
        text-align: center;
    }
"""

FILTER_BUTTON_STYLE = """
    QPushButton {
        background-color: #f5f5f5;
        color: #333333;
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        padding: 4px 12px;
        font-size: 13px;
        font-weight: normal;
    }
    QPushButton:hover {
        background-color: #e6f7ff;
        border-color: #73BBA3;
    }
    QPushButton:pressed {
        background-color: #d6ebd0;
        border-color: #73BBA3;
    }
    QPushButton:checked {
        background-color: #73BBA3;
        color: white;
        border-color: #5A9D8C;
    }
"""

PAGE_INFO_LABEL_STYLE = """
    QLabel {
        color: #73BBA3;
        font-size: 12px;
        padding: 0 10px;
        min-width: 110px;
        text-align: center;
    }
"""

PAGE_SIZE_LABEL_STYLE = """
    QLabel {
        color: #666666;
        font-size: 12px;
        padding-right: 3px;
    }
"""

PAGINATION_BUTTON_STYLE = """
    QPushButton {
        background-color: #f5f5f5;
        color: #333333;
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 12px;
        min-width: 70px;
    }
    QPushButton:hover {
        background-color: #e6f7ff;
        border-color: #73BBA3;
        color: #73BBA3;
    }
    QPushButton:pressed {
        background-color: #d6ebd0;
        border-color: #73BBA3;
    }
    QPushButton:disabled {
        background-color: #f5f5f5;
        color: #d9d9d9;
        border-color: #e8e8e8;
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
        border: 1px solid #d9d9d9;
        border-radius: 4px;
        background-color: white;
        font-size: 13px;
        selection-background-color: #E8F5E9;
        selection-color: #333333;
        outline: 0;
    }
    QTableWidget::item {
        padding: 6px;
        border-bottom: 1px solid #f0f0f0;
        border: none;
        text-align: center;
        min-height: 30px;
        white-space: normal;
    }
    QTableWidget::item:selected {
        background-color: #E8F5E9;
        color: #73BBA3;
        border: none;
        outline: none;
    }
    QTableWidget::item:focus {
        border: none;
        outline: none;
    }
    QTableWidget:focus {
        outline: none;
        border: 1px solid #d9d9d9;
    }
    QHeaderView::section {
        background-color: #f5f5f5;
        padding: 6px;
        border: 1px solid #d9d9d9;
        font-weight: bold;
        text-align: center;
    }
    QTableWidget QScrollBar:vertical {
        background-color: #f0f0f0;
        width: 16px;
        border-radius: 0px;
        margin: 0px;
        border: 1px solid #d9d9d9;
        border-left: none;
    }

    QTableWidget QScrollBar::handle:vertical {
        background-color: #a0a0a0;
        border-radius: 4px;
        min-height: 30px;
        margin: 3px;
    }

    QTableWidget QScrollBar::handle:vertical:hover {
        background-color: #808080;
    }

    QTableWidget QScrollBar::handle:vertical:pressed {
        background-color: #606060;
    }

    QTableWidget QScrollBar::add-line:vertical {
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QTableWidget QScrollBar::sub-line:vertical {
        height: 0px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QTableWidget QScrollBar::add-page:vertical,
    QTableWidget QScrollBar::sub-page:vertical {
        background-color: transparent;
    }

    QTableWidget QScrollBar:horizontal {
        background-color: #f0f0f0;
        height: 12px;
        border-radius: 6px;
        margin: 0px;
        border: none;
        position: absolute;
        bottom: 0px;
    }

    QTableWidget QScrollBar::handle:horizontal {
        background-color: #c0c0c0;
        border-radius: 6px;
        min-width: 20px;
        margin: 2px;
    }

    QTableWidget QScrollBar::handle:horizontal:hover {
        background-color: #a0a0a0;
    }

    QTableWidget QScrollBar::handle:horizontal:pressed {
        background-color: #808080;
    }

    QTableWidget QScrollBar::add-line:horizontal {
        width: 0px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }

    QTableWidget QScrollBar::sub-line:horizontal {
        width: 0px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }

    QTableWidget QScrollBar::add-page:horizontal,
    QTableWidget QScrollBar::sub-page:horizontal {
        background-color: transparent;
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
        background-color: #f5f5f5;
        border: 1px solid #d9d9d9;
        padding: 3px;
        text-align: center;
        font-weight: normal;
    }
    QTableWidget::item:selected {
        background-color: #E8F5E9;
        color: #73BBA3;
    }
    QTableWidget QTableCornerButton::section {
        background-color: #f5f5f5;
        border: 1px solid #d9d9d9;
    }
"""

TABLE_CORNER_STYLE = """
    background-color: #f5f5f5;
    border: 1px solid #d9d9d9;
"""


def action_button_style(background, hover, pressed):
    return f"""
        QPushButton {{
            background-color: {background};
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}
        QPushButton:pressed {{
            background-color: {pressed};
        }}
    """


def page_size_combo_style(arrow_path):
    safe_arrow_path = str(arrow_path).replace("\\", "/")
    return f"""
        QComboBox {{
            border: 1px solid #d9d9d9;
            border-radius: 3px;
            padding: 1px 20px 1px 6px;
            background-color: white;
            font-size: 12px;
            min-width: 60px;
            selection-background-color: #73BBA3;
            selection-color: white;
        }}
        QComboBox:hover {{
            border-color: #73BBA3;
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
            border: 1px solid #d9d9d9;
            border-radius: 3px;
            background-color: white;
            selection-background-color: #73BBA3;
            selection-color: white;
            padding: 2px;
        }}
        QComboBox QAbstractItemView::item {{
            min-height: 20px;
            padding: 2px 6px;
            font-size: 12px;
        }}
        QComboBox QAbstractItemView::item:hover {{
            background-color: #E8F5E9;
            color: #333333;
        }}
    """
