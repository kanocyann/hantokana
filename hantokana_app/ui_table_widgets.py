from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtGui import QTextOption, QTextDocument, QPalette
from PySide6.QtWidgets import QApplication, QLabel, QSizePolicy, QStyle, QStyledItemDelegate


class WordWrapDelegate(QStyledItemDelegate):
    """自定义表格项代理，处理文本换行"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.height_cache = {}

    def paint(self, painter, option, index):
        if index.model().data(index, Qt.DisplayRole):
            text = index.data(Qt.DisplayRole)
            self.initStyleOption(option, index)
            style = option.widget.style() if option.widget else QApplication.style()
            style.drawControl(QStyle.CE_ItemViewItem, option, painter, option.widget)

            doc = QTextDocument()
            doc.setHtml(text)
            doc.setTextWidth(option.rect.width() - 12)

            text_option = QTextOption()
            text_option.setWrapMode(QTextOption.WordWrap)
            text_option.setAlignment(Qt.AlignCenter)
            doc.setDefaultTextOption(text_option)

            painter.save()
            painter.translate(option.rect.left() + 6, option.rect.top() + 6)
            clip_rect = QRectF(0, 0, option.rect.width() - 12, option.rect.height() - 12)
            painter.setClipRect(clip_rect)

            if option.state & QStyle.State_Selected:
                painter.setPen(option.palette.color(QPalette.HighlightedText))
            else:
                painter.setPen(option.palette.color(QPalette.Text))

            doc.drawContents(painter)
            painter.restore()
        else:
            super().paint(painter, option, index)

    def sizeHint(self, option, index):
        text = index.data(Qt.DisplayRole)
        if not text:
            return super().sizeHint(option, index)

        default_height = 42
        width = option.rect.width()
        if width <= 0:
            width = 200

        cache_key = f"{text}:{width}"
        if cache_key in self.height_cache:
            return QSize(width, self.height_cache[cache_key])

        doc = QTextDocument()
        doc.setHtml(text)
        doc.setTextWidth(width - 12)

        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WordWrap)
        text_option.setAlignment(Qt.AlignCenter)
        doc.setDefaultTextOption(text_option)

        text_height = doc.size().height() + 12
        result_height = max(default_height, int(text_height))
        self.height_cache[cache_key] = result_height
        return QSize(width, result_height)

    def createEditor(self, parent, option, index):
        return None


class CenteredLabel(QLabel):
    """自定义标签类，确保文本始终居中显示"""

    def __init__(self, html_content="", parent=None):
        super().__init__(parent)
        self.original_content = html_content
        self.height_cache = {}

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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setWordWrap(True)
        self.calculateOptimalHeight()

    def calculateOptimalHeight(self):
        width = self.width() - 12
        if width <= 0:
            width = 200

        cache_key = f"{self.original_content}:{width}"
        if cache_key in self.height_cache:
            self.setMinimumHeight(self.height_cache[cache_key])
            return

        doc = QTextDocument()
        doc.setHtml(self.original_content)
        doc.setTextWidth(width)

        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WordWrap)
        text_option.setAlignment(Qt.AlignCenter)
        doc.setDefaultTextOption(text_option)

        height = int(doc.size().height()) + 10
        optimal_height = max(30, height)
        self.setMinimumHeight(optimal_height)
        self.height_cache[cache_key] = optimal_height

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.calculateOptimalHeight()
        self.setAlignment(Qt.AlignCenter)
