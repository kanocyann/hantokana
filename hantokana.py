import sys
import os
import json
from ctypes import windll
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QCheckBox, QLabel, QDialog,
                              QFileDialog, QMenu, QListWidget, QLineEdit, 
                             QFrame, QStyleFactory, QTableWidget, QTableWidgetItem, QHeaderView,
                             QSizePolicy, QComboBox, QStyledItemDelegate, QStyle)
from PySide6.QtCore import Qt, QUrl, QRect, QSize, QTimer, QRectF
from PySide6.QtGui import (QIcon, QAction, QFont, QPixmap, QDesktopServices, QPainter, 
                          QPen, QColor, QKeySequence, QShortcut, QTextOption, QTextDocument, QPalette)
import jaconv
import pykakasi
from fugashi import Tagger
from PySide6.QtCore import QMimeData
import re

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
        
        if word_type == "compound_words":
            title = "复合词"
        elif word_type == "normal_words":
            title = "普通词"
        elif word_type == "common_combinations":
            title = "常见后缀组合"
        elif word_type == "prefix_combinations":
            title = "常见前缀组合"
        else:
            title = "自定义"
            
        self.setWindowTitle(f"编辑{title}词典")
        self.setWindowFlags(Qt.Window)
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
        if word_type == 'compound_words':
            label_text = '复合词'
        elif word_type == 'common_combinations':
            label_text = '词汇 (后接助词)'
        elif word_type == 'prefix_combinations':
            label_text = '助词 (前接词汇)'
        else:
            label_text = '汉字'
        word_label = QLabel(label_text)
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
        if word_type == 'compound_words':
            self.kanji_edit.setPlaceholderText("请输入复合词")
        elif word_type == 'common_combinations':
            self.kanji_edit.setPlaceholderText("请输入词汇 (如: それ、これ等)")
        elif word_type == 'prefix_combinations':
            self.kanji_edit.setPlaceholderText("请输入助词 (如: まで、から等)")
        else:
            self.kanji_edit.setPlaceholderText("请输入汉字或词汇")
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
        if word_type == 'common_combinations':
            self.reading_label = QLabel("对应助词 (用逗号间隔)")
        elif word_type == 'prefix_combinations':
            self.reading_label = QLabel("对应词汇 (用逗号间隔)")
        else:
            self.reading_label = QLabel("对应假名 (用逗号间隔)")
        self.reading_label.setStyleSheet("""
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
        input_layout.addWidget(self.reading_label)
        
        self.readings_edit = QLineEdit()
        if word_type == 'common_combinations':
            self.readings_edit.setPlaceholderText("请输入助词，多个助词用逗号分隔")
        elif word_type == 'prefix_combinations':
            self.readings_edit.setPlaceholderText("请输入词汇，多个词汇用逗号分隔")
        else:
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
            QListWidget::item:selected:focus {
                outline: none;
                border: 1px solid #73BBA3;
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
        
        # 获取右键点击的单元格位置
        item = self.table_widget.itemAt(position)
        if item:
            row = self.table_widget.row(item)
            column = self.table_widget.column(item)
            
            # 添加编辑选项
            edit_action = menu.addAction("编辑")
            edit_action.triggered.connect(lambda: self.on_cell_double_clicked(row, column))
            
            # 添加复制选项
            menu.addSeparator()
            copy_action = menu.addAction("复制")
            copy_action.triggered.connect(self.copy_selection)
        else:
            # 如果没有选中单元格，只显示复制选项
            copy_action = menu.addAction("复制")
            copy_action.triggered.connect(self.copy_selection)
        
        menu.exec_(self.table_widget.viewport().mapToGlobal(position))
    
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
        
        # 确保词典中存在所需的键
        if self.word_type not in self.custom_dict:
            self.custom_dict[self.word_type] = {}
            
        word_dict = self.custom_dict[self.word_type]
        
        if self.word_type == "common_combinations" or self.word_type == "prefix_combinations":
            # 组合词典的显示方式
            for word, particles in sorted(word_dict.items()):
                self.list_widget.addItem(f"{word} → {', '.join(particles)}")
        else:
            # 普通词和复合词的显示方式
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
        
        # 分割读音为列表
        readings_list = self.split_readings(reading)
        
        # 直接更新词典
        self.custom_dict[self.word_type][word] = readings_list
        
        self.update_dict_view()
        
        # 保存到文件
        try:
            dict_path = self.parent().current_dict_path or self.parent().get_dict_path()
            os.makedirs(os.path.dirname(dict_path), exist_ok=True)
            with open(dict_path, "w", encoding="utf-8") as f:
                json.dump(self.custom_dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            CustomMessageBox(self, "错误", f"保存词条时出错: {str(e)}", style='error').exec()
            return
        
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
        item_text = item.text()
        
        # 提取词条和读音
        if " → " in item_text:
            parts = item_text.split(" → ")
            word = parts[0]
            reading_part = parts[1]
        
            # 设置词条和读音
            self.kanji_edit.setText(word)
            self.readings_edit.setText(reading_part)
        else:
            # 如果格式不对，直接使用整个文本作为词条
            self.kanji_edit.setText(item_text)
            self.readings_edit.clear()
        
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
                item_text = item.text()
                
                # 提取词条
                if " → " in item_text:
                    word = item_text.split(" → ")[0]
                    if word in self.custom_dict[self.word_type]:
                        del self.custom_dict[self.word_type][word]
                else:
                    # 如果格式不对，尝试直接使用整个文本作为词条
                    word = item_text
                    if word in self.custom_dict[self.word_type]:
                        del self.custom_dict[self.word_type][word]
            
            self.update_dict_view()
            
            # 保存到文件
            try:
                dict_path = self.parent().current_dict_path or self.parent().get_dict_path()
                os.makedirs(os.path.dirname(dict_path), exist_ok=True)
                with open(dict_path, "w", encoding="utf-8") as f:
                    json.dump(self.custom_dict, f, ensure_ascii=False, indent=2)
            except Exception as e:
                CustomMessageBox(self, "错误", f"保存词条时出错: {str(e)}", style='error').exec()
                return
            
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
    # 常见的单独助词
    pure_particles = {
        # 格助词
        'が', 'の', 'を', 'に', 'へ', 'で', 'と', 'から', 'まで', 'より',
        
        # 提示助词
        'は', 'も',
        
        # 接续助词
        'て', 'で', 'ば', 'と', 'けど', 'けれど', 'が', 'のに', 'し',
        
        # 终助词
        'か', 'な', 'ね', 'よ', 'わ', 'ぞ', 'ぜ', 'さ',
        
        # 副助词
        'だけ', 'ばかり', 'まで', 'など', 'なり', 'くらい', 'ぐらい', 'しか',
        
        # 并列助词
        'や', 'とか', 'だの',
        
        # 系助词
        'だ', 'です', 'ます', 'である',
        
        # 其他
        'って', 'じゃ'
    }

    # 常见的复合助词
    compound_particles_map = {
        # だ系列
        ('だ', 'って'): 'だって',
        ('だ', 'けど'): 'だけど',
        ('だ', 'から'): 'だから',
        ('だ', 'し'): 'だし',
        ('じゃ', 'ない'): 'じゃない',
        ('で', 'は'): 'では',
        ('じゃ', 'ありません'): 'じゃありません',
        
        # て系列
        ('て', 'いる'): 'ている',
        ('て', 'いた'): 'ていた',
        ('て', 'ない'): 'てない',
        ('て', 'は'): 'ては',
        ('て', 'も'): 'ても',
        ('て', 'から'): 'てから',
        
        # って系列
        ('って', 'いる'): 'っている',
        ('って', 'いた'): 'っていた',
        ('って', 'ない'): 'ってない',
        
        # に系列
        ('に', 'は'): 'には',
        ('に', 'も'): 'にも',
        ('に', 'よって'): 'によって',
        ('に', 'ついて'): 'について',
        ('に', 'とって'): 'にとって',
        ('に', 'おいて'): 'において',
        ('に', 'よる'): 'による',
        ('に', 'わたって'): 'にわたって',
        ('に', 'したがって'): 'にしたがって',
        ('に', 'かけて'): 'にかけて',
        ('ため', 'に'): 'ために',
        ('為', 'に'): 'ために',
        
        # の系列
        ('の', 'は'): 'のは',
        ('の', 'も'): 'のも',
        ('の', 'で'): 'ので',
        ('の', 'に'): 'のに',
        
        # と系列
        ('と', 'は'): 'とは',
        ('と', 'も'): 'とも',
        ('と', 'して'): 'として',
        ('と', 'しても'): 'としても',
        
        # から系列
        ('から', 'は'): 'からは',
        ('から', 'も'): 'からも',
        ('から', 'の'): 'からの',
        ('から', 'こそ'): 'からこそ',
        
        # まで系列
        ('まで', 'は'): 'までは',
        ('まで', 'も'): 'までも',
        ('まで', 'の'): 'までの',
        ('まで', 'に'): 'までに',
        
        # で系列
        ('で', 'も'): 'でも',
        ('で', 'は'): 'では',
        ('で', 'の'): 'での',
        
        # へ系列
        ('へ', 'は'): 'へは',
        ('へ', 'も'): 'へも',
        ('へ', 'の'): 'への',
        
        # その他
        ('かも', 'しれない'): 'かもしれない',
        ('なけれ', 'ば'): 'なければ',
        ('みたい', 'だ'): 'みたいだ',
        ('みたい', 'な'): 'みたいな',
        ('よう', 'だ'): 'ようだ',
        ('よう', 'な'): 'ような',
        ('べき', 'だ'): 'べきだ',
        ('はず', 'だ'): 'はずだ',
        ('そう', 'だ'): 'そうだ',
        ('そう', 'な'): 'そうな',
        ('なん', 'て'): 'なんて',
        ('なん', 'か'): 'なんか',
        ('くらい', 'は'): 'くらいは',
        ('ぐらい', 'は'): 'ぐらいは',
        
        # 常见指示词组合
        ('それ', 'じゃ'): 'それじゃ',
        ('それ', 'では'): 'それでは',
        ('これ', 'じゃ'): 'これじゃ',
        ('これ', 'では'): 'これでは',
        ('あれ', 'じゃ'): 'あれじゃ',
        ('あれ', 'では'): 'あれでは',
        ('どれ', 'じゃ'): 'どれじゃ',
        ('どれ', 'では'): 'どれでは',
        
        # 常见代词组合
        ('わたし', 'は'): 'わたしは',
        ('あなた', 'は'): 'あなたは',
        ('かれ', 'は'): 'かれは',
        ('かのじょ', 'は'): 'かのじょは',
        ('だれ', 'が'): 'だれが',
        ('なに', 'が'): 'なにが',
        ('どこ', 'で'): 'どこで',
        ('いつ', 'も'): 'いつも'
    }

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
            "compound_words": {},
            "common_combinations": {},
            "prefix_combinations": {}
        }
        self.current_dict_path = None
        self.tagger = None
        self.conv = None
        self.dict_search_dialog = None  # 添加词典搜索对话框变量
        
        # 加载配置和字典
        self.load_config()
        self.load_custom_dict()
        
        # 创建主窗口部件
        self.setup_ui()
        
        # 设置快捷键
        self.setup_shortcuts()
        
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
        
        edit_prefix_combinations_action = QAction("编辑前缀组合词典", self)
        edit_prefix_combinations_action.triggered.connect(lambda: self.open_edit_dict_window("prefix_combinations"))
        file_menu.addAction(edit_prefix_combinations_action)
        
        edit_combinations_action = QAction("编辑后缀组合词典", self)
        edit_combinations_action.triggered.connect(lambda: self.open_edit_dict_window("common_combinations"))
        file_menu.addAction(edit_combinations_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 设置菜单
        settings_menu = menubar.addMenu("设置")
        dict_path_action = QAction("设置默认词库路径", self)
        dict_path_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(dict_path_action)
        
        # 添加词典搜索菜单项
        dict_search_action = QAction("词典搜索", self)
        dict_search_action.triggered.connect(self.open_dict_search)
        settings_menu.addAction(dict_search_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.open_about_window)
        help_menu.addAction(about_action)
    
    def load_config(self):
        """加载配置"""
        config = {}
        try:
            if os.path.exists(self.get_config_path()):
                with open(self.get_config_path(), 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_dict_path = config.get('current_dict_path', self.current_dict_path)
        except Exception as e:
            print(f"加载配置时出错: {e}")
            # 如果加载失败，使用默认配置
            self.current_dict_path = self.resource_path("dictionary.txt")
        return config  # 始终返回一个字典，即使是空的
    
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
                            "compound_words": {},
                            "common_combinations": {},
                            "prefix_combinations": {}
                        }, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"初始化字典文件失败: {str(e)}")

        try:
            with open(custom_dict_path, "r", encoding="utf-8") as f:
                self.custom_dict = json.load(f)
                
            # 确保词典包含所有必要的键
            if "normal_words" not in self.custom_dict:
                self.custom_dict["normal_words"] = {}
            if "compound_words" not in self.custom_dict:
                self.custom_dict["compound_words"] = {}
            if "common_combinations" not in self.custom_dict:
                self.custom_dict["common_combinations"] = {}
            if "prefix_combinations" not in self.custom_dict:
                self.custom_dict["prefix_combinations"] = {}
                
            self.current_dict_path = custom_dict_path
        except Exception as e:
            print(f"加载字典文件失败: {str(e)}")
            self.custom_dict = {
                "normal_words": {},
                "compound_words": {},
                "common_combinations": {},
                "prefix_combinations": {}
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
    
    def save_config(self, config):
        """保存配置到文件"""
        config_path = self.get_config_path()
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
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
        # 使用新的API
        kks = pykakasi.Kakasi()
        # 配置转换选项
        kks.options = {
            "H": "a",  # 平假名转罗马字
            "K": "a",  # 片假名转罗马字
            "J": "a",  # 汉字转罗马字
            "r": "Hepburn"  # 使用平文式罗马字
        }
        return kks
    
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
            # 在分词前先检查前缀组合
            prefix_combinations = self.custom_dict.get("prefix_combinations", {})
            pre_processed_text = raw
            
            # 检查每个前缀组合
            for prefix, targets in prefix_combinations.items():
                for target in targets:
                    # 如果文本中包含前缀+目标词的组合

                    
                    # 也检查目标词+前缀的组合（因为分词可能会颠倒顺序）
                    if target + prefix in raw:

                        # 创建一个特殊的词条
                        word = target + prefix
                        readings = []
                        
                        # 使用pykakasi转换
                        converted = self.conv.convert(word)
                        if converted:
                            # 提取读音（假名形式）
                            reading = ''.join([item.get('hira', item.get('orig', '')) for item in converted])
                            if reading:
                                readings = [reading]
                        
                        # 处理所有读音
                        if readings:
                            line = f"[{word}]"
                            
                            if self.use_hira.isChecked():
                                # 平假名：先统一转换为平假名
                                hira_readings = []
                                for reading in readings:
                                    # 如果是片假名，先转换为平假名
                                    hira_reading = jaconv.kata2hira(reading)
                                    hira_readings.append(hira_reading)
                                line += f" → [{', '.join(hira_readings)}]"
                            
                            if self.use_kata.isChecked():
                                # 片假名：先统一转换为平假名，再转换为片假名
                                kata_readings = []
                                for reading in readings:
                                    # 先统一转换为平假名，再转换为片假名
                                    hira_reading = jaconv.kata2hira(reading)
                                    kata_reading = jaconv.hira2kata(hira_reading)
                                    kata_readings.append(kata_reading)
                                line += f" → [{', '.join(kata_readings)}]"
                            
                            if self.use_roma.isChecked():
                                # 罗马音：先统一转换为平假名，再转换为罗马音
                                roma_readings = []
                                for reading in readings:
                                    # 先统一转换为平假名
                                    hira_reading = jaconv.kata2hira(reading)
                                    roma_reading = self.convert_to_romaji(hira_reading)
                                    roma_readings.append(roma_reading)
                                line += f" → [{', '.join(roma_readings)}]"
                            
                            result += line + "\n"
                            
                            # 从原始文本中移除已处理的组合
                            pre_processed_text = pre_processed_text.replace(target + prefix, "")
                    
                    # 检查前缀+目标词的组合
                    if prefix + target in raw:

                        # 创建一个特殊的词条
                        word = prefix + target
                        readings = []
                        
                        # 使用pykakasi转换
                        converted = self.conv.convert(word)
                        if converted:
                            # 提取读音（假名形式）
                            reading = ''.join([item.get('hira', item.get('orig', '')) for item in converted])
                            if reading:
                                readings = [reading]
                        
                        # 处理所有读音
                        if readings:
                            line = f"[{word}]"
                            
                            if self.use_hira.isChecked():
                                # 平假名：先统一转换为平假名
                                hira_readings = []
                                for reading in readings:
                                    # 如果是片假名，先转换为平假名
                                    hira_reading = jaconv.kata2hira(reading)
                                    hira_readings.append(hira_reading)
                                line += f" → [{', '.join(hira_readings)}]"
                            
                            if self.use_kata.isChecked():
                                # 片假名：先统一转换为平假名，再转换为片假名
                                kata_readings = []
                                for reading in readings:
                                    # 先统一转换为平假名，再转换为片假名
                                    hira_reading = jaconv.kata2hira(reading)
                                    kata_reading = jaconv.hira2kata(hira_reading)
                                    kata_readings.append(kata_reading)
                                line += f" → [{', '.join(kata_readings)}]"
                            
                            if self.use_roma.isChecked():
                                # 罗马音：先统一转换为平假名，再转换为罗马音
                                roma_readings = []
                                for reading in readings:
                                    # 先统一转换为平假名
                                    hira_reading = jaconv.kata2hira(reading)
                                    roma_reading = self.convert_to_romaji(hira_reading)
                                    roma_readings.append(roma_reading)
                                line += f" → [{', '.join(roma_readings)}]"
                            
                            result += line + "\n"
                            
                            # 从原始文本中移除已处理的组合
                            pre_processed_text = pre_processed_text.replace(prefix + target, "")
            
            # 如果已经处理了所有文本，直接返回结果
            if pre_processed_text.strip() == "":
                self.text_output.setPlainText(result.strip())
                return
            
            # 否则继续正常分词处理
            # 先进行正常分词
            words = self.tagger(raw)
            

            
            # 使用集合来跟踪已处理的词，避免重复
            processed_words = set()
            
            # 定义常见的动词词尾
            verb_endings = ['て', 'た', 'ない', 'ます', 'る', 'れる', 'せる', 'らる', 'られる', 'させる', 'てらっしゃい', 'でらっしゃい', 'ください', 'なさい', 'たり', 'だり', 'ちゃう', 'じゃう', 'てる', 'でる', 'とく', 'どく', 'とる', 'どる', 'てみる', 'でみる']
            
            # 定义常见的助动词和语气词组合
            auxiliary_endings = ['たい', 'たく', 'たかっ', 'たけれ', 'たかろ', 'ない', 'なく', 'なかっ', 'なけれ', 'なかろ', 'ます', 'ました', 'ません', 'ませんでした', 'んだ', 'んです', 'のだ', 'のです', 'そうだ', 'そうです', 'ようだ', 'ようです', 'みたいだ', 'みたいです', 'はずだ', 'はずです', 'べきだ', 'べきです', 'ことになる', 'ことにする', 'ことがある', 'ことができる']
            
            # 定义需要优先作为整体处理的助动词组合
            priority_compounds = ['いたいんだ', 'たいんだ', 'なければ', 'ならない', 'かもしれない', 'てしまう', 'でしまう', 'ていく', 'でいく', 'てくる', 'でくる', 'ておく', 'でおく', 'なければならない', 'ことができる', 'ようにする', 'ようにしている', 'ことになっている', 'ことにしている']
            
            # 从自定义词典中获取指示词和助词组合
            # 使用get方法确保即使词典中没有这个键也能返回空字典
            common_combinations = self.custom_dict.get("common_combinations", {})
            prefix_combinations = self.custom_dict.get("prefix_combinations", {})
            
            
            i = 0
            while i < len(words):
                # 尝试合并复合词
                for j in range(len(words), i, -1):
                    combined = ''.join([w.surface for w in words[i:j]])
                    if combined in self.custom_dict["compound_words"] or combined in priority_compounds:
                        word = combined
                        i = j
                        break
                else:
                    # 检查常见组合
                    if i + 1 < len(words):
                        current_word = words[i].surface
                        next_word = words[i + 1].surface
                        
                        # 检查是否是常见的指示词+助词组合（后缀模式）
                        if current_word in common_combinations and next_word in common_combinations[current_word]:
                            word = current_word + next_word
                            i += 2

                            continue
                        
                        # 检查是否是常见的助词+指示词组合（前缀模式）
                        if current_word in prefix_combinations and next_word in prefix_combinations[current_word]:
                            word = current_word + next_word
                            i += 2

                            continue
                        
                        # 另一种检查前缀组合的方式 - 直接遍历前缀组合词典
                        found_prefix = False
                        for prefix, targets in prefix_combinations.items():
                            if current_word == prefix and next_word in targets:
                                word = current_word + next_word
                                i += 2

                                found_prefix = True
                                break
                            
                            # 也检查目标词+前缀的组合（因为分词可能会颠倒顺序）
                            if next_word == prefix and current_word in targets:
                                word = current_word + next_word
                                i += 2

                                found_prefix = True
                                break
                        
                        if found_prefix:
                            continue
                        
                        # 检查当前词是否以促音结尾
                        if current_word.endswith(('っ', 'ッ')):
                            # 合并促音和后续词
                            word = current_word + next_word
                            i += 2
                        # 检查是否是常见的促音组合
                        elif (i + 1 < len(words) and 
                              ('っ' in current_word or 'ッ' in current_word) and
                              any(x in next_word for x in ['て', 'た', 'ち', 'つ', 'と'])):
                            word = current_word + next_word
                            i += 2
                        # 检查是否是敬语形式
                        elif (i + 1 < len(words) and 
                              (next_word == 'てらっしゃい' or next_word == 'でらっしゃい' or 
                               next_word == 'ください' or next_word == 'なさい' or
                               'いらっしゃ' in next_word or 'おっしゃ' in next_word or
                               'くださ' in next_word or 'なさ' in next_word or
                               'ござい' in next_word or 'いただ' in next_word or
                               'いたし' in next_word or 'になる' in next_word or
                               'します' in next_word or 'しました' in next_word)):
                            word = current_word + next_word
                            i += 2
                        # 检查是否是动词词干+词尾的情况
                        elif next_word in verb_endings or next_word in auxiliary_endings:
                            # 检查是否是汉字+动词词尾的常见模式
                            if any(ord(c) in range(0x4E00, 0x9FFF) for c in current_word):
                                # 特殊处理敬语形式
                                if (next_word in ['てらっしゃい', 'でらっしゃい', 'ください', 'なさい'] or 
                                    'らっしゃ' in next_word or 'いらっしゃ' in next_word or 'おっしゃ' in next_word or
                                    'くださ' in next_word or 'なさ' in next_word or 'ござい' in next_word or
                                    'いただ' in next_word or 'いたし' in next_word or 'になる' in next_word or
                                    'ます' in next_word or 'ました' in next_word or 'ません' in next_word or
                                    'です' in next_word or 'でした' in next_word or 'でしょ' in next_word or
                                    'お' == next_word[0:1] or 'ご' == next_word[0:1]):
                                    # 尝试合并更多的敬语部分
                                    combined_word = current_word + next_word
                                    i += 2
                                    # 检查是否还有更多部分需要合并
                                    while i < len(words) and (
                                        words[i].surface in ['ます', 'ました', 'ません', 'ませんでした', 'です', 'でした',
                                                           'でしょう', 'でしょうか', 'ください', 'くださいませ', 'なさい'] or
                                        'ござい' in words[i].surface or 'いただ' in words[i].surface or
                                        'いたし' in words[i].surface):
                                        combined_word += words[i].surface
                                        i += 1
                                    word = combined_word
                                else:
                                    word = current_word + next_word
                                    i += 2
                            # 检查是否是假名动词词干+词尾或形容词+助动词组合
                            elif current_word.endswith(('し', 'き', 'ち', 'り', 'い', 'み', 'に', 'び', 'ぎ', 'く', 'か', 'さ', 'な')):
                                # 处理形容词+助动词的特殊情况
                                # 对于形容词く形式，我们优先保持其独立性，除非是特定组合
                                if current_word.endswith('く'):
                                    # 检查是否在自定义词典中有这个形容词
                                    if current_word in self.custom_dict["normal_words"]:
                                        word = current_word
                                        i += 1
                                    # 如果下一个词是特定助动词，且组合不在词典中，则分开处理
                                    elif next_word.startswith(('い', 'あ', 'お')) and f"{current_word}{next_word}" not in self.custom_dict["compound_words"]:
                                        word = current_word
                                        i += 1
                                    else:
                                        # 否则尝试合并
                                        combined_word = current_word + next_word
                                        i += 2
                                        # 检查是否还有更多部分需要合并
                                        while i < len(words) and (words[i].surface in auxiliary_endings or words[i].surface in ['だ', 'です']):
                                            combined_word += words[i].surface
                                            i += 1
                                        word = combined_word
                                else:
                                    word = current_word + next_word
                                    i += 2
                            # 检查是否是助动词+语气词组合
                            elif current_word in auxiliary_endings and next_word in ['だ', 'です', 'ん', 'の', 'でしょう', 'でございます']:
                                # 合并助动词和语气词
                                combined_word = current_word + next_word
                                i += 2
                                # 检查是否还有更多部分需要合并
                                while i < len(words) and (
                                    words[i].surface in ['だ', 'です', 'ね', 'よ', 'か', 'な', 'でしょう', 'でしょうか', 'ございます'] or
                                    'ござい' in words[i].surface or 'いただ' in words[i].surface or
                                    'いたし' in words[i].surface):
                                    combined_word += words[i].surface
                                    i += 1
                                word = combined_word
                            # 检查是否是敬语相关词汇
                            elif ('お' == current_word[0:1] or 'ご' == current_word[0:1]) and next_word in ['する', 'します', 'しました', 'いたします', 'いたしました']:
                                # 合并敬语表达
                                combined_word = current_word + next_word
                                i += 2
                                # 检查是否还有更多部分需要合并
                                while i < len(words) and (
                                    words[i].surface in ['ます', 'ました', 'ません', 'ませんでした', 'です', 'でした', 'でしょう', 'でしょうか']):
                                    combined_word += words[i].surface
                                    i += 1
                                word = combined_word
                            # 检查是否是片假名序列
                            elif all(ord(c) in range(0x30A0, 0x30FF) or c in 'ー・' for c in current_word if c.strip()):
                                merge_end = i + 1
                                kata_sequence = [current_word]
                                
                                while merge_end < len(words):
                                    next_word = words[merge_end].surface
                                    next_is_kata = all(ord(c) in range(0x30A0, 0x30FF) or c in 'ー・' for c in next_word if c.strip())
                                    if next_is_kata or next_word in ['ー', '・']:
                                        kata_sequence.append(next_word)
                                        merge_end += 1
                                    else:
                                        break
                                
                                if len(kata_sequence) > 1:
                                    word = ''.join(kata_sequence)
                                    i = merge_end
                                else:
                                    # 检查复合助词
                                    found_compound = False
                                    for k in range(1, 4):  # 最多检查3个词的组合
                                        if i + k <= len(words):
                                            word_tuple = tuple(w.surface for w in words[i:i+k])
                                            if word_tuple in self.compound_particles_map:
                                                word = self.compound_particles_map[word_tuple]
                                                i += k
                                                found_compound = True
                                                break
                                    
                                    if not found_compound:
                                        word = words[i].surface
                                        i += 1
                            else:
                                # 检查复合助词
                                found_compound = False
                                for k in range(1, 4):  # 最多检查3个词的组合
                                    if i + k <= len(words):
                                        word_tuple = tuple(w.surface for w in words[i:i+k])
                                        if word_tuple in self.compound_particles_map:
                                            word = self.compound_particles_map[word_tuple]
                                            i += k
                                            found_compound = True
                                            break
                                
                                if not found_compound:
                                    word = words[i].surface
                                    i += 1
                        # 检查是否是片假名序列
                        elif all(ord(c) in range(0x30A0, 0x30FF) or c in 'ー・' for c in current_word if c.strip()):
                            merge_end = i + 1
                            kata_sequence = [current_word]
                            
                            while merge_end < len(words):
                                next_word = words[merge_end].surface
                                next_is_kata = all(ord(c) in range(0x30A0, 0x30FF) or c in 'ー・' for c in next_word if c.strip())
                                if next_is_kata or next_word in ['ー', '・']:
                                    kata_sequence.append(next_word)
                                    merge_end += 1
                                else:
                                    break
                            
                            if len(kata_sequence) > 1:
                                word = ''.join(kata_sequence)
                                i = merge_end
                            else:
                                # 检查复合助词
                                found_compound = False
                                for k in range(1, 4):  # 最多检查3个词的组合
                                    if i + k <= len(words):
                                        word_tuple = tuple(w.surface for w in words[i:i+k])
                                        if word_tuple in self.compound_particles_map:
                                            word = self.compound_particles_map[word_tuple]
                                            i += k
                                            found_compound = True
                                            break
                                
                                if not found_compound:
                                    word = words[i].surface
                                    i += 1
                        else:
                            # 检查复合助词
                            found_compound = False
                            for k in range(1, 4):  # 最多检查3个词的组合
                                if i + k <= len(words):
                                    word_tuple = tuple(w.surface for w in words[i:i+k])
                                    if word_tuple in self.compound_particles_map:
                                        word = self.compound_particles_map[word_tuple]
                                        i += k
                                        found_compound = True
                                        break
                            
                            if not found_compound:
                                word = words[i].surface
                                i += 1
                    else:
                        word = words[i].surface
                        i += 1

                # 如果这个词已经处理过，跳过
                if word in processed_words:
                    continue
                
                processed_words.add(word)

                # 对于纯中文文本或非日文字符，直接跳过转换
                if not any(
                    ord(char) in range(0x3040, 0x309F) or  # 平假名
                    ord(char) in range(0x30A0, 0x30FF) or  # 片假名
                    ord(char) in range(0x4E00, 0x9FFF)     # 汉字
                    for char in word
                ):
                    continue

                # 优先使用自定义词典
                readings = self.custom_dict["normal_words"].get(word) or self.custom_dict["compound_words"].get(word)
                
                if not readings:
                    # 使用pykakasi转换
                    converted = self.conv.convert(word)
                    if converted:
                        # 提取读音（假名形式）
                        reading = ''.join([item.get('hira', item.get('orig', '')) for item in converted])
                        if reading:
                            readings = [reading]

                # 处理所有读音
                if readings:
                    line = f"[{word}]"
                    
                    if self.use_hira.isChecked():
                        # 平假名：先统一转换为平假名
                        hira_readings = []
                        for reading in readings:
                            # 如果是片假名，先转换为平假名
                            hira_reading = jaconv.kata2hira(reading)
                            hira_readings.append(hira_reading)
                        line += f" → [{', '.join(hira_readings)}]"
                    
                    if self.use_kata.isChecked():
                        # 片假名：先统一转换为平假名，再转换为片假名
                        kata_readings = []
                        for reading in readings:
                            # 先统一转换为平假名，再转换为片假名
                            hira_reading = jaconv.kata2hira(reading)
                            kata_reading = jaconv.hira2kata(hira_reading)
                            kata_readings.append(kata_reading)
                        line += f" → [{', '.join(kata_readings)}]"
                    
                    if self.use_roma.isChecked():
                        # 罗马音：先统一转换为平假名，再转换为罗马音
                        roma_readings = []
                        for reading in readings:
                            # 先统一转换为平假名
                            hira_reading = jaconv.kata2hira(reading)
                            roma_reading = self.convert_to_romaji(hira_reading)
                            roma_readings.append(roma_reading)
                        line += f" → [{', '.join(roma_readings)}]"
                    
                    result += line + "\n"
            
            self.text_output.setPlainText(result.strip())
        except Exception as e:
            CustomMessageBox(self, "错误", str(e), style='error').exec()

    def convert_to_romaji(self, kana_text):
        """将假名转换为罗马音，正确处理促音和拗音"""
        romaji = ""
        i = 0
        
        while i < len(kana_text):
            char = kana_text[i]
            
            if char in ['っ', 'ッ']:  # 促音
                if i + 1 < len(kana_text):
                    next_char = kana_text[i + 1]
                    
                    # 检查是否是拗音组合
                    if (i + 2 < len(kana_text) and 
                        kana_text[i + 2] in ['ゃ', 'ゅ', 'ょ', 'ャ', 'ュ', 'ョ']):
                        # 处理拗音中的促音 (如っしゃ)
                        yoon_combo = next_char + kana_text[i + 2]
                        yoon_result = self.conv.convert(yoon_combo)
                        if yoon_result:
                            roma = yoon_result[0].get('hepburn', '')
                            # 双写第一个辅音
                            if roma and roma[0] not in 'aeiou':
                                romaji += roma[0] + roma
                            else:
                                romaji += roma
                        i += 3
                    else:
                        # 普通促音处理
                        next_result = self.conv.convert(next_char)
                        if next_result:
                            roma = next_result[0].get('hepburn', '')
                            # 双写第一个辅音
                            if roma and roma[0] not in 'aeiou':
                                romaji += roma[0] + roma
                            else:
                                romaji += roma
                        i += 2
                else:
                    i += 1
            elif (i + 1 < len(kana_text) and 
                kana_text[i + 1] in ['ゃ', 'ゅ', 'ょ', 'ャ', 'ュ', 'ョ']):
                # 处理拗音
                yoon_combo = kana_text[i:i+2]
                yoon_result = self.conv.convert(yoon_combo)
                if yoon_result:
                    romaji += yoon_result[0].get('hepburn', '')
                i += 2
            else:
                # 普通假名
                char_result = self.conv.convert(char)
                if char_result:
                    romaji += char_result[0].get('hepburn', '')
                i += 1
        
        return romaji

   
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
                    
                    # 合并common_combinations
                    if "common_combinations" in new_dict:
                        # 确保custom_dict中有common_combinations键
                        if "common_combinations" not in self.custom_dict:
                            self.custom_dict["common_combinations"] = {}
                            
                        # 合并common_combinations字典
                        for word, particles in new_dict["common_combinations"].items():
                            if word in self.custom_dict["common_combinations"]:
                                # 如果单词已存在，合并助词列表（去重）
                                existing_particles = set(self.custom_dict["common_combinations"][word])
                                new_particles = set(particles)
                                self.custom_dict["common_combinations"][word] = list(existing_particles.union(new_particles))
                            else:
                                # 如果单词不存在，直接添加
                                self.custom_dict["common_combinations"][word] = particles
                    
                    # 合并prefix_combinations
                    if "prefix_combinations" in new_dict:
                        # 确保custom_dict中有prefix_combinations键
                        if "prefix_combinations" not in self.custom_dict:
                            self.custom_dict["prefix_combinations"] = {}
                            
                        # 合并prefix_combinations字典
                        for word, prefixes in new_dict["prefix_combinations"].items():
                            if word in self.custom_dict["prefix_combinations"]:
                                # 如果单词已存在，合并前缀列表（去重）
                                existing_prefixes = set(self.custom_dict["prefix_combinations"][word])
                                new_prefixes = set(prefixes)
                                self.custom_dict["prefix_combinations"][word] = list(existing_prefixes.union(new_prefixes))
                            else:
                                # 如果单词不存在，直接添加
                                self.custom_dict["prefix_combinations"][word] = prefixes
                    
                    # 保存到当前使用的词库文件
                    dict_path = self.current_dict_path or self.get_dict_path()
                    os.makedirs(os.path.dirname(dict_path), exist_ok=True)
                    with open(dict_path, "w", encoding="utf-8") as f:
                        json.dump(self.custom_dict, f, ensure_ascii=False, indent=2)
                    
                    CustomMessageBox(self, "成功", "词典导入并合并成功", style='success').exec()
                else:
                    CustomMessageBox(self, "警告", "所选文件格式无效，请选择一个有效的 JSON 文件", style='warning').exec()
            except Exception as e:
                CustomMessageBox(self, "错误", f"导入词典时发生错误: {e}", style='error').exec()
    
    def open_edit_dict_window(self, word_type, target_word=None):
        """打开词典编辑窗口
        
        Args:
            word_type: 词典类型
            target_word: 可选，需要定位的词条
        """
        dialog = DictEditDialog(self, word_type, self.custom_dict)
        # 设置窗口图标
        icon_path = self.resource_path("icon.ico")
        dialog.setWindowIcon(QIcon(icon_path))
        
        # 如果指定了目标词条，尝试定位
        if target_word:
            # 查找并选择目标词条
            for i in range(dialog.list_widget.count()):
                item = dialog.list_widget.item(i)
                if item.text().startswith(f"{target_word} →"):
                    dialog.list_widget.setCurrentItem(item)
                    # 滚动到该项
                    dialog.list_widget.scrollToItem(item)
                    # 自动填充到编辑框
                    dialog.edit_entry()
                    break
        
        if dialog.exec() == QDialog.Accepted:
            # 更新主窗口的词典数据
            self.custom_dict = dialog.custom_dict
            # 保存到文件
            self.save_custom_dict()
    
    def open_settings_window(self):
        """打开设置窗口"""
        dialog = QDialog(self)
        dialog.setWindowTitle("设置")
        dialog.setWindowFlags(Qt.Window)
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
        dialog.setWindowFlags(Qt.Window)
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
        version_label = QLabel("版本: 0.3.1")
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
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # 添加Ctrl+F快捷键
        search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        search_shortcut.activated.connect(self.open_dict_search)
    
    def open_dict_search(self):
        """打开词典搜索对话框"""
        if not self.dict_search_dialog:
            self.dict_search_dialog = DictSearchDialog(self)
        
        # 如果对话框已经打开，则刷新数据
        if self.dict_search_dialog.isVisible():
            self.dict_search_dialog.load_dict_data()
        else:
            self.dict_search_dialog.show()

class DictSearchDialog(QDialog):
    """词典搜索对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("词典搜索")
        self.setWindowFlags(Qt.Window)
        self.setModal(False)  # 非模态对话框，可以与主窗口交互
        self.setMinimumSize(1100, 400)
        
        # 初始化用户调整列宽的标志
        self.is_user_resizing = False
        
        # 初始化列宽比例
        self.column_ratios = [0.45, 0.45, 0.10]  # 词条45%，读音45%，类型10%
        
        # 词典数据和分页相关变量
        self.all_entries = []  # 存储所有词条
        self.filtered_entries = []  # 存储筛选后的词条
        self.current_page = 1
        self.entries_per_page = 50
        self.current_type = "全部"  # 当前选中的词条类型
        self.search_timer = QTimer()  # 用于延迟搜索，提高性能
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        
        # 设置窗口图标
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
        
        # 搜索区域
        search_frame = QFrame()
        search_frame.setFrameStyle(QFrame.StyledPanel)
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 1px solid #e8e8e8;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        search_layout = QVBoxLayout(search_frame)
        search_layout.setSpacing(8)
        search_layout.setContentsMargins(12, 12, 12, 12)
        
        # 搜索输入框和提示（放在同一行）
        search_input_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词搜索词典（用空格分隔多个关键词）...")
        self.search_edit.setStyleSheet("""
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
        """)
        self.search_edit.textChanged.connect(self.on_search_text_changed)
        search_input_layout.addWidget(self.search_edit)
        
        # 匹配计数标签
        self.match_count_label = QLabel("0 个匹配")
        self.match_count_label.setAlignment(Qt.AlignCenter)
        self.match_count_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 13px;
                padding: 0 10px;
                min-width: 120px;
                text-align: center;
            }
        """)
        search_input_layout.addWidget(self.match_count_label)
        
        search_layout.addLayout(search_input_layout)
        
        # 类型筛选区域
        filter_layout = QHBoxLayout()
        
        # 添加类型选择按钮
        self.type_buttons = {}
        types = ["全部", "普通词", "复合词", "前缀组合", "后缀组合"]
        
        for type_name in types:
            btn = QPushButton(type_name)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)  # 单选模式
            btn.setFixedHeight(32)
            
            # 设置现代化按钮样式
            btn.setStyleSheet("""
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
            """)
            
            # 设置"全部"按钮为默认选中
            if type_name == "全部":
                btn.setChecked(True)
            
            btn.clicked.connect(lambda checked, t=type_name: self.on_type_filter_clicked(t))
            filter_layout.addWidget(btn)
            self.type_buttons[type_name] = btn
        
        # 创建分页控件（先不添加到布局中，后面会添加到底部）
        self.page_info_label = QLabel("第 1 页 / 共 1 页")
        self.page_info_label.setStyleSheet("""
            QLabel {
                color: #73BBA3;
                font-size: 12px;
                padding: 0 10px;
                min-width: 110px;
                text-align: center;
            }
        """)
        
        # 设置按钮样式
        button_style = """
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
        
        # 首页按钮
        self.first_page_btn = QPushButton("首页")
        self.first_page_btn.setFixedWidth(60)
        self.first_page_btn.setFixedHeight(26)
        self.first_page_btn.clicked.connect(self.go_to_first_page)
        self.first_page_btn.setStyleSheet(button_style)
        
        # 上一页按钮
        self.prev_page_btn = QPushButton("上一页")
        self.prev_page_btn.setFixedWidth(60)
        self.prev_page_btn.setFixedHeight(26)
        self.prev_page_btn.clicked.connect(self.go_to_prev_page)
        self.prev_page_btn.setStyleSheet(button_style)
        
        # 下一页按钮
        self.next_page_btn = QPushButton("下一页")
        self.next_page_btn.setFixedWidth(60)
        self.next_page_btn.setFixedHeight(26)
        self.next_page_btn.clicked.connect(self.go_to_next_page)
        self.next_page_btn.setStyleSheet(button_style)
        
        # 尾页按钮
        self.last_page_btn = QPushButton("末页")
        self.last_page_btn.setFixedWidth(60)
        self.last_page_btn.setFixedHeight(26)
        self.last_page_btn.clicked.connect(self.go_to_last_page)
        self.last_page_btn.setStyleSheet(button_style)
        
        # 每页条数设置
        self.page_size_label = QLabel("每页显示：")
        self.page_size_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
                padding-right: 3px;
            }
        """)
        
        # 从配置文件加载每页条数
        config = self.parent.load_config() or {}  # 确保config不为None
        self.entries_per_page = config.get("entries_per_page", 50)
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["10", "20", "50", "100"])
        self.page_size_combo.setCurrentText(str(self.entries_per_page))
        self.page_size_combo.setFixedWidth(70)
        self.page_size_combo.setFixedHeight(26)
        # 确保下拉箭头可见
        self.page_size_combo.setEditable(False)  # 不可编辑
        self.page_size_combo.setFrame(True)      # 显示边框
        self.page_size_combo.setMaxVisibleItems(4)  # 最多显示4项
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        self.page_size_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 3px;
                padding: 1px 20px 1px 6px;
                background-color: white;
                font-size: 12px;
                min-width: 60px;
                selection-background-color: #73BBA3;
                selection-color: white;
            }
            QComboBox:hover {
                border-color: #73BBA3;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 16px;
                border-left: 1px solid #d9d9d9;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #f5f5f5;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #666666;
            }
            /* 下拉列表样式 */
            QComboBox QAbstractItemView {
                border: 1px solid #d9d9d9;
                border-radius: 3px;
                background-color: white;
                selection-background-color: #73BBA3;
                selection-color: white;
                padding: 2px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 20px;
                padding: 2px 6px;
                font-size: 12px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #E8F5E9;
                color: #333333;
            }
        """)
        
        # 不再需要提前创建分页布局，我们将在底部直接添加
        
        search_layout.addLayout(filter_layout)
        
        layout.addWidget(search_frame)
        
        # 表格区域
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        
        # 设置默认表头标签
        self.update_table_headers()
        
        # 设置表头可见
        self.table_widget.horizontalHeader().setVisible(True)
        
        # 让表格高度可以自动调整（不设置固定高度）
        self.table_widget.setMinimumHeight(450)  # 设置最小高度
        
        # 设置默认列宽
        self.table_widget.setColumnWidth(0, 300)
        self.table_widget.setColumnWidth(1, 300)
        self.table_widget.setColumnWidth(2, 100)
        
        # 设置最小列宽
        self.table_widget.horizontalHeader().setMinimumSectionSize(100)
        
        # 设置表头调整模式：所有列自动伸展填充可用空间
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        # 设置垂直表头宽度
        self.table_widget.verticalHeader().setFixedWidth(50)
        
        # 设置水平表头策略，确保拖动时保持其他列可见
        self.table_widget.horizontalHeader().setMinimumSectionSize(150)
        
        # 调整表格大小策略 - 在垂直方向上优先扩展
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        
        # 设置表格滚动条策略
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 需要时显示水平滚动条
        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 总是显示垂直滚动条
        
        # 优化表格性能和滚动行为
        self.table_widget.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table_widget.verticalScrollBar().setSingleStep(10)
        
        # 设置滚动范围扩展，确保能滚动到底部但不留太多空白
        self.table_widget.verticalScrollBar().setProperty("extraBottom", 5)
        
        # 设置表格调整大小策略
        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        
        # 连接列宽变化信号
        self.table_widget.horizontalHeader().sectionResized.connect(self.on_section_resized)
        
        # 设置表格右键菜单
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        # 设置复制快捷键
        copy_shortcut = QShortcut(QKeySequence.Copy, self.table_widget)
        copy_shortcut.activated.connect(self.copy_selection)
        
        # 连接双击信号
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        # 应用自定义代理来支持文本换行
        word_wrap_delegate = WordWrapDelegate(self.table_widget)
        self.table_widget.setItemDelegate(word_wrap_delegate)
        
        # 设置表格项居中对齐
        self.table_widget.setStyleSheet("""
            QTableWidget {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                background-color: white;
                font-size: 13px;
                selection-background-color: #E8F5E9;
                selection-color: #333333;
                outline: 0;  /* 移除整个表格的焦点轮廓 */
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f0f0f0;
                border: none;  /* 移除选中项的边框 */
                text-align: center;  /* 文字居中 */
                min-height: 30px;
                white-space: normal;  /* 允许文本换行 */
            }
            QTableWidget::item:selected {
                background-color: #E8F5E9;
                color: #73BBA3;
                border: none;  /* 移除选中项的边框 */
                outline: none;  /* 移除选中项的轮廓线 */
            }
            QTableWidget::item:focus {
                border: none;  /* 移除焦点项的边框 */
                outline: none;  /* 移除焦点项的轮廓线 */
            }
            QTableWidget:focus {
                outline: none;  /* 表格获得焦点时也不显示轮廓 */
                border: 1px solid #d9d9d9;  /* 保持相同的边框 */
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 6px;
                border: 1px solid #d9d9d9;
                font-weight: bold;
                text-align: center;  /* 表头文字居中 */
            }
            /* 垂直滚动条样式 */
            QTableWidget QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 16px;  /* 增加宽度 */
                border-radius: 0px;  /* 移除圆角 */
                margin: 0px;
                border: 1px solid #d9d9d9;
                border-left: none;
            }
            
            QTableWidget QScrollBar::handle:vertical {
                background-color: #a0a0a0;  /* 更深的颜色 */
                border-radius: 4px;
                min-height: 30px;  /* 增加最小高度 */
                margin: 3px;
            }
            
            QTableWidget QScrollBar::handle:vertical:hover {
                background-color: #808080;  /* 更深的悬停颜色 */
            }
            
            QTableWidget QScrollBar::handle:vertical:pressed {
                background-color: #606060;  /* 更深的按下颜色 */
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
            
            /* 水平滚动条样式 */
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
        """)
        
        # 设置页码标签样式保持一致的高度
        self.page_info_label.setMinimumHeight(26)
        self.page_info_label.setAlignment(Qt.AlignCenter)
        
        # 创建表格容器
        table_frame = QFrame()
        table_frame.setFrameStyle(QFrame.NoFrame)
        table_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_frame_layout = QVBoxLayout(table_frame)
        table_frame_layout.setContentsMargins(0, 0, 0, 0)
        table_frame_layout.setSpacing(0)
        
        # 添加表格到表格容器
        table_frame_layout.addWidget(self.table_widget)
        
        # 创建每页条数设置布局（右对齐）- 放在表格外部右下角
        page_size_widget = QWidget()
        page_size_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        page_size_widget.setFixedHeight(30)  # 设置固定高度
        page_size_layout = QHBoxLayout(page_size_widget)
        page_size_layout.setContentsMargins(0, 2, 6, 0)  # 调整边距
        page_size_layout.addStretch()  # 左侧弹性空间
        page_size_layout.addWidget(self.page_size_label)
        page_size_layout.addWidget(self.page_size_combo)
        
        # 设置样式确保与表格分离
        page_size_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        # 创建表格和控件的主容器布局
        table_container = QVBoxLayout()
        table_container.setContentsMargins(0, 0, 0, 0)
        table_container.setSpacing(4)  # 设置垂直间距
        
        # 添加表格框架和每页条数设置到主容器
        table_container.addWidget(table_frame)
        table_container.addWidget(page_size_widget)
        
        # 创建分页按钮容器 - 与表格保持小距离
        pagination_widget = QWidget()
        pagination_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        pagination_layout = QHBoxLayout(pagination_widget)
        pagination_layout.setContentsMargins(0, 4, 0, 0)  # 调整上下边距
        
        # 创建分页按钮布局
        pagination_buttons = QHBoxLayout()
        pagination_buttons.setSpacing(4)  # 减小按钮之间的间距
        pagination_buttons.addWidget(self.first_page_btn)
        pagination_buttons.addWidget(self.prev_page_btn)
        pagination_buttons.addWidget(self.page_info_label)
        pagination_buttons.addWidget(self.next_page_btn)
        pagination_buttons.addWidget(self.last_page_btn)
        
        # 将分页按钮居中放置
        pagination_layout.addStretch(1)  # 左侧弹性空间
        pagination_layout.addLayout(pagination_buttons)  # 分页按钮居中
        pagination_layout.addStretch(1)  # 右侧弹性空间
        
        # 添加分页布局到表格容器
        table_container.addWidget(pagination_widget)
        
        # 将整个容器添加到主布局
        layout.addLayout(table_container)
        
        # 更新布局
        self.remove_focus_rect()
        self.update_page_controls()
    
    def remove_focus_rect(self):
        """移除表格项的焦点框并优化表格外观"""
        # 设置表格焦点策略为点击焦点，允许选择但不显示焦点框
        self.table_widget.setFocusPolicy(Qt.ClickFocus)
        
        # 禁用表格的项目编辑但允许选择
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # 启用表格的项目选择，允许选择多个单元格以便复制
        self.table_widget.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table_widget.setSelectionBehavior(QTableWidget.SelectItems)  # 允许选择单元格而非整行
        
        # 设置行号居中对齐
        for i in range(self.table_widget.rowCount()):
            item = self.table_widget.verticalHeaderItem(i)
            if item:
                item.setTextAlignment(Qt.AlignCenter)
        
        # 设置左上角为空白
        corner_button = self.table_widget.findChild(QWidget, "qt_table_vheader")
        if corner_button:
            corner_button.setStyleSheet("""
                background-color: #f5f5f5;
                border: 1px solid #d9d9d9;
            """)
        
        # 应用自定义样式表
        self.table_widget.setStyleSheet(self.table_widget.styleSheet() + """
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
        """)
        
        # 禁用表格的焦点矩形
        self.table_widget.setAttribute(Qt.WA_MacShowFocusRect, False)
    
    def on_search_text_changed(self, text):
        """当搜索文本变化时，延迟执行搜索以提高性能"""
        # 取消之前的定时器
        self.search_timer.stop()
        # 启动新的定时器，300毫秒后执行搜索
        self.search_timer.start(300)
    
    def perform_search(self):
        """执行实际的搜索操作"""
        # 重置到第一页
        self.current_page = 1
        # 执行搜索
        self.filter_and_display_entries()
    
    def update_table_headers(self):
        """根据当前选择的类型更新表格列标题"""
        if self.current_type == "普通词" or self.current_type == "复合词":
            self.table_widget.setHorizontalHeaderLabels(["词条", "读音", "类型"])
        elif self.current_type == "前缀组合":
            self.table_widget.setHorizontalHeaderLabels(["词条", "前缀", "类型"])
        elif self.current_type == "后缀组合":
            self.table_widget.setHorizontalHeaderLabels(["词条", "后缀", "类型"])
        else:  # "全部"
            self.table_widget.setHorizontalHeaderLabels(["词条", "内容", "类型"])
    
    def on_type_filter_clicked(self, type_name):
        """处理类型过滤按钮点击"""
        self.current_type = type_name
        self.current_page = 1  # 重置到第一页
        
        # 更新表格列标题
        self.update_table_headers()
        
        self.filter_and_display_entries()
    
    def go_to_prev_page(self):
        """转到上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()
            self.update_page_controls()
            
            # 滚动到表格顶部
            self.table_widget.verticalScrollBar().setValue(0)
            
            # 重新计算滚动区域，确保所有行可见
            QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
            
            # 再次检查最后一行是否可见，增加延迟以确保渲染完成
            QTimer.singleShot(500, self.scroll_to_bottom_check)
    
    def go_to_next_page(self):
        """转到下一页"""
        total_pages = self.calculate_total_pages()
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_current_page()
            self.update_page_controls()
            
            # 滚动到表格顶部
            self.table_widget.verticalScrollBar().setValue(0)
            
            # 重新计算滚动区域，确保所有行可见
            QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
            
            # 再次检查最后一行是否可见，增加延迟以确保渲染完成
            QTimer.singleShot(500, self.scroll_to_bottom_check)
    
    def go_to_first_page(self):
        """转到第一页"""
        if self.current_page > 1:
            self.current_page = 1
            self.display_current_page()
            self.update_page_controls()
            
            # 滚动到表格顶部
            self.table_widget.verticalScrollBar().setValue(0)
            
            # 重新计算滚动区域，确保所有行可见
            QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
            
            # 再次检查最后一行是否可见，增加延迟以确保渲染完成
            QTimer.singleShot(500, self.scroll_to_bottom_check)
    
    def go_to_last_page(self):
        """转到最后一页"""
        total_pages = self.calculate_total_pages()
        if self.current_page < total_pages:
            self.current_page = total_pages
            self.display_current_page()
            self.update_page_controls()
            
            # 滚动到表格顶部
            self.table_widget.verticalScrollBar().setValue(0)
            
            # 重新计算滚动区域，确保所有行可见
            QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
            
            # 再次检查最后一行是否可见，增加延迟以确保渲染完成
            QTimer.singleShot(500, self.scroll_to_bottom_check)
    
    def on_page_size_changed(self, text):
        """处理每页显示条数变化"""
        try:
            new_size = int(text)
            if new_size != self.entries_per_page:
                self.entries_per_page = new_size
                self.current_page = 1  # 重置到第一页
                self.filter_and_display_entries()
                
                # 滚动到表格顶部
                self.table_widget.verticalScrollBar().setValue(0)
                
                # 重新计算滚动区域，确保所有行可见
                QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
                
                # 再次检查最后一行是否可见，增加延迟以确保渲染完成
                QTimer.singleShot(500, self.scroll_to_bottom_check)
                
                # 保存设置到配置文件
                config = self.parent.load_config() or {}  # 确保config不为None
                config["entries_per_page"] = new_size
                self.parent.save_config(config)
        except ValueError:
            pass  # 忽略无效输入
    
    def calculate_total_pages(self):
        """计算总页数"""
        total_entries = len(self.filtered_entries)
        return max(1, (total_entries + self.entries_per_page - 1) // self.entries_per_page)
    
    def update_page_controls(self):
        """更新分页控件状态"""
        total_pages = self.calculate_total_pages()
        self.page_info_label.setText(f"第 {self.current_page} 页 / 共 {total_pages} 页")
        
        # 更新每页显示条数下拉框
        current_size = str(self.entries_per_page)
        if self.page_size_combo.currentText() != current_size:
            index = self.page_size_combo.findText(current_size)
            if index >= 0:
                self.page_size_combo.setCurrentIndex(index)
        
        # 启用/禁用首页/上一页按钮
        is_first_page = self.current_page <= 1
        self.first_page_btn.setEnabled(not is_first_page)
        self.prev_page_btn.setEnabled(not is_first_page)
        
        # 启用/禁用下一页/尾页按钮
        is_last_page = self.current_page >= total_pages
        self.next_page_btn.setEnabled(not is_last_page)
        self.last_page_btn.setEnabled(not is_last_page)
    
    def filter_and_display_entries(self):
        """根据搜索文本和选择的类型过滤词条并显示"""
        search_text = self.search_edit.text().strip().lower()
        search_keywords = [keyword.strip() for keyword in search_text.split() if keyword.strip()]
        
        # 过滤符合条件的词条
        self.filtered_entries = []
        
        for entry in self.all_entries:
            # 类型过滤
            if self.current_type != "全部" and entry['type'] != self.current_type:
                continue
            
            # 关键词搜索
            if search_keywords:
                word = entry['word'].lower()
                readings = entry['readings'].lower()
                
                # 检查每个关键词是否匹配
                all_keywords_match = True
                for keyword in search_keywords:
                    if keyword not in word and keyword not in readings:
                        all_keywords_match = False
                        break
                
                if not all_keywords_match:
                    continue
            
            # 词条符合所有条件，添加到过滤结果中
            self.filtered_entries.append(entry)
        
        # 显示当前页
        self.display_current_page()
        
        # 更新匹配计数和分页控件
        self.match_count_label.setText(f"{len(self.filtered_entries)} 个匹配")
        self.update_page_controls()
        
        # 滚动到表格顶部
        self.table_widget.verticalScrollBar().setValue(0)
        
        # 重新计算滚动区域，确保所有行可见
        QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
        
        # 再次检查最后一行是否可见
        QTimer.singleShot(400, self.scroll_to_bottom_check)
    
    def display_current_page(self):
        """显示当前页的词条"""
        # 禁用表格更新，减少闪烁
        self.table_widget.setUpdatesEnabled(False)
        
        # 清空表格
        self.table_widget.setRowCount(0)
        
        # 计算当前页的起始和结束索引
        start_idx = (self.current_page - 1) * self.entries_per_page
        end_idx = min(start_idx + self.entries_per_page, len(self.filtered_entries))
        
        # 获取当前页的词条
        current_page_entries = self.filtered_entries[start_idx:end_idx]
        
        # 只设置实际数据的行数，不添加空行
        actual_rows = len(current_page_entries)
        
        # 确保设置足够的行数，即使是空行也需要
        self.table_widget.setRowCount(actual_rows)
        
        # 获取搜索关键词
        search_text = self.search_edit.text().strip().lower()
        search_keywords = [keyword.strip() for keyword in search_text.split() if keyword.strip()]
        
        # 预计算所有行的高度
        row_heights = []
        
        # 在表格中显示当前页的词条
        for i, entry in enumerate(current_page_entries):
            # 设置行号从1开始
            row_idx = start_idx + i + 1
            row_header = QTableWidgetItem(str(row_idx))
            row_header.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setVerticalHeaderItem(i, row_header)
            
            # 添加词条（使用富文本高亮匹配的关键词）
            word = entry['word']
            word_lower = word.lower()
            highlighted_word = word
            
            # 高亮搜索关键词
            if search_keywords:
                # 收集所有匹配位置
                matches = []
                for keyword in search_keywords:
                    pos = 0
                    while True:
                        pos = word_lower.find(keyword, pos)
                        if pos == -1:
                            break
                        matches.append((pos, pos + len(keyword)))
                        pos += 1
                
                # 合并重叠的匹配区域
                if matches:
                    matches.sort()
                    merged_matches = [matches[0]]
                    for curr_start, curr_end in matches[1:]:
                        prev_start, prev_end = merged_matches[-1]
                        if curr_start <= prev_end:
                            # 合并重叠区域
                            merged_matches[-1] = (prev_start, max(prev_end, curr_end))
                        else:
                            merged_matches.append((curr_start, curr_end))
                    
                    # 构建高亮文本
                    result = ""
                    last_end = 0
                    for start, end in merged_matches:
                        result += word[last_end:start]  # 添加非高亮部分
                        result += f'<span style="background-color: #FFFF00;">{word[start:end]}</span>'  # 添加高亮部分
                        last_end = end
                    result += word[last_end:]  # 添加最后一部分
                    highlighted_word = result
            
            word_item = QTableWidgetItem()
            word_item.setData(Qt.UserRole, word)  # 存储原始数据
            
            if any(keyword in word_lower for keyword in search_keywords):
                # 先添加项目到表格
                word_item.setData(Qt.DisplayRole, "")  # 清除普通文本
                word_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, 0, word_item)
                
                # 然后设置富文本标签
                rich_label = self.create_rich_text_label(highlighted_word)
                self.table_widget.setCellWidget(i, 0, rich_label)
            else:
                # 使用普通文本 - 设置成富文本标签以确保换行正常工作
                rich_label = self.create_rich_text_label(word)
                word_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, 0, word_item)
                self.table_widget.setCellWidget(i, 0, rich_label)
            
            # 添加读音/前缀/后缀（使用富文本高亮匹配的关键词）
            readings = entry['readings']
            readings_lower = readings.lower()
            highlighted_readings = readings
            
            # 高亮搜索关键词
            if search_keywords:
                # 收集所有匹配位置
                matches = []
                for keyword in search_keywords:
                    pos = 0
                    while True:
                        pos = readings_lower.find(keyword, pos)
                        if pos == -1:
                            break
                        matches.append((pos, pos + len(keyword)))
                        pos += 1
                
                # 合并重叠的匹配区域
                if matches:
                    matches.sort()
                    merged_matches = [matches[0]]
                    for curr_start, curr_end in matches[1:]:
                        prev_start, prev_end = merged_matches[-1]
                        if curr_start <= prev_end:
                            # 合并重叠区域
                            merged_matches[-1] = (prev_start, max(prev_end, curr_end))
                        else:
                            merged_matches.append((curr_start, curr_end))
                    
                    # 构建高亮文本
                    result = ""
                    last_end = 0
                    for start, end in merged_matches:
                        result += readings[last_end:start]  # 添加非高亮部分
                        result += f'<span style="background-color: #FFFF00;">{readings[start:end]}</span>'  # 添加高亮部分
                        last_end = end
                    result += readings[last_end:]  # 添加最后一部分
                    highlighted_readings = result
            
            readings_item = QTableWidgetItem()
            readings_item.setData(Qt.UserRole, readings)  # 存储原始数据
            
            if any(keyword in readings_lower for keyword in search_keywords):
                # 先添加项目到表格
                readings_item.setData(Qt.DisplayRole, "")  # 清除普通文本
                readings_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, 1, readings_item)
                
                # 然后设置富文本标签
                rich_label = self.create_rich_text_label(highlighted_readings)
                self.table_widget.setCellWidget(i, 1, rich_label)
            else:
                # 使用普通文本 - 设置成富文本标签以确保换行正常工作
                rich_label = self.create_rich_text_label(readings)
                readings_item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i, 1, readings_item)
                self.table_widget.setCellWidget(i, 1, rich_label)
            
            # 添加类型
            type_item = QTableWidgetItem()
            type_item.setData(Qt.UserRole, entry['type'])  # 存储原始数据
            type_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(i, 2, type_item)
            
            # 使用富文本标签以确保类型列也能正常换行
            type_label = self.create_rich_text_label(entry['type'])
            self.table_widget.setCellWidget(i, 2, type_label)
            
            # 预计算行高 - 使用QTextDocument计算
            col_heights = []
            for col in range(3):
                cell_widget = self.table_widget.cellWidget(i, col)
                if isinstance(cell_widget, CenteredLabel):
                    # 获取标签高度
                    col_heights.append(cell_widget.minimumHeight())
            
            # 取所有列中最大的高度作为行高
            if col_heights:
                row_heights.append(max(col_heights))
            else:
                row_heights.append(42)  # 默认行高
        
        # 一次性设置所有行高，减少重绘次数
        for i, height in enumerate(row_heights):
            self.table_widget.setRowHeight(i, height)
        
        # 设置表格外观
        self.setup_table_appearance()
        
        # 重新启用表格更新
        self.table_widget.setUpdatesEnabled(True)
        
        # 只检查滚动条，不强制调整所有行高
        QTimer.singleShot(100, self.scroll_to_bottom_check)
        
    def ensure_all_rows_visible(self, rows_count):
        """确保所有行都可见，包括最后一行，但不添加多余的底部空间"""
        if rows_count == 0:
            return
            
        # 计算需要的表格高度
        header_height = self.table_widget.horizontalHeader().height()
        
        # 直接计算所有行的总高度，不再重新调整行高
        total_row_height = sum(self.table_widget.rowHeight(i) for i in range(min(rows_count, self.table_widget.rowCount())))
        
        # 添加最小的额外空间，只确保最后一行完全可见
        padding = 5  # 减小到极小的值
        
        # 计算表格内容区域的总高度
        content_height = header_height + total_row_height + padding
        
        # 调整表格垂直滚动条的范围
        vsb = self.table_widget.verticalScrollBar()
        if vsb:
            # 计算值，确保能够滚动到最后一行并显示完整
            # 获取最后一行的高度，添加到计算中
            last_row_height = 0
            if rows_count > 0 and rows_count <= self.table_widget.rowCount():
                last_row_height = self.table_widget.rowHeight(rows_count - 1)
            else:
                last_row_height = 38  # 默认高度
                
            # 增加额外空间以确保最后一行一定可见
            extra_buffer = 15  # 额外的缓冲区，以确保绝对可见
            max_value = content_height - self.table_widget.viewport().height() + last_row_height + extra_buffer
            if max_value < 0:
                max_value = 0
                
            # 设置滚动范围，确保最后一行可完全显示
            vsb.setMaximum(max_value)
            
        # 通过定时器延迟执行滚动到底部的操作，确保正确设置滚动范围
        # 减少延迟时间，加快响应速度
        QTimer.singleShot(100, self.scroll_to_bottom_check)
    
    def scroll_to_bottom_check(self):
        """确保可以滚动到底部，确保最后一行完全可见，但不留太多空白"""
        rows = self.table_widget.rowCount()
        if rows <= 0:
            return
            
        # 获取最后一行
        last_row_index = rows - 1
        last_item = self.table_widget.item(last_row_index, 0)
        if not last_item:
            return
            
        # 获取滚动条
        vsb = self.table_widget.verticalScrollBar()
        if not vsb:
            return
            
        # 记住当前滚动位置
        current_pos = vsb.value()
        
        # 计算所有行的总高度（使用已经设置好的行高）
        total_height = sum(self.table_widget.rowHeight(i) for i in range(rows))
        
        # 计算滚动条最大值，确保最后一行完全可见
        viewport_height = self.table_widget.viewport().height()
        header_height = self.table_widget.horizontalHeader().height()
        last_row_height = self.table_widget.rowHeight(last_row_index)
        
        # 增加额外空间确保最后一行完全可见
        extra_buffer = last_row_height + 5  # 使用最后一行高度加上额外空间
        max_value = total_height + header_height - viewport_height + extra_buffer
        if max_value < 0:
            max_value = 0
            
        # 设置滚动条最大值
        vsb.setMaximum(max_value)
        
        # 测试是否可以滚动到底部查看最后一行
        temp_pos = vsb.value()
        vsb.setValue(vsb.maximum())
        
        # 检查最后一行是否可见
        last_row_rect = self.table_widget.visualItemRect(last_item)
        viewport_rect = self.table_widget.viewport().rect()
        
        # 如果最后一行不完全可见，增加更多空间
        if not viewport_rect.contains(last_row_rect.bottomRight()):
            # 计算需要额外增加的空间
            extra_space = last_row_rect.bottom() - viewport_rect.bottom() + 5
            vsb.setMaximum(vsb.maximum() + extra_space)
        
        # 恢复原始滚动位置
        vsb.setValue(current_pos)
    
    def setup_table_appearance(self):
        """设置表格外观"""
        # 设置表格左上角按钮样式
        corner_button = self.table_widget.findChild(QWidget, "qt_table_vheader")
        if corner_button:
            corner_button.setStyleSheet("""
                background-color: #f5f5f5;
                border: 1px solid #d9d9d9;
            """)
        
        # 确保所有行号都居中对齐
        for i in range(self.table_widget.rowCount()):
            if not self.table_widget.verticalHeaderItem(i):
                row_header = QTableWidgetItem(str(i + 1))
                row_header.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setVerticalHeaderItem(i, row_header)
    
    # 这些方法已重新实现为更高效的版本
    
    def on_section_resized(self, index, old_size, new_size):
        """处理列宽变化，确保每列都有合理的宽度"""
        # 标记为用户正在调整列宽
        self.is_user_resizing = True
        
        # 设置最小列宽和最大列宽比例
        min_width = 150
        max_width_ratio = 0.6  # 最大不超过总宽度的60%
        
        # 获取表格总宽度和当前所有列宽
        total_width = self.table_widget.viewport().width()
        column_widths = [self.table_widget.columnWidth(i) for i in range(3)]
        
        # 计算最大允许宽度，确保其他列至少有最小宽度
        max_allowed_width = total_width - min_width * (len(column_widths) - 1)
        max_width = min(max_allowed_width, int(total_width * max_width_ratio))
        
        # 确保最大宽度不小于最小宽度
        max_width = max(max_width, min_width)
        
        # 确保列宽不小于最小宽度且不超过最大宽度
        if new_size < min_width:
            self.table_widget.setColumnWidth(index, min_width)
        elif new_size > max_width:
            self.table_widget.setColumnWidth(index, max_width)
        
        # 计算调整后的总宽度
        adjusted_widths = column_widths.copy()
        adjusted_widths[index] = self.table_widget.columnWidth(index)
        
        # 确保其他列也至少有最小宽度
        remaining_width = total_width - adjusted_widths[index]
        other_columns = [i for i in range(3) if i != index]
        
        # 如果剩余宽度不足以给其他列最小宽度，则调整当前列
        if remaining_width < min_width * len(other_columns):
            # 重新计算当前列的最大宽度
            max_current_width = total_width - min_width * len(other_columns)
            if max_current_width >= min_width:
                self.table_widget.setColumnWidth(index, max_current_width)
            else:
                # 极端情况，所有列设为最小宽度
                for i in range(3):
                    self.table_widget.setColumnWidth(i, min_width)
        
        # 确保所有其他列都至少有最小宽度
        for col in other_columns:
            if self.table_widget.columnWidth(col) < min_width:
                self.table_widget.setColumnWidth(col, min_width)
        
        # 延迟重置标志位，允许用户调整完成
        QTimer.singleShot(500, self.reset_resizing_flag)
    
    def enforce_column_constraints(self, total_width, min_width):
        """强制执行列宽约束，确保所有列都有合理的宽度"""
        # 检查是否是用户手动调整列宽
        if hasattr(self, 'is_user_resizing') and self.is_user_resizing:
            return
            
        # 如果表格还没有完全初始化，延迟执行
        if not self.table_widget.isVisible() or total_width <= 0:
            QTimer.singleShot(100, lambda: self.enforce_column_constraints(
                self.table_widget.viewport().width(), min_width))
            return
            
        # 获取当前所有列的宽度
        col0_width = self.table_widget.columnWidth(0)
        col1_width = self.table_widget.columnWidth(1)
        col2_width = self.table_widget.columnWidth(2)
        
        # 计算可用宽度（减去垂直滚动条宽度和行头宽度）
        scrollbar_width = 15  # 估计滚动条宽度
        header_width = self.table_widget.verticalHeader().width()
        
        if self.table_widget.verticalScrollBar().isVisible():
            available_width = max(0, total_width - scrollbar_width)
        else:
            available_width = total_width
            
        # 确保可用宽度至少能容纳三列最小宽度
        min_total_width = min_width * 3
        if available_width < min_total_width:
            available_width = min_total_width
        
        # 计算最大列宽（不超过可用宽度的60%，且确保其他列至少有最小宽度）
        max_width = min(int(available_width * 0.6), available_width - min_width * 2)
        
        # 确保最大宽度不小于最小宽度
        max_width = max(max_width, min_width)
        
        # 计算列宽比例
        col0_ratio = 0.45  # 词条列占45%
        col1_ratio = 0.45  # 读音列占45%
        col2_ratio = 0.10  # 类型列占10%
        
        # 计算理想列宽，同时确保不超过最大宽度
        ideal_col0_width = min(max_width, max(min_width, int(available_width * col0_ratio)))
        ideal_col1_width = min(max_width, max(min_width, int(available_width * col1_ratio)))
        ideal_col2_width = min(max_width, max(min_width, int(available_width * col2_ratio)))
        
        # 调整总宽度以匹配可用宽度
        total_ideal_width = ideal_col0_width + ideal_col1_width + ideal_col2_width
        if total_ideal_width > available_width:
            # 按比例缩小
            ratio = available_width / total_ideal_width
            ideal_col0_width = max(min_width, int(ideal_col0_width * ratio))
            ideal_col1_width = max(min_width, int(ideal_col1_width * ratio))
            ideal_col2_width = max(min_width, int(ideal_col2_width * ratio))
            
            # 再次检查总宽度
            total_ideal_width = ideal_col0_width + ideal_col1_width + ideal_col2_width
            if total_ideal_width > available_width:
                # 如果仍然超过，从最大的列中减少
                excess = total_ideal_width - available_width
                if ideal_col0_width >= ideal_col1_width and ideal_col0_width > min_width:
                    ideal_col0_width = max(min_width, ideal_col0_width - excess)
                elif ideal_col1_width > min_width:
                    ideal_col1_width = max(min_width, ideal_col1_width - excess)
                elif ideal_col2_width > min_width:
                    ideal_col2_width = max(min_width, ideal_col2_width - excess)
        
        # 确保所有列宽都不超过最大宽度且总和不超过可用宽度
        ideal_col0_width = min(max_width, ideal_col0_width)
        ideal_col1_width = min(max_width, ideal_col1_width)
        ideal_col2_width = min(max_width, ideal_col2_width)
        
        # 最后检查：确保总宽度不超过可用宽度
        total_width_check = ideal_col0_width + ideal_col1_width + ideal_col2_width
        if total_width_check > available_width:
            # 如果超过，按比例缩小所有列
            ratio = available_width / total_width_check
            ideal_col0_width = max(min_width, int(ideal_col0_width * ratio))
            ideal_col1_width = max(min_width, int(ideal_col1_width * ratio))
            ideal_col2_width = max(min_width, int(ideal_col2_width * ratio))
        
        # 应用新的列宽
        self.table_widget.setColumnWidth(0, ideal_col0_width)
        self.table_widget.setColumnWidth(1, ideal_col1_width)
        self.table_widget.setColumnWidth(2, ideal_col2_width)
        
        # 调整垂直表头宽度
        self.table_widget.verticalHeader().setFixedWidth(50)
    
    def reset_resizing_flag(self):
        """重置用户调整标志位"""
        self.is_user_resizing = False
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        
        # 调整表格尺寸以适应窗口大小
        margins_h = 48  # 水平边距
        margins_v = 240  # 垂直边距（其他控件总高度）
        
        # 计算可用空间
        table_width = self.width() - margins_h
        table_height = self.height() - margins_v
        
        # 确保最小高度
        if table_height < 450:
            table_height = 450
        
        # 设置表格尺寸
        self.table_widget.setFixedWidth(table_width)
        self.table_widget.setFixedHeight(table_height)
        
        # 重新设置列宽比例
        self.adjust_columns_to_fit()
        
        # 重新计算滚动区域，确保所有行可见
        self.ensure_all_rows_visible(self.table_widget.rowCount())
    
    def adjust_columns_to_fit(self):
        """调整列宽以适应表格宽度"""
        # 获取表格可用宽度
        available_width = self.table_widget.width() - self.table_widget.verticalHeader().width()
        if self.table_widget.verticalScrollBar().isVisible():
            available_width -= self.table_widget.verticalScrollBar().width()
        
        # 应用列宽比例
        col0_width = int(available_width * self.column_ratios[0])
        col1_width = int(available_width * self.column_ratios[1])
        col2_width = available_width - col0_width - col1_width  # 确保总宽度正好等于可用宽度
        
        # 设置列宽
        self.table_widget.setColumnWidth(0, col0_width)
        self.table_widget.setColumnWidth(1, col1_width)
        self.table_widget.setColumnWidth(2, col2_width)
            
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        
        # 调整表格尺寸以适应窗口大小
        margins_h = 48  # 水平边距
        margins_v = 240  # 垂直边距（其他控件总高度）
        
        # 计算可用空间
        table_width = self.width() - margins_h
        table_height = self.height() - margins_v
        
        # 确保最小高度
        if table_height < 450:
            table_height = 450
            
        # 设置表格尺寸
        self.table_widget.setFixedWidth(table_width)
        self.table_widget.setFixedHeight(table_height)
        
        # 加载词典数据
        self.load_dict_data()
        
        # 窗口显示时，初始化列宽
        # 使用多个延时，确保在不同时机都能正确设置列宽
        QTimer.singleShot(50, self.adjust_columns_to_fit)
        QTimer.singleShot(200, self.adjust_columns_to_fit)
        QTimer.singleShot(500, self.adjust_columns_to_fit)
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 获取右键点击的单元格位置
        item = self.table_widget.itemAt(position)
        if item:
            row = self.table_widget.row(item)
            column = self.table_widget.column(item)
            
            # 添加编辑选项
            edit_action = menu.addAction("编辑")
            edit_action.triggered.connect(lambda: self.on_cell_double_clicked(row, column))
            
            # 添加复制选项
            menu.addSeparator()
            copy_action = menu.addAction("复制")
            copy_action.triggered.connect(self.copy_selection)
        else:
            # 如果没有选中单元格，只显示复制选项
            copy_action = menu.addAction("复制")
            copy_action.triggered.connect(self.copy_selection)
        
        menu.exec_(self.table_widget.viewport().mapToGlobal(position))
    
    def copy_selection(self):
        """复制选中的单元格内容到剪贴板"""
        selected = self.table_widget.selectedItems()
        if not selected:
            return
            
        # 获取所有选中单元格的行列位置
        rows = set()
        cols = set()
        for item in selected:
            rows.add(self.table_widget.row(item))
            cols.add(self.table_widget.column(item))
        
        # 按行列顺序排序
        rows = sorted(list(rows))
        cols = sorted(list(cols))
        
        # 构建文本表格
        texts = []
        for row in rows:
            row_texts = []
            for col in cols:
                # 检查是否有单元格控件（富文本标签）
                cell_widget = self.table_widget.cellWidget(row, col)
                if cell_widget and isinstance(cell_widget, QLabel):
                    # 从QLabel获取纯文本（去除HTML标签）
                    if isinstance(cell_widget, CenteredLabel):
                        # 使用get_plain_text方法获取纯文本内容
                        text = cell_widget.get_plain_text()
                    else:
                        text = cell_widget.text()
                        # 移除HTML标签
                        text = text.replace(r'<span style="background-color: #FFFF00;">', '')
                        text = text.replace('</span>', '')
                        text = text.replace('<div align="center" style="text-align:center; width:100%;">', '')
                        text = text.replace('</div>', '')
                    row_texts.append(text)
                else:
                    # 常规单元格项处理
                    item = self.table_widget.item(row, col)
                    if item and item in selected:
                        # 尝试从UserRole获取原始数据
                        data = item.data(Qt.UserRole)
                        if data:
                            row_texts.append(data)
                        else:
                            row_texts.append(item.text())
                    else:
                        row_texts.append("")
            texts.append("\t".join(row_texts))
        
        # 复制到剪贴板
        QApplication.clipboard().setText("\n".join(texts))
    
    def load_dict_data(self):
        """加载词典数据"""
        # 获取词典数据
        custom_dict = self.parent.custom_dict
        
        # 清空数据
        self.all_entries = []
        
        # 加载普通词
        for word, readings in custom_dict.get("normal_words", {}).items():
            readings_text = ", ".join(readings) if isinstance(readings, list) else str(readings)
            self.all_entries.append({
                'word': word,
                'readings': readings_text,
                'type': "普通词"
            })
        
        # 加载复合词
        for word, readings in custom_dict.get("compound_words", {}).items():
            readings_text = ", ".join(readings) if isinstance(readings, list) else str(readings)
            self.all_entries.append({
                'word': word,
                'readings': readings_text,
                'type': "复合词"
            })
        
        # 加载后缀组合
        for word, particles in custom_dict.get("common_combinations", {}).items():
            particles_text = ", ".join(particles) if isinstance(particles, list) else str(particles)
            self.all_entries.append({
                'word': word,
                'readings': particles_text,
                'type': "后缀组合"
            })
        
        # 加载前缀组合
        for word, targets in custom_dict.get("prefix_combinations", {}).items():
            targets_text = ", ".join(targets) if isinstance(targets, list) else str(targets)
            self.all_entries.append({
                'word': word,
                'readings': targets_text,
                'type': "前缀组合"
            })
        
        # 按词条排序
        self.all_entries.sort(key=lambda x: x['word'])
        
        # 应用当前过滤器和搜索
        self.filter_and_display_entries()
    
    def center_on_parent(self, parent):
        """在父窗口中心显示"""
        if parent:
            self.move(parent.frameGeometry().center() - self.rect().center())
    
    def showEvent(self, event):
        """窗口显示时的处理"""
        super().showEvent(event)
        
        # 加载词典数据
        self.load_dict_data()
        
        # 禁用表格项的焦点框
        self.remove_focus_rect()
        
        # 居中显示
        self.center_on_parent(self.parent)
        
        # 调整列宽以适应内容
        self.adjust_columns_to_fit()

    def create_rich_text_label(self, html_content):
        """创建富文本标签用于显示高亮文本"""
        return CenteredLabel(html_content, self)

    def on_cell_double_clicked(self, row, column):
        """处理单元格双击事件"""
        # 获取当前页的起始索引
        start_idx = (self.current_page - 1) * self.entries_per_page
        
        # 确保索引有效
        if 0 <= row < len(self.filtered_entries) and start_idx + row < len(self.filtered_entries):
            # 获取双击的词条
            entry = self.filtered_entries[start_idx + row]
            entry_type = entry['type']
            word = entry['word']  # 获取词条文本
            
            # 类型映射
            type_mapping = {
                "普通词": "normal_words",
                "复合词": "compound_words",
                "前缀组合": "prefix_combinations",
                "后缀组合": "common_combinations"
            }
            
            # 如果类型有效，打开对应的编辑窗口
            if entry_type in type_mapping:
                word_type = type_mapping[entry_type]
                self.parent.open_edit_dict_window(word_type, word)  # 传递词条文本

class WordWrapDelegate(QStyledItemDelegate):
    """自定义表格项代理，处理文本换行"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.height_cache = {}  # 缓存行高计算结果
        
    def paint(self, painter, option, index):
        """重写绘制方法，支持文本换行"""
        # 检查单元格是否有部件
        if index.model().data(index, Qt.DisplayRole):
            # 对于没有自定义部件的单元格，处理文本换行
            text = index.data(Qt.DisplayRole)
            
            # 绘制背景和选择效果
            self.initStyleOption(option, index)
            style = option.widget.style() if option.widget else QApplication.style()
            style.drawControl(QStyle.CE_ItemViewItem, option, painter, option.widget)
            
            # 创建文本文档来绘制文本
            doc = QTextDocument()
            doc.setHtml(text)  # 支持HTML格式
            doc.setTextWidth(option.rect.width() - 12)  # 减去边距
            
            # 设置文本选项
            text_option = QTextOption()
            text_option.setWrapMode(QTextOption.WordWrap)
            text_option.setAlignment(Qt.AlignCenter)
            doc.setDefaultTextOption(text_option)
            
            # 绘制文本
            painter.save()
            painter.translate(option.rect.left() + 6, option.rect.top() + 6)  # 添加边距
            clip_rect = QRectF(0, 0, option.rect.width() - 12, option.rect.height() - 12)
            painter.setClipRect(clip_rect)
            
            # 设置文本颜色
            if option.state & QStyle.State_Selected:
                painter.setPen(option.palette.color(QPalette.HighlightedText))
            else:
                painter.setPen(option.palette.color(QPalette.Text))
                
            doc.drawContents(painter)
            painter.restore()
        else:
            # 对于有自定义部件的单元格，使用默认绘制
            super().paint(painter, option, index)
    
    def sizeHint(self, option, index):
        """重写尺寸提示方法，计算换行文本需要的高度"""
        text = index.data(Qt.DisplayRole)
        if not text:
            return super().sizeHint(option, index)
        
        # 默认行高
        default_height = 42
        
        # 计算文本宽度
        width = option.rect.width()
        if width <= 0:
            width = 200  # 默认宽度
        
        # 使用缓存避免重复计算
        cache_key = f"{text}:{width}"
        if cache_key in self.height_cache:
            return QSize(width, self.height_cache[cache_key])
            
        # 使用QTextDocument计算高度
        doc = QTextDocument()
        doc.setHtml(text)  # 支持HTML格式
        doc.setTextWidth(width - 12)  # 减去边距
        
        # 设置文本选项
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WordWrap)
        text_option.setAlignment(Qt.AlignCenter)
        doc.setDefaultTextOption(text_option)
        
        # 计算文档高度
        text_height = doc.size().height() + 12  # 添加边距
        
        # 确保最小高度
        result_height = max(default_height, int(text_height))
        
        # 缓存结果
        self.height_cache[cache_key] = result_height
        
        return QSize(width, result_height)

    def createEditor(self, parent, option, index):
        """禁止编辑，确保只读状态"""
        return None

class CenteredLabel(QLabel):
    """自定义标签类，确保文本始终居中显示"""
    def __init__(self, html_content="", parent=None):
        super().__init__(parent)
        
        # 保存原始内容
        self.original_content = html_content
        self.height_cache = {}  # 缓存高度计算结果
        
        # 在HTML内容中直接添加居中样式
        centered_html = f'<div align="center" style="text-align:center; width:100%;">{html_content}</div>'
        
        self.setTextFormat(Qt.RichText)
        self.setAlignment(Qt.AlignCenter)
        self.setText(centered_html)
        self.setStyleSheet("""
            background: transparent;
            padding: 4px;
            border: none;
            margin: 0;
            font-size: 13px;
            color: #333333;
            text-align: center;
            qproperty-alignment: AlignCenter;
        """)
        
        # 设置适当的策略
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # 启用文本换行
        self.setWordWrap(True)
        
        # 使用QTextDocument计算高度
        self.calculateOptimalHeight()
    
    def get_plain_text(self):
        """获取不包含HTML标签的纯文本内容"""
        # 使用正则表达式去除所有HTML标签
        return re.sub(r'<[^>]*>', '', self.original_content)
    
    def calculateOptimalHeight(self):
        """使用QTextDocument计算最佳高度"""
        # 获取当前宽度
        width = self.width() - 12  # 减去padding
        if width <= 0:
            width = 200  # 默认宽度
            
        # 检查缓存
        cache_key = f"{self.original_content}:{width}"
        if cache_key in self.height_cache:
            self.setMinimumHeight(self.height_cache[cache_key])
            return
            
        # 使用QTextDocument计算高度
        doc = QTextDocument()
        doc.setHtml(self.original_content)
        doc.setTextWidth(width)
        
        # 设置文本选项
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WordWrap)
        text_option.setAlignment(Qt.AlignCenter)
        doc.setDefaultTextOption(text_option)
        
        # 计算高度并添加边距
        height = int(doc.size().height()) + 10
        
        # 设置最小高度
        optimal_height = max(30, height)
        self.setMinimumHeight(optimal_height)
        
        # 缓存结果
        self.height_cache[cache_key] = optimal_height
    
    def resizeEvent(self, event):
        """重写大小变化事件，确保调整大小后文本仍然居中"""
        super().resizeEvent(event)
        # 重新计算高度
        self.calculateOptimalHeight()
        # 重新设置对齐方式
        self.setAlignment(Qt.AlignCenter)

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