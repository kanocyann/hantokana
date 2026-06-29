from PySide6.QtCore import Qt, QRect, QSize, QMimeData
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QCheckBox, QTextEdit


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
        self.toggled.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        text_rect = rect.adjusted(32, 0, 0, 0)

        painter.setPen(QColor("#1f1f1f"))
        painter.setFont(self.font())
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.text())

        checkbox_x = 8
        checkbox_y = (rect.height() - 18) // 2
        checkbox_rect = QRect(checkbox_x, checkbox_y, 18, 18)

        if self.isChecked():
            painter.setBrush(QColor("#73BBA3"))
            painter.setPen(QColor("#73BBA3"))
        else:
            painter.setBrush(QColor("white"))
            painter.setPen(QColor("#d9d9d9"))

        painter.drawRoundedRect(checkbox_rect, 3, 3)

        if self.isChecked():
            painter.setPen(QPen(QColor("white"), 2))
            painter.drawLine(checkbox_x + 3, checkbox_y + 9, checkbox_x + 7, checkbox_y + 13)
            painter.drawLine(checkbox_x + 7, checkbox_y + 13, checkbox_x + 15, checkbox_y + 5)

    def sizeHint(self):
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(text_width + 40, 30)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
            self.update()


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
        self.toggled.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        text_rect = rect.adjusted(50, 0, 0, 0)

        painter.setPen(QColor("#1f1f1f"))
        painter.setFont(self.font())
        painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, self.text())

        switch_x = 8
        switch_y = (rect.height() - 20) // 2
        switch_rect = QRect(switch_x, switch_y, 36, 20)

        if self.isChecked():
            painter.setBrush(QColor("#73BBA3"))
            painter.setPen(QColor("#73BBA3"))
        else:
            painter.setBrush(QColor("#f5f5f5"))
            painter.setPen(QColor("#d9d9d9"))

        painter.drawRoundedRect(switch_rect, 10, 10)

        if self.isChecked():
            slider_x = switch_x + 18
        else:
            slider_x = switch_x + 2

        slider_rect = QRect(slider_x, switch_y + 2, 16, 16)
        painter.setBrush(QColor("white"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(slider_rect)

    def sizeHint(self):
        text_width = self.fontMetrics().horizontalAdvance(self.text())
        return QSize(text_width + 52, 24)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())
            self.update()
            self.toggled.emit(self.isChecked())


class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source: QMimeData):
        self.insertPlainText(source.text())
