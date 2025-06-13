import sys
import os
import json
from ctypes import windll
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QCheckBox, QLabel, QDialog,
                              QFileDialog, QMenu, QListWidget, QLineEdit, 
                             QFrame, QStyleFactory)
from PySide6.QtCore import Qt, QUrl, QRect, QSize
from PySide6.QtGui import QIcon, QAction, QFont, QPixmap, QDesktopServices, QPainter, QPen, QColor
import jaconv
import pykakasi
from fugashi import Tagger
from PySide6.QtCore import QMimeData

# 高清支持
windll.shcore.SetProcessDpiAwareness(1)

# 定义样式表
STYLE_SHEET = """
QMainWindow {
    background-color: #f0f2f5;
}

QLabel {
    font-size: 13px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

QLabel[type="success"] {
    color: #52c41a;
    background: transparent;
}

QLabel[type="warning"] {
    color: #faad14;
    background: transparent;
}

QLabel[type="error"] {
    color: #f5222d;
    background: transparent;
}

QLabel[type="info"] {
    color: #73BBA3;
    background: transparent;
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

QPushButton[type="success"] {
    background-color: #52c41a;
}

QPushButton[type="success"]:hover {
    background-color: #73d13d;
}

QPushButton[type="success"]:pressed {
    background-color: #389e0d;
}

QPushButton[type="warning"] {
    background-color: #faad14;
}

QPushButton[type="warning"]:hover {
    background-color: #ffc53d;
}

QPushButton[type="warning"]:pressed {
    background-color: #d48806;
}

QPushButton[type="error"] {
    background-color: #f5222d;
}

QPushButton[type="error"]:hover {
    background-color: #ff4d4f;
}

QPushButton[type="error"]:pressed {
    background-color: #cf1322;
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

QCheckBox {
    font-size: 13px;
    spacing: 8px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #d9d9d9;
    border-radius: 3px;
    background-color: white;
    position: relative;
}

QCheckBox::indicator:checked {
    background-color: #73BBA3;
    border-color: #73BBA3;
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
}

QCheckBox::indicator:unchecked {
    background-color: white;
    border-color: #d9d9d9;
    image: none;
}

QCheckBox::indicator:hover {
    border-color: #73BBA3;
}

QCheckBox::indicator:checked:hover {
    background-color: #88D66C;
    border-color: #88D66C;
}

/* 开关样式复选框 */
QCheckBox[type="switch"] {
    font-size: 13px;
    spacing: 8px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

QCheckBox[type="switch"]::indicator {
    width: 44px;
    height: 24px;
    border: 2px solid #d9d9d9;
    border-radius: 12px;
    background-color: #f5f5f5;
}

QCheckBox[type="switch"]::indicator:checked {
    background-color: #73BBA3;
    border-color: #73BBA3;
}

QCheckBox[type="switch"]::indicator:unchecked {
    background-color: #f5f5f5;
    border-color: #d9d9d9;
}

QCheckBox[type="switch"]::indicator:hover {
    border-color: #73BBA3;
}

QCheckBox[type="switch"]::indicator:checked:hover {
    background-color: #88D66C;
    border-color: #88D66C;
}

/* 开关滑块 */
QCheckBox[type="switch"]::indicator::after {
    content: "";
    position: absolute;
    top: 2px;
    left: 2px;
    width: 16px;
    height: 16px;
    border-radius: 8px;
    background-color: white;
    transition: left 0.2s ease;
}

QCheckBox[type="switch"]::indicator:checked::after {
    left: 22px;
}

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

QFrame {
    background-color: transparent;
    border: none;
}

QFrame[type="border"] {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    background-color: white;
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

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
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

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* 自定义消息对话框样式 */
MessageDialog QLabel {
    font-size: 14px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

MessageDialog QPushButton {
    background-color: #73BBA3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 13px;
    min-width: 100px;
}

MessageDialog QPushButton:hover {
    background-color: #88D66C;
}

MessageDialog QPushButton:pressed {
    background-color: #5A9D8C;
}

/* 设置窗口样式 */
QDialog[windowTitle="设置"] QLabel {
    font-size: 16px;
    font-weight: bold;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

QDialog[windowTitle="设置"] QFrame {
    background-color: #fafafa;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 8px;
}

QDialog[windowTitle="设置"] QLineEdit {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    font-size: 13px;
}

QDialog[windowTitle="设置"] QLineEdit:focus {
    border-color: #40a9ff;
}

/* 关于窗口样式 */
QDialog[windowTitle="关于"] QLabel {
    font-size: 14px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

QDialog[windowTitle="关于"] QLabel[title="true"] {
    font-size: 18px;
    font-weight: bold;
    color: #1890ff;
    background: transparent;
}

QDialog[windowTitle="关于"] QFrame {
    background-color: #fafafa;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 16px;
}

QDialog[windowTitle="关于"] QLabel[link="true"] {
    color: #1890ff;
    background: transparent;
}

QDialog[windowTitle="关于"] QLabel[link="true"]:hover {
    color: #40a9ff;
}

/* 词典编辑对话框样式 */
DictEditDialog QLabel {
    font-size: 14px;
    color: #1f1f1f;
    background: transparent;
    padding: 0px;
    margin: 0px;
    border: none;
}

DictEditDialog QFrame {
    background-color: #fafafa;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    padding: 16px;
}

DictEditDialog QListWidget {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    background-color: white;
    font-size: 13px;
}

DictEditDialog QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #f0f0f0;
    background: transparent;
    border-radius: 4px;
    margin: 2px 4px;
}

DictEditDialog QListWidget::item:selected {
    background-color: #E8F5E9;
    color: #73BBA3;
    border: 1px solid #73BBA3;
    border-radius: 6px;
    margin: 1px 3px;
    outline: none;
    text-decoration: none;
}

DictEditDialog QListWidget::item:selected:focus {
    outline: none;
    border: 1px solid #73BBA3;
}

DictEditDialog QListWidget::item:hover {
    background-color: #f5f5f5;
    border-radius: 4px;
}

DictEditDialog QPushButton {
    background-color: #73BBA3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 13px;
    min-width: 100px;
}

DictEditDialog QPushButton:hover {
    background-color: #88D66C;
}

DictEditDialog QPushButton:pressed {
    background-color: #5A9D8C;
}

DictEditDialog QPushButton[type="secondary"] {
    background-color: #f5f5f5;
    color: #1f1f1f;
    border: 1px solid #d9d9d9;
}

DictEditDialog QPushButton[type="secondary"]:hover {
    background-color: #fafafa;
    border-color: #40a9ff;
    color: #40a9ff;
}

DictEditDialog QPushButton[type="secondary"]:pressed {
    background-color: #f0f0f0;
}
"""

class CustomCheckBox(QCheckBox):
    """自定义复选框，支持绿色背景和勾选图标"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                spacing: 8px;
                color: #1f1f1f;
                background: transparent;
                padding: 0px;
                margin: 0px;
                border: none;
            }
        """)
        # 连接状态变化信号到重绘
        self.toggled.connect(self.update)
    
    def paintEvent(self, event):
        """自定义绘制复选框效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取复选框区域
        rect = self.rect()
        text_rect = rect.adjusted(32, 0, 0, 0)  # 为复选框留出更多空间
        
        # 绘制文本
        painter.setPen(QColor("#1f1f1f"))
        painter.setFont(self.font())
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.text())
        
        # 计算复选框位置
        checkbox_x = 8
        checkbox_y = (rect.height() - 18) // 2
        checkbox_rect = QRect(checkbox_x, checkbox_y, 18, 18)
        
        # 绘制复选框背景
        if self.isChecked():
            painter.setBrush(QColor("#73BBA3"))
            painter.setPen(QColor("#73BBA3"))
        else:
            painter.setBrush(QColor("white"))
            painter.setPen(QColor("#d9d9d9"))
        
        painter.drawRoundedRect(checkbox_rect, 3, 3)
        
        # 绘制勾选图标
        if self.isChecked():
            painter.setPen(QPen(QColor("white"), 2))
            painter.drawLine(checkbox_x + 3, checkbox_y + 9, checkbox_x + 7, checkbox_y + 13)
            painter.drawLine(checkbox_x + 7, checkbox_y + 13, checkbox_x + 15, checkbox_y + 5)
    
    def sizeHint(self):
        """返回建议的大小"""
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(text_width + 40, 30)  # 增加总宽度
    
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.toggle()
            self.update()  # 强制重绘
    
class SwitchCheckBox(QCheckBox):
    """开关样式的复选框，类似v0.2.py中的info-round-toggle"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                spacing: 8px;
                color: #1f1f1f;
                background: transparent;
                padding: 0px;
                margin: 0px;
                border: none;
            }
        """)
        # 连接状态变化信号到重绘
        self.toggled.connect(self.update)
    
    def paintEvent(self, event):
        """自定义绘制开关效果"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取复选框区域
        rect = self.rect()
        text_rect = rect.adjusted(50, 0, 0, 0)
        
        # 绘制文本
        painter.setPen(QColor("#1f1f1f"))
        painter.setFont(self.font())
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.text())
        
        # 计算开关位置
        switch_x = 8
        switch_y = (rect.height() - 20) // 2  # 减小开关高度
        switch_rect = QRect(switch_x, switch_y, 36, 20)  # 减小开关尺寸
        
        # 绘制开关背景
        if self.isChecked():
            painter.setBrush(QColor("#73BBA3"))
            painter.setPen(QColor("#73BBA3"))
        else:
            painter.setBrush(QColor("#f5f5f5"))
            painter.setPen(QColor("#d9d9d9"))
        
        painter.drawRoundedRect(switch_rect, 10, 10)
        
        # 绘制滑块
        if self.isChecked():
            slider_x = switch_x + 18
        else:
            slider_x = switch_x + 2
        
        slider_rect = QRect(slider_x, switch_y + 2, 16, 16)  # 减小滑块尺寸
        painter.setBrush(QColor("white"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(slider_rect)
    
    def sizeHint(self):
        """返回建议的大小"""
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(text_width + 52, 24)  # 减小总宽度和高度
    
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            # 先切换状态
            self.setChecked(not self.isChecked())
            # 然后更新显示
            self.update()
            # 最后触发信号
            self.toggled.emit(self.isChecked())
    
class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        self.insertPlainText(source.text())

class CustomMessageBox(QDialog):
    """自定义消息框"""
    def __init__(self, parent, title, message, style='info', show_dont_show_again=False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        
        # 设置窗口图标 - 添加错误处理
        try:
            if hasattr(parent, 'resource_path'):
                icon_path = parent.resource_path("icon.ico")
                self.setWindowIcon(QIcon(icon_path))
            else:
                # 如果父窗口没有resource_path方法，尝试直接使用相对路径
                icon_path = "icon.ico"
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
        except Exception:
            # 如果设置图标失败，忽略错误继续执行
            pass
        
        # 设置窗口样式
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
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setSpacing(8)  # 减小整体间距
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标
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
        
        # 消息
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
        
        # 不再显示选项
        self.dont_show_again = None
        if show_dont_show_again and style in ['info', 'success']:
            self.dont_show_again = QCheckBox("不再显示此提示")
            self.dont_show_again.setChecked(False)
            layout.addWidget(self.dont_show_again)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        if style == 'question':
            # 是/否按钮
            yes_button = QPushButton("是")
            yes_button.setStyleSheet(f"""
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
            yes_button.clicked.connect(self.accept)
            no_button.clicked.connect(self.reject)
            button_layout.addWidget(yes_button)
            button_layout.addWidget(no_button)
        else:
            # 确定按钮
            ok_button = QPushButton("确定")
            ok_button.setStyleSheet(f"""
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
            ok_button.clicked.connect(self.accept)
            button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
        
        # 设置固定宽度
        self.setFixedWidth(300)
        
        # 居中显示
        self.center_on_parent(parent)
    
    def center_on_parent(self, parent):
        """居中显示"""
        if parent:
            self.move(parent.frameGeometry().center() - self.rect().center())

class MessageDialog(QDialog):
    """自定义消息对话框"""
    def __init__(self, parent, title, message, style='info'):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        
        # 设置窗口图标 - 添加错误处理
        try:
            if hasattr(parent, 'resource_path'):
                icon_path = parent.resource_path("icon.ico")
                self.setWindowIcon(QIcon(icon_path))
            else:
                # 如果父窗口没有resource_path方法，尝试直接使用相对路径
                icon_path = "icon.ico"
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
        except Exception:
            # 如果设置图标失败，忽略错误继续执行
            pass
        
        # 设置窗口大小
        self.setFixedSize(360, 220)
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 设置图标和消息
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
        
        # 确定按钮
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
        
        # 居中显示
        self.center_on_parent(parent)
    
    def center_on_parent(self, parent):
        """在父窗口中心显示"""
        if parent:
            self.move(parent.frameGeometry().center() - self.rect().center())

class DictEditDialog(QDialog):
    """词典编辑对话框"""
    def __init__(self, parent, word_type, custom_dict):
        super().__init__(parent)
        self.word_type = word_type
        self.custom_dict = custom_dict
        self.setWindowTitle(f"编辑{'复合词' if word_type == 'compound_words' else '普通词'}词典")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        # 设置窗口图标 - 添加错误处理
        try:
            if hasattr(parent, 'resource_path'):
                icon_path = parent.resource_path("icon.ico")
                self.setWindowIcon(QIcon(icon_path))
            else:
                # 如果父窗口没有resource_path方法，尝试直接使用相对路径
                icon_path = "icon.ico"
                if os.path.exists(icon_path):
                    self.setWindowIcon(QIcon(icon_path))
        except Exception:
            # 如果设置图标失败，忽略错误继续执行
            pass
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 路径显示
        path_label = QLabel(f"当前词典文件路径: {parent.current_dict_path}")
        path_label.setStyleSheet("color: #666666;")
        layout.addWidget(path_label)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel)
        input_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #e8e8e8;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(8)  # 减小间距
        input_layout.setContentsMargins(12, 12, 12, 12)  # 设置内边距
        
        # 添加标签，去掉底框线
        word_label = QLabel(f"{'复合词' if word_type == 'compound_words' else '汉字'}")
        word_label.setStyleSheet("""
            QLabel {
                border: none;
                font-size: 13px;
                color: #333333;
                font-weight: 500;
                margin-bottom: 2px;
                padding-left: 0px;
            }
        """)
        input_layout.addWidget(word_label)
        
        self.kanji_edit = QLineEdit()
        self.kanji_edit.setPlaceholderText("请输入汉字或复合词")
        self.kanji_edit.setStyleSheet("""
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
        """)
        input_layout.addWidget(self.kanji_edit)
        
        # 添加标签，去掉底框线
        reading_label = QLabel("对应假名 (用逗号间隔)")
        reading_label.setStyleSheet("""
            QLabel {
                border: none;
                font-size: 13px;
                color: #333333;
                font-weight: 500;
                margin-top: 8px;
                margin-bottom: 2px;
                padding-left: 0px;
            }
        """)
        input_layout.addWidget(reading_label)
        
        self.readings_edit = QLineEdit()
        self.readings_edit.setPlaceholderText("请输入假名读音，多个读音用逗号分隔")
        self.readings_edit.setStyleSheet("""
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
        """)
        input_layout.addWidget(self.readings_edit)
        
        layout.addWidget(input_frame)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        add_button = QPushButton("保存词条")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #73BBA3;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #88D66C;
            }
            QPushButton:pressed {
                background-color: #5A9D8C;
            }
        """)
        add_button.clicked.connect(self.add_entry)
        
        edit_button = QPushButton("编辑词条")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #FFB700;
            }
            QPushButton:pressed {
                background-color: #FF8C00;
            }
        """)
        edit_button.clicked.connect(self.edit_entry)
        
        delete_button = QPushButton("删除选中")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #F49BAB;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #FFAAAA;
            }
            QPushButton:pressed {
                background-color: #FF9898;
            }
        """)
        delete_button.clicked.connect(self.delete_selected)
        
        copy_all_button = QPushButton("复制全部")
        copy_all_button.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #096dd9;
            }
        """)
        copy_all_button.clicked.connect(self.copy_all)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(copy_all_button)
        
        layout.addLayout(button_layout)
        
        # 词典列表
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.list_widget.setStyleSheet("""
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
            QListWidget::item:hover {
                background-color: #f5f5f5;
                border-radius: 4px;
            }
            
            /* 垂直滚动条样式 */
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
            
            /* 水平滚动条样式 */
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
        """)
        layout.addWidget(self.list_widget)
        
        # 选中即复制选项
        copy_layout = QHBoxLayout()
        copy_layout.addStretch()
        self.copy_on_select = SwitchCheckBox("选中即复制")
        self.copy_on_select.setChecked(False)
        copy_layout.addWidget(self.copy_on_select)
        copy_layout.addStretch()
        layout.addLayout(copy_layout)
        
        # 更新列表
        self.update_dict_view()
        
        # 居中显示
        self.center_on_parent(parent)
        
        # 连接信号
        self.copy_on_select.toggled.connect(self.on_selection_changed)
        self.last_selected_item = None  # 添加标志位
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu()
        copy_action = menu.addAction("复制")
        edit_action = menu.addAction("编辑")
        delete_action = menu.addAction("删除")
        
        action = menu.exec_(self.list_widget.mapToGlobal(position))
        if action == copy_action:
            self.copy_selected()
        elif action == edit_action:
            self.edit_entry()
        elif action == delete_action:
            self.delete_selected()
    
    def copy_selected(self):
        """复制选中的词条"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            CustomMessageBox(self, "提示", "请先选择要复制的词条", style='info').exec()
            return
        
        text = "\n".join(item.text() for item in selected_items)
        QApplication.clipboard().setText(text)
        CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
    
    def center_on_parent(self, parent):
        """在父窗口中心显示"""
        if parent:
            self.move(parent.frameGeometry().center() - self.rect().center())
    
    def update_dict_view(self):
        """更新词典列表显示"""
        self.list_widget.clear()
        word_dict = self.custom_dict[self.word_type]
        for kanji, readings in sorted(word_dict.items()):
            self.list_widget.addItem(f"{kanji} → {', '.join(readings)}")
    
    def split_readings(self, raw):
        """分割假名字符串为列表"""
        for sep in [",", "，", "、"]:
            raw = raw.replace(sep, ",")
        return [r.strip() for r in raw.split(",") if r.strip()]
    
    def add_entry(self):
        """添加词条"""
        # 使用主界面上的输入框
        word = self.kanji_edit.text().strip()
        reading = self.readings_edit.text().strip()
        
        if not word or not reading:
            CustomMessageBox(self, "警告", "词条和读音不能为空", style='warning').exec()
            return
        
        # 检查是否已存在该词条
        is_edit = word in self.custom_dict[self.word_type]
        
        self.custom_dict[self.word_type][word] = self.split_readings(reading)
        self.update_dict_view()
        
        # 清空输入框
        self.kanji_edit.clear()
        self.readings_edit.clear()
        
        if is_edit:
            CustomMessageBox(self, "成功", "词条更新成功", style='success').exec()
        else:
            CustomMessageBox(self, "成功", "词条添加成功", style='success').exec()
    
    def edit_entry(self):
        """编辑词条"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            CustomMessageBox(self, "提示", "请先选择要编辑的词条", style='info').exec()
            return
        
        item = selected_items[0]
        word = item.text().split(" → ")[0]
        
        # 添加错误处理
        if word not in self.custom_dict[self.word_type]:
            CustomMessageBox(self, "错误", f"词条 '{word}' 不存在于词典中", style='error').exec()
            return
            
        # 获取所有读音并用逗号连接
        readings = self.custom_dict[self.word_type][word]
        reading = ", ".join(readings)
        
        # 填充到主界面的输入框中
        self.kanji_edit.setText(word)
        self.readings_edit.setText(reading)
        
        # 将焦点设置到读音输入框，方便用户修改
        self.readings_edit.setFocus()
        self.readings_edit.selectAll()
    
    def delete_selected(self):
        """删除选中的词条"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            CustomMessageBox(self, "提示", "请先选择要删除的词条", style='info').exec()
            return
        
        dialog = CustomMessageBox(self, "确认删除", "确定要删除选中的词条吗？", style='question')
        if dialog.exec() == QDialog.Accepted:
            for item in selected_items:
                word = item.text().split(" → ")[0]
                del self.custom_dict[self.word_type][word]
            self.update_dict_view()
            CustomMessageBox(self, "成功", "词条删除成功", style='success').exec()
    
    def copy_all(self):
        """复制所有词条"""
        if not self.custom_dict:
            CustomMessageBox(self, "提示", "词典为空", style='info').exec()
            return
        
        text = "\n".join(f"{word} → {reading}" for word, reading in self.custom_dict[self.word_type].items())
        QApplication.clipboard().setText(text)
        CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
    
    def on_selection_changed(self):
        """当选中列表项时，如果启用了'选中即复制'，则复制选中项"""
        if self.copy_on_select.isChecked():
            selected_items = self.list_widget.selectedItems()
            if selected_items:
                current_item = selected_items[0].text()
                if current_item != self.last_selected_item:  # 检查是否与上次选中项相同
                    QApplication.clipboard().setText(current_item)
                    CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
                    self.last_selected_item = current_item  # 更新标志位
            else:
                QApplication.clipboard().clear()
                self.last_selected_item = None  # 清空标志位

class MainWindow(QMainWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日文汉字-假名/罗马音 转换工具")
        self.setMinimumSize(850, 700)
        
        # 设置窗口图标
        icon_path = self.resource_path("icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        
        # 设置样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            
            /* 菜单栏样式 */
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
            
            /* 下拉菜单样式 */
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
        """)
        
        # 初始化变量
        self.custom_dict = {
            "normal_words": {},
            "compound_words": {}
        }
        self.current_dict_path = None
        self.tagger = None
        self.conv = None
        
        # 加载配置和字典
        self.load_config()
        self.load_custom_dict()
        
        # 创建主窗口部件
        self.setup_ui()
        
        # 居中显示
        self.center_on_screen()
    
    def center_on_screen(self):
        """在屏幕中心显示"""
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.center() - self.rect().center())
    
    def setup_ui(self):
        """设置UI"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 创建菜单
        self.create_menu()
        
        # 输入区域
        input_label = QLabel("输入日文文本")
        input_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(input_label)
        
        self.text_input = PlainTextEdit()
        self.text_input.setMinimumHeight(200)
        self.text_input.setPlaceholderText("请输入要转换的日文文本")
        self.text_input.setStyleSheet("""
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
            
            /* 垂直滚动条样式 */
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
            
            /* 水平滚动条样式 */
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
        """)
        layout.addWidget(self.text_input)
        
        # 转换选项
        options_label = QLabel("转换方式")
        options_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(options_label)
        
        options_layout = QHBoxLayout()
        options_layout.setSpacing(24)
        
        self.use_hira = CustomCheckBox("平假名")
        self.use_hira.setChecked(True)
        self.use_kata = CustomCheckBox("片假名")
        self.use_kata.setChecked(True)
        self.use_roma = CustomCheckBox("罗马音")
        self.use_roma.setChecked(True)
        
        options_layout.addWidget(self.use_hira)
        options_layout.addWidget(self.use_kata)
        options_layout.addWidget(self.use_roma)
        options_layout.addStretch()
        
        layout.addLayout(options_layout)
        
        # 转换按钮
        convert_button = QPushButton("开始转换")
        convert_button.setFixedWidth(140)
        convert_button.setFixedHeight(44)
        convert_button.clicked.connect(self.convert_text)
        convert_button.setStyleSheet("""
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
        """)
        layout.addWidget(convert_button, alignment=Qt.AlignCenter)
        
        # 输出区域
        output_label = QLabel("转换结果")
        output_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(output_label)
        
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setPlaceholderText("转换结果将显示在这里")
        self.text_output.setMinimumHeight(200)
        self.text_output.setStyleSheet("""
            QTextEdit {
                border: 2px solid #73BBA3;
                border-radius: 4px;
                padding: 10px;
                padding-right: 6px;
                background-color: white;
                margin-bottom: 16px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border-color: #88D66C;
            }
            
            /* 垂直滚动条样式 */
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
            
            /* 水平滚动条样式 */
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
        """)
        layout.addWidget(self.text_output)
        
        # 复制按钮
        copy_button = QPushButton("复制结果")
        copy_button.setFixedWidth(140)
        copy_button.setFixedHeight(44)
        copy_button.clicked.connect(self.copy_result)
        copy_button.setStyleSheet("""
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
        """)
        layout.addWidget(copy_button, alignment=Qt.AlignCenter)
    
    def create_menu(self):
        """创建菜单"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        import_action = QAction("导入词典", self)
        import_action.triggered.connect(self.load_dict)
        file_menu.addAction(import_action)
        
        edit_normal_action = QAction("编辑普通词词典", self)
        edit_normal_action.triggered.connect(lambda: self.open_edit_dict_window("normal_words"))
        file_menu.addAction(edit_normal_action)
        
        edit_compound_action = QAction("编辑复合词词典", self)
        edit_compound_action.triggered.connect(lambda: self.open_edit_dict_window("compound_words"))
        file_menu.addAction(edit_compound_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 设置菜单
        settings_menu = menubar.addMenu("设置")
        dict_path_action = QAction("设置默认词库路径", self)
        dict_path_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(dict_path_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.open_about_window)
        help_menu.addAction(about_action)
    
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.get_config_path()):
                with open(self.get_config_path(), 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_dict_path = config.get('current_dict_path', self.current_dict_path)
        except Exception as e:
            print(f"加载配置时出错: {e}")
            # 如果加载失败，使用默认配置
            self.current_dict_path = self.resource_path("dictionary.txt")
    
    def load_custom_dict(self):
        """加载自定义词典"""
        if self.current_dict_path and os.path.exists(self.current_dict_path):
            custom_dict_path = self.current_dict_path
        else:
            custom_dict_path = self.get_dict_path()

        if not os.path.exists(custom_dict_path):
            try:
                initial_dict_path = self.resource_path("custom_dict.json")
                if os.path.exists(initial_dict_path):
                    with open(initial_dict_path, "r", encoding="utf-8") as src:
                        data = src.read()
                    with open(custom_dict_path, "w", encoding="utf-8") as dst:
                        dst.write(data)
                else:
                    with open(custom_dict_path, "w", encoding="utf-8") as f:
                        json.dump({
                            "normal_words": {},
                            "compound_words": {}
                        }, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"初始化字典文件失败: {str(e)}")

        try:
            with open(custom_dict_path, "r", encoding="utf-8") as f:
                self.custom_dict = json.load(f)
            self.current_dict_path = custom_dict_path
        except Exception as e:
            print(f"加载字典文件失败: {str(e)}")
            self.custom_dict = {
                "normal_words": {},
                "compound_words": {}
            }
    
    def save_custom_dict(self):
        """保存自定义词典"""
        dict_path = self.current_dict_path or self.get_dict_path()
        os.makedirs(os.path.dirname(dict_path), exist_ok=True)
        try:
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump(self.custom_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存字典文件失败: {str(e)}")
    
    def get_appdata_path(self):
        """获取应用程序数据目录路径"""
        appdata = os.getenv('APPDATA')
        app_dir = os.path.join(appdata, 'Hantokana')
        os.makedirs(app_dir, exist_ok=True)
        return app_dir
    
    def get_dict_path(self):
        """获取字典文件永久存储路径"""
        return os.path.join(self.get_appdata_path(), 'custom_dict.json')
    
    def get_config_path(self):
        """获取配置文件路径"""
        config_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "HanToKana")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")
    
    def resource_path(self, relative_path):
        """获取资源的绝对路径"""
        try:
            # PyInstaller创建临时文件夹,将路径存储在_MEIPASS中
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def init_tagger(self):
        """初始化分词器"""
        try:
            return Tagger('-r "' + self.resource_path('dicdir/mecabrc') + '" -d "' + self.resource_path('dicdir') + '"')
        except Exception:
            return Tagger()
    
    def init_kks(self):
        """初始化假名转换器"""
        kks = pykakasi.kakasi()
        kks.setMode("J", "a")
        kks.setMode("K", "a")
        kks.setMode("H", "a")
        kks.setMode("r", "Hepburn")
        return kks.getConverter()
    
    def convert_text(self):
        """执行日语文本转换"""
        if self.conv is None:
            self.conv = self.init_kks()
        if self.tagger is None:
            self.tagger = self.init_tagger()

        raw = self.text_input.toPlainText().strip()
        if not raw:
            self.text_output.setPlainText("请输入日文文本。")
            return
        if not (self.use_hira.isChecked() or self.use_kata.isChecked() or self.use_roma.isChecked()):
            CustomMessageBox(self, "警告", "请选择至少一个转换方式", style='warning').exec()
            return

        result = ""
        try:
            # 先进行正常分词
            words = self.tagger(raw)
            
            # 使用集合来跟踪已处理的词，避免重复
            processed_words = set()
            
            i = 0
            while i < len(words):
                # 尝试合并复合词
                for j in range(len(words), i, -1):
                    combined = ''.join([w.surface for w in words[i:j]])
                    if combined in self.custom_dict["compound_words"]:
                        word = combined
                        i = j
                        break
                else:
                    word = words[i].surface
                    i += 1

                # 如果这个词已经处理过，跳过
                if word in processed_words:
                    continue
                
                processed_words.add(word)

                # 对于纯中文文本或标点符号，直接跳过转换
                if (all(ord(char) > 127 for char in word) and 
                    not any(ord(char) in range(0x3040, 0x30FF) for char in word) and
                    not any(ord(char) in range(0x4E00, 0x9FFF) for char in word)):
                    # 这是纯中文文本或标点符号，不进行转换
                    continue

                # 检查是否包含日文字符（平假名、片假名、汉字）
                has_japanese = any(
                    ord(char) in range(0x3040, 0x309F) or  # 平假名
                    ord(char) in range(0x30A0, 0x30FF) or  # 片假名
                    ord(char) in range(0x4E00, 0x9FFF)     # 汉字
                    for char in word
                )
                
                # 如果不包含日文字符，跳过转换
                if not has_japanese:
                    continue

                # 优先使用自定义词典
                readings = self.custom_dict["normal_words"].get(word) or self.custom_dict["compound_words"].get(word)
                if not readings:
                    # 使用pykakasi转换
                    converted = self.conv.convert(word)
                    readings = [item['hira'] for item in converted]

                # 处理所有读音
                if readings:
                    line = f"[{word}]"
                    if self.use_hira.isChecked():
                        # 如果有多个读音，用逗号分隔
                        hira_readings = [jaconv.kata2hira(reading) for reading in readings]
                        line += f" → [{', '.join(hira_readings)}]"
                    if self.use_kata.isChecked():
                        kata_readings = [jaconv.hira2kata(jaconv.kata2hira(reading)) for reading in readings]
                        line += f" → [{', '.join(kata_readings)}]"
                    if self.use_roma.isChecked():
                        roma_readings = []
                        for reading in readings:
                            roma_item = self.conv.convert(reading)[0]
                            roma_readings.append(roma_item['hepburn'])
                        line += f" → [{', '.join(roma_readings)}]"
                    result += line + "\n"
            
            self.text_output.setPlainText(result.strip())
        except Exception as e:
            CustomMessageBox(self, "错误", str(e), style='error').exec()
    
    def copy_result(self):
        """复制转换结果"""
        QApplication.clipboard().setText(self.text_output.toPlainText())
        CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
    
    def load_dict(self):
        """加载自定义词典文件"""
        # 创建文件对话框并设置图标
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("选择自定义词典文件")
        file_dialog.setNameFilter("JSON 文件 (*.json)")
        
        # 设置窗口图标
        try:
            icon_path = self.resource_path("icon.ico")
            file_dialog.setWindowIcon(QIcon(icon_path))
        except Exception:
            # 如果设置图标失败，忽略错误继续执行
            pass
        
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if not file_path:
                return
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    new_dict = json.load(f)
                if isinstance(new_dict, dict):
                    # 合并字典
                    self.custom_dict["normal_words"] = {**self.custom_dict["normal_words"], **new_dict.get("normal_words", {})}
                    self.custom_dict["compound_words"] = {**self.custom_dict["compound_words"], **new_dict.get("compound_words", {})}
                    # 确保目标目录存在
                    os.makedirs(os.path.dirname(self.get_dict_path()), exist_ok=True)
                    with open(self.get_dict_path(), "w", encoding="utf-8") as f:
                        json.dump(self.custom_dict, f, ensure_ascii=False, indent=2)
                    CustomMessageBox(self, "成功", "词典导入并合并成功", style='success').exec()
                else:
                    CustomMessageBox(self, "警告", "所选文件格式无效，请选择一个有效的 JSON 文件", style='warning').exec()
            except Exception as e:
                CustomMessageBox(self, "错误", f"导入词典时发生错误: {e}", style='error').exec()
    
    def open_edit_dict_window(self, word_type):
        """打开词典编辑窗口"""
        dialog = DictEditDialog(self, word_type, self.custom_dict)
        # 设置窗口图标
        icon_path = self.resource_path("icon.ico")
        dialog.setWindowIcon(QIcon(icon_path))
        if dialog.exec() == QDialog.Accepted:
            # 更新主窗口的词典数据
            self.custom_dict = dialog.custom_dict
            # 保存到文件
            self.save_custom_dict()
    
    def open_settings_window(self):
        """打开设置窗口"""
        dialog = QDialog(self)
        dialog.setWindowTitle("设置")
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        dialog.setModal(True)
        
        # 设置窗口图标
        try:
            icon_path = self.resource_path("icon.ico")
            dialog.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass

        layout = QVBoxLayout(dialog)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 路径输入框
        path_frame = QFrame()
        path_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                background: transparent;
            }
        """)
        path_layout = QHBoxLayout(path_frame)
        path_layout.setContentsMargins(8, 8, 8, 8)
        path_layout.setSpacing(8)
        
        path_edit = QLineEdit()
        path_edit.setText(self.current_dict_path or "")
        path_edit.setPlaceholderText("请选择或输入词典文件路径")
        path_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #40a9ff;
            }
        """)
        path_layout.addWidget(path_edit)
        
        select_button = QPushButton("选择文件")
        select_button.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                color: #1f1f1f;
                border: 1px solid #d9d9d9;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #fafafa;
                border-color: #40a9ff;
                color: #40a9ff;
            }
            QPushButton:pressed {
                background-color: #f0f0f0;
            }
        """)
        select_button.clicked.connect(lambda: self.select_path(path_edit))
        path_layout.addWidget(select_button)
        
        layout.addWidget(path_frame)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        save_button = QPushButton("保存设置")
        save_button.setStyleSheet("""
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
                background-color: #88D66C;
            }
        """)
        save_button.clicked.connect(lambda: self.save_settings(path_edit, dialog))
        
        cancel_button = QPushButton("取消")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F49BAB;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #FFAAAA;
            }
            QPushButton:pressed {
                background-color: #FF9898;
            }
        """)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # 设置最小大小
        dialog.setMinimumSize(500, 150)
        
        # 居中显示
        dialog.move(self.frameGeometry().center() - dialog.rect().center())
        dialog.exec()
    
    def select_path(self, path_edit):
        """选择词库路径"""
        parent_dialog = path_edit.window()  # 获取设置窗口作为父窗口
        
        # 创建文件对话框并设置图标
        file_dialog = QFileDialog(parent_dialog)
        file_dialog.setWindowTitle("选择默认词典文件")
        file_dialog.setNameFilter("JSON 文件 (*.json)")
        
        # 设置窗口图标
        try:
            icon_path = self.resource_path("icon.ico")
            file_dialog.setWindowIcon(QIcon(icon_path))
        except Exception:
            # 如果设置图标失败，忽略错误继续执行
            pass
        
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                path_edit.setText(file_path)
    
    def save_settings(self, path_edit, settings_window):
        """保存设置"""
        new_path = path_edit.text()
        if new_path != self.current_dict_path:
            self.current_dict_path = new_path
        
        # 保存配置到JSON文件
        config = {
            'current_dict_path': self.current_dict_path
        }
        
        with open(self.get_config_path(), 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        
        settings_window.accept()
    
    def open_about_window(self):
        """打开关于页面"""
        dialog = QDialog(self)
        dialog.setWindowTitle("关于")
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        dialog.setModal(True)
        
        # 设置窗口图标
        icon_path = self.resource_path("icon.ico")
        dialog.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(8)  # 减小间距
        layout.setContentsMargins(16, 16, 16, 16)  # 减小边距
        
        # 创建主框架
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 0px solid;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        main_layout = QVBoxLayout(main_frame)
        main_layout.setSpacing(8)  # 减小间距
        
        # 标题
        title_label = QLabel("日文汉字 - 假名/罗马音转换工具")
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1f1f1f;
            margin-bottom: 2px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel("这是一款用于将日文汉字转换为假名和罗马音的工具。")
        desc_label.setStyleSheet("""
            font-size: 14px;
            color: #1f1f1f;
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)
        
        feature_label = QLabel("支持自定义词典，可以添加和编辑常用词汇。")
        feature_label.setStyleSheet("""
            font-size: 14px;
            color: #1f1f1f;
        """)
        feature_label.setAlignment(Qt.AlignCenter)
        feature_label.setWordWrap(True)
        main_layout.addWidget(feature_label)
        
        # 图片
        try:
            image_path = self.resource_path("hantokana.png")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                image_label = QLabel()
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # 减小图片尺寸
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("""
                    QLabel {
                        background-color: transparent;
                        border: 0px solid #d9d9d9;
                        border-radius: 4px;
                        padding: 2px;
                    }
                """)
                main_layout.addWidget(image_label)
        except Exception as e:
            print(f"加载图片失败: {str(e)}")
        
        # 版本信息
        version_label = QLabel("版本: 0.3")
        version_label.setStyleSheet("""
            font-size: 14px;
            color: #1f1f1f;
        """)
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)
        
        github_label = QLabel("https://github.com/kanocyann/hantokana")
        github_label.setStyleSheet("""
            font-size: 14px;
            color: #73BBA3;
        """)
        github_label.setAlignment(Qt.AlignCenter)
        github_label.setCursor(Qt.PointingHandCursor)
        github_label.mousePressEvent = lambda e: QDesktopServices.openUrl(QUrl("https://github.com/kanocyann/hantokana"))
        main_layout.addWidget(github_label)
        
        layout.addWidget(main_frame)
        
        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.setFixedWidth(100)  # 减小按钮宽度
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #73BBA3;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #88D66C;
            }
            QPushButton:pressed {
                background-color: #88D66C;
            }
        """)
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)
        
        # 设置最小大小
        dialog.setMinimumSize(450, 400)  # 增加宽度，减小高度
        
        # 居中显示
        dialog.move(self.frameGeometry().center() - dialog.rect().center())
        dialog.exec()
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        dialog = CustomMessageBox(self, "确认退出", "确定要退出应用程序吗？", style='question')
        if dialog.exec() == QDialog.Accepted:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle(QStyleFactory.create("Fusion"))
    
    # 设置默认字体
    font = QFont("Microsoft YaHei UI", 9)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())