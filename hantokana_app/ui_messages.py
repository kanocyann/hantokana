from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from .ui_controls import CustomCheckBox
from .ui_utils import center_on_parent, icon_path_exists


class CustomMessageBox(QDialog):
    """自定义消息框"""

    def __init__(self, parent, title, message, style='info', show_dont_show_again=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setModal(True)

        try:
            icon_path, exists = icon_path_exists(parent, "icon.ico")
            if exists:
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass

        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
                border: 0px solid;
                border-radius: 8px;
            }
            QLabel {
                background: transparent;
                border: 0px solid;
                margin: 0px;
                padding: 0px;
            }
            QPushButton {
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
            QCheckBox {
                font-size: 12px;
                color: #666;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        icon_label = QLabel()
        if style == 'info':
            icon_label.setText("ℹ")
            color = "#73BBA3"
        elif style == 'success':
            icon_label.setText("✓")
            color = "#52c41a"
        elif style == 'warning':
            icon_label.setText("⚠")
            color = "#faad14"
        elif style == 'error':
            icon_label.setText("✕")
            color = "#f5222d"
        elif style == 'question':
            icon_label.setText("?")
            color = "#73BBA3"
        else:
            icon_label.setText("ℹ")
            color = "#73BBA3"

        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                color: {color};
                background: transparent;
                border: 0px solid;
                margin: 0px;
                padding: 0px;
                margin-bottom: 2px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        message_label = QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #1f1f1f;
                background: transparent;
                border: 0px solid;
                margin: 0px;
                padding: 0px;
                margin-top: 2px;
            }
        """)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        self.dont_show_again = show_dont_show_again
        self.dont_show_checkbox = None
        if show_dont_show_again:
            self.dont_show_checkbox = CustomCheckBox("不再显示此提示")
            self.dont_show_checkbox.setChecked(False)
            layout.addWidget(self.dont_show_checkbox)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(8)
        self.ok_button = None

        if style == 'question':
            self.ok_button = QPushButton("是")
            self.ok_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 13px;
                    min-width: 60px;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                }}
                QPushButton:pressed {{
                    background-color: {color}bb;
                }}
            """)
            no_button = QPushButton("否")
            no_button.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    color: #666;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 13px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:pressed {
                    background-color: #d9d9d9;
                }
            """)
            self.ok_button.clicked.connect(self.accept)
            no_button.clicked.connect(self.reject)
            self.button_layout.addWidget(self.ok_button)
            self.button_layout.addWidget(no_button)
        else:
            self.ok_button = QPushButton("确定")
            self.ok_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 13px;
                    min-width: 60px;
                }}
                QPushButton:hover {{
                    background-color: {color}dd;
                }}
                QPushButton:pressed {{
                    background-color: {color}bb;
                }}
            """)
            self.ok_button.clicked.connect(self.accept)
            self.button_layout.addWidget(self.ok_button)

        layout.addLayout(self.button_layout)
        self.setFixedWidth(300)
        center_on_parent(self, parent)


class MessageDialog(QDialog):
    """自定义消息对话框"""

    def __init__(self, parent, title, message, style='info'):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setModal(True)

        try:
            icon_path, exists = icon_path_exists(parent, "icon.ico")
            if exists:
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass

        self.setFixedSize(360, 220)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        icon_text = {
            'info': '✓',
            'warning': '⚠',
            'error': '✗',
            'success': '✓',
            'question': '?'
        }.get(style, 'i')

        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"""
            font-size: 36px;
            color: {
                '#52c41a' if style in ['info', 'success'] else
                '#faad14' if style == 'warning' else
                '#f5222d' if style == 'error' else
                '#1890ff' if style == 'question' else
                '#1890ff'
            };
            font-weight: bold;
            padding: 8px;
            background-color: {
                '#f6ffed' if style in ['info', 'success'] else
                '#fffbe6' if style == 'warning' else
                '#fff1f0' if style == 'error' else
                '#e6f7ff' if style == 'question' else
                '#e6f7ff'
            };
            border-radius: 50%;
            min-width: 64px;
            min-height: 64px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        message_label = QLabel(message)
        message_label.setStyleSheet("""
            font-size: 14px;
            color: #1f1f1f;
            font-weight: bold;
            padding: 8px;
            background-color: #fafafa;
            border-radius: 4px;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        ok_button = QPushButton("确定")
        ok_button.setFixedWidth(120)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        center_on_parent(self, parent)
