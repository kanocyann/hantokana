APP_STYLE_SHEET = """
QMainWindow {
    background-color: white;
}

QLabel {
    font-size: 13px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

QPushButton {
    background-color: #73BBA3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 13px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #88D66C;
}

QPushButton:pressed {
    background-color: #5A9D8C;
}

QPushButton:disabled {
    background-color: #d9d9d9;
    color: #999999;
}

QTextEdit {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    font-size: 13px;
    selection-background-color: #73BBA3;
}

QTextEdit:focus {
    border-color: #88D66C;
}

QLineEdit {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #88D66C;
}

QMenuBar {
    background-color: white;
    border-bottom: 1px solid #d9d9d9;
}

QMenuBar::item {
    padding: 6px 10px;
    border-radius: 2px;
    background: transparent;
    margin: 1px;
    font-size: 12px;
    border: none;
}

QMenuBar::item:selected {
    background-color: #E8F5E9;
    color: #73BBA3;
    border: 1px solid #73BBA3;
    border-radius: 2px;
}

QMenu {
    background-color: white;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 4px;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 2px;
    background: transparent;
    margin: 1px 2px;
    font-size: 12px;
    border: none;
}

QMenu::item:selected {
    background-color: #E8F5E9;
    color: #73BBA3;
    border: 1px solid #73BBA3;
    border-radius: 2px;
}

QMenu::separator {
    height: 1px;
    background-color: #d9d9d9;
    margin: 4px 8px;
}

QScrollBar:vertical {
    border: none;
    background-color: #f5f5f5;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background-color: #73BBA3;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #88D66C;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #f5f5f5;
    height: 8px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background-color: #73BBA3;
    border-radius: 4px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #88D66C;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""


SECTION_LABEL_STYLE = "font-size: 14px; font-weight: bold;"


MAIN_TEXT_EDIT_STYLE = """
QTextEdit {
    border: 2px solid #73BBA3;
    border-radius: 4px;
    padding: 10px;
    padding-right: 6px;
    background-color: white;
    font-size: 14px;
    margin-bottom: 16px;
}
QTextEdit:focus {
    border-color: #88D66C;
}

QTextEdit QScrollBar:vertical {
    background-color: #f0f0f0;
    width: 12px;
    border-radius: 6px;
    margin: 0px;
    border: none;
    position: absolute;
    right: 0px;
}

QTextEdit QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QTextEdit QScrollBar::handle:vertical:hover {
    background-color: #a0a0a0;
}

QTextEdit QScrollBar::handle:vertical:pressed {
    background-color: #808080;
}

QTextEdit QScrollBar::add-line:vertical {
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QTextEdit QScrollBar::sub-line:vertical {
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QTextEdit QScrollBar::add-page:vertical,
QTextEdit QScrollBar::sub-page:vertical {
    background-color: transparent;
}

QTextEdit QScrollBar:horizontal {
    background-color: #f0f0f0;
    height: 12px;
    border-radius: 6px;
    margin: 0px;
    border: none;
    position: absolute;
    bottom: 0px;
}

QTextEdit QScrollBar::handle:horizontal {
    background-color: #c0c0c0;
    border-radius: 6px;
    min-width: 20px;
    margin: 2px;
}

QTextEdit QScrollBar::handle:horizontal:hover {
    background-color: #a0a0a0;
}

QTextEdit QScrollBar::handle:horizontal:pressed {
    background-color: #808080;
}

QTextEdit QScrollBar::add-line:horizontal {
    width: 0px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QTextEdit QScrollBar::sub-line:horizontal {
    width: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QTextEdit QScrollBar::add-page:horizontal,
QTextEdit QScrollBar::sub-page:horizontal {
    background-color: transparent;
}
"""


PRIMARY_ACTION_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #73BBA3, stop:1 #5A9D8C);
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 500;
    padding: 2px 0 2px 0;
    margin: 8px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #88D66C, stop:1 #73BBA3);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5A9D8C, stop:1 #4A8D7C);
}
"""
