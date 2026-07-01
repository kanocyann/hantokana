from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
)

from .dict_search_core import (
    calculate_total_pages as calculate_search_total_pages,
    entry_at_page_row,
    filter_entries,
    get_page_entries,
)
from .dict_table_core import (
    DEFAULT_COLUMN_RATIOS,
    DEFAULT_MIN_ROW_HEIGHT,
    DEFAULT_SCROLL_BOTTOM_PADDING,
    calculate_table_scroll_max,
    calculate_table_size,
    constrain_resized_column_widths,
    format_selected_cells_as_tsv,
    ratio_column_widths,
)
from .dict_dialog_styles import (
    FILTER_BUTTON_STYLE,
    MATCH_COUNT_LABEL_STYLE,
    PAGE_INFO_LABEL_STYLE,
    PAGE_SIZE_LABEL_STYLE,
    PAGINATION_BUTTON_STYLE,
    PANEL_FRAME_STYLE,
    SEARCH_LINE_EDIT_STYLE,
    TABLE_CORNER_STYLE,
    TABLE_FOCUS_STYLE,
    TABLE_WIDGET_STYLE,
    TRANSPARENT_WIDGET_STYLE,
    page_size_combo_style,
)
from .dict_view_core import (
    DISPLAY_NAME_TO_WORD_TYPE,
    DICT_SEARCH_TYPES,
    highlight_text,
    iter_custom_dict_entries,
    split_search_keywords,
)
from .storage_core import resource_path as storage_resource_path
from .ui_shared import (
    CenteredLabel,
    center_on_parent,
    WordWrapDelegate,
)


def _resolve_icon_path(parent, relative_path="icon.ico"):
    if parent and hasattr(parent, "resource_path"):
        try:
            return parent.resource_path(relative_path)
        except Exception:
            pass
    return storage_resource_path(relative_path, __file__)

class DictSearchDialog(QDialog):
    """词典搜索对话框"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("词典搜索")
        self.setWindowFlags(Qt.Window)
        self.setModal(False)  # 非模态对话框，可以与主窗口交互
        self.setMinimumSize(1100, 760)
        self.setStyleSheet("QDialog { background-color: #f4f6f8; }")
        
        # 初始化用户调整列宽的标志
        self.is_user_resizing = False
        self.is_applying_column_widths = False
        self.is_applying_row_heights = False
        self.row_resize_keep_bottom = False
        self.row_resize_timer = QTimer(self)
        self.row_resize_timer.setSingleShot(True)
        self.row_resize_timer.timeout.connect(self._finish_row_resize)
        
        # 初始化列宽比例
        self.column_ratios = DEFAULT_COLUMN_RATIOS
        
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
            self.setWindowIcon(QIcon(_resolve_icon_path(parent, "icon.ico")))
        except Exception:
            pass
        
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.addWidget(self._build_header_card())
        layout.addWidget(self._build_search_frame())

        self._create_pagination_controls()
        self._create_table_widget()
        table_card = QFrame()
        table_card.setProperty("card", "true")
        table_card.setAttribute(Qt.WA_StyledBackground, True)
        table_card_layout = QVBoxLayout(table_card)
        table_card_layout.setContentsMargins(14, 14, 14, 14)
        table_card_layout.setSpacing(10)
        table_card_layout.addLayout(self._build_table_controls_layout())
        layout.addWidget(table_card, 1)

        self.remove_focus_rect()
        self.update_page_controls()

    def _build_header_card(self):
        header = QFrame()
        header.setProperty("card", "true")
        header.setAttribute(Qt.WA_StyledBackground, True)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 14, 16, 14)
        header_layout.setSpacing(12)

        title_column = QVBoxLayout()
        title_column.setSpacing(4)
        title = QLabel("词典搜索")
        title.setProperty("title", "true")
        subtitle = QLabel("搜索、筛选和分页查看词条，双击可直接进入编辑。")
        subtitle.setProperty("muted", "true")
        subtitle.setWordWrap(True)
        title_column.addWidget(title)
        title_column.addWidget(subtitle)
        header_layout.addLayout(title_column, 1)

        self.search_scope_label = QLabel("全部")
        self.search_scope_label.setProperty("badge", "true")
        header_layout.addWidget(self.search_scope_label, 0, Qt.AlignRight | Qt.AlignVCenter)

        return header

    def _build_search_frame(self):
        search_frame = QFrame()
        search_frame.setFrameStyle(QFrame.StyledPanel)
        search_frame.setStyleSheet(PANEL_FRAME_STYLE)
        search_frame.setProperty("card", "true")
        search_frame.setAttribute(Qt.WA_StyledBackground, True)
        search_layout = QVBoxLayout(search_frame)
        search_layout.setSpacing(10)
        search_layout.setContentsMargins(14, 14, 14, 14)

        search_input_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入关键词搜索词典（用空格分隔多个关键词）...")
        self.search_edit.setStyleSheet(SEARCH_LINE_EDIT_STYLE)
        self.search_edit.textChanged.connect(self.on_search_text_changed)
        search_input_layout.addWidget(self.search_edit)

        self.match_count_label = QLabel("0 个匹配")
        self.match_count_label.setAlignment(Qt.AlignCenter)
        self.match_count_label.setStyleSheet(MATCH_COUNT_LABEL_STYLE)
        search_input_layout.addWidget(self.match_count_label)

        search_layout.addLayout(search_input_layout)
        search_layout.addLayout(self._build_type_filter_layout())

        return search_frame

    def _build_type_filter_layout(self):
        filter_layout = QHBoxLayout()
        self.type_buttons = {}
        types = list(DICT_SEARCH_TYPES)

        for type_name in types:
            btn = QPushButton(type_name)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setFixedHeight(32)
            btn.setStyleSheet(FILTER_BUTTON_STYLE)

            if type_name == "全部":
                btn.setChecked(True)

            btn.clicked.connect(lambda checked, t=type_name: self.on_type_filter_clicked(t))
            filter_layout.addWidget(btn)
            self.type_buttons[type_name] = btn

        return filter_layout

    def _create_pagination_controls(self):
        self.page_info_label = QLabel("第 1 页 / 共 1 页")
        self.page_info_label.setStyleSheet(PAGE_INFO_LABEL_STYLE)

        self.first_page_btn = self._create_page_button("首页", self.go_to_first_page)
        self.prev_page_btn = self._create_page_button("上一页", self.go_to_prev_page)
        self.next_page_btn = self._create_page_button("下一页", self.go_to_next_page)
        self.last_page_btn = self._create_page_button("末页", self.go_to_last_page)

        self.page_size_label = QLabel("每页显示：")
        self.page_size_label.setStyleSheet(PAGE_SIZE_LABEL_STYLE)

        config = self.parent.load_config() or {}
        self.entries_per_page = config.get("entries_per_page", 50)

        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["10", "20", "50", "100"])
        self.page_size_combo.setCurrentText(str(self.entries_per_page))
        self.page_size_combo.setFixedWidth(70)
        self.page_size_combo.setFixedHeight(26)
        self.page_size_combo.setEditable(False)
        self.page_size_combo.setFrame(True)
        self.page_size_combo.setMaxVisibleItems(4)
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)

        try:
            arrow_path = _resolve_icon_path(self.parent, "arrow.svg")
        except Exception:
            arrow_path = "arrow.svg"
        self.page_size_combo.setStyleSheet(page_size_combo_style(arrow_path))

    def _create_page_button(self, text, slot):
        button = QPushButton(text)
        button.setFixedWidth(60)
        button.setFixedHeight(26)
        button.clicked.connect(slot)
        button.setStyleSheet(PAGINATION_BUTTON_STYLE)
        return button

    def _create_table_widget(self):
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.update_table_headers()

        self.table_widget.horizontalHeader().setVisible(True)
        self.table_widget.setMinimumHeight(450)
        self.table_widget.setColumnWidth(0, 300)
        self.table_widget.setColumnWidth(1, 300)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.horizontalHeader().setMinimumSectionSize(100)
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_widget.verticalHeader().setFixedWidth(50)
        self.table_widget.verticalHeader().setMinimumSectionSize(DEFAULT_MIN_ROW_HEIGHT)
        self.table_widget.horizontalHeader().setMinimumSectionSize(150)
        self.table_widget.verticalHeader().setSectionsMovable(False)
        self.table_widget.verticalHeader().setSectionsClickable(False)
        self.table_widget.verticalHeader().sectionResized.connect(self.on_row_resized)

        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table_widget.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table_widget.verticalScrollBar().setSingleStep(10)
        self.table_widget.verticalScrollBar().setProperty("extraBottom", 5)
        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustIgnored)
        self.table_widget.horizontalHeader().sectionResized.connect(self.on_section_resized)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_context_menu)

        copy_shortcut = QShortcut(QKeySequence.Copy, self.table_widget)
        copy_shortcut.activated.connect(self.copy_selection)
        self.table_widget.cellDoubleClicked.connect(self.on_cell_double_clicked)

        word_wrap_delegate = WordWrapDelegate(self.table_widget)
        self.table_widget.setItemDelegate(word_wrap_delegate)
        self.table_widget.setStyleSheet(TABLE_WIDGET_STYLE + TABLE_FOCUS_STYLE)

    def _build_table_controls_layout(self):
        self.page_info_label.setMinimumHeight(26)
        self.page_info_label.setAlignment(Qt.AlignCenter)

        table_container = QVBoxLayout()
        table_container.setContentsMargins(0, 0, 0, 0)
        table_container.setSpacing(10)

        table_frame = QFrame()
        table_frame.setFrameStyle(QFrame.NoFrame)
        table_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_frame.setProperty("card", "true")
        table_frame.setAttribute(Qt.WA_StyledBackground, True)
        table_frame_layout = QVBoxLayout(table_frame)
        table_frame_layout.setContentsMargins(0, 0, 0, 0)
        table_frame_layout.setSpacing(0)
        table_frame_layout.addWidget(self.table_widget)
        table_container.addWidget(table_frame, 1)

        footer_row = QHBoxLayout()
        footer_row.setContentsMargins(0, 0, 0, 0)
        footer_row.setSpacing(8)
        footer_row.addWidget(self.page_info_label)
        footer_row.addStretch(1)
        footer_row.addWidget(self.page_size_label)
        footer_row.addWidget(self.page_size_combo)
        table_container.addLayout(footer_row)

        pagination_row = QHBoxLayout()
        pagination_row.setContentsMargins(0, 0, 0, 0)
        pagination_row.setSpacing(6)
        pagination_row.addStretch(1)
        pagination_row.addWidget(self.first_page_btn)
        pagination_row.addWidget(self.prev_page_btn)
        pagination_row.addWidget(self.next_page_btn)
        pagination_row.addWidget(self.last_page_btn)
        pagination_row.addStretch(1)
        table_container.addLayout(pagination_row)

        return table_container
    
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
            corner_button.setStyleSheet(TABLE_CORNER_STYLE)
        
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
        if hasattr(self, "search_scope_label"):
            self.search_scope_label.setText(type_name)
        
        # 更新表格列标题
        self.update_table_headers()
        
        self.filter_and_display_entries()
    
    def go_to_prev_page(self):
        """转到上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()
            self.update_page_controls()
            self._schedule_scroll_recheck(final_delay=500)
    
    def go_to_next_page(self):
        """转到下一页"""
        total_pages = self.calculate_total_pages()
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_current_page()
            self.update_page_controls()
            self._schedule_scroll_recheck(final_delay=500)
    
    def go_to_first_page(self):
        """转到第一页"""
        if self.current_page > 1:
            self.current_page = 1
            self.display_current_page()
            self.update_page_controls()
            self._schedule_scroll_recheck(final_delay=500)
    
    def go_to_last_page(self):
        """转到最后一页"""
        total_pages = self.calculate_total_pages()
        if self.current_page < total_pages:
            self.current_page = total_pages
            self.display_current_page()
            self.update_page_controls()
            self._schedule_scroll_recheck(final_delay=500)
    
    def on_page_size_changed(self, text):
        """处理每页显示条数变化"""
        try:
            new_size = int(text)
            if new_size != self.entries_per_page:
                self.entries_per_page = new_size
                self.current_page = 1  # 重置到第一页
                self.filter_and_display_entries()
                self._schedule_scroll_recheck(final_delay=500)
                
                # 保存设置到配置文件
                config = self.parent.load_config() or {}  # 确保config不为None
                config["entries_per_page"] = new_size
                self.parent.save_config(config)
        except ValueError:
            pass  # 忽略无效输入
    
    def calculate_total_pages(self):
        """计算总页数"""
        return calculate_search_total_pages(len(self.filtered_entries), self.entries_per_page)
    
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
        self.filtered_entries = filter_entries(
            self.all_entries,
            self.current_type,
            self.search_edit.text(),
        )
        
        # 显示当前页
        self.display_current_page()
        
        # 更新匹配计数和分页控件
        self.match_count_label.setText(f"{len(self.filtered_entries)} 个匹配")
        self.update_page_controls()
        
        self._schedule_scroll_recheck(final_delay=400)

    def _schedule_scroll_recheck(self, final_delay=400):
        self.table_widget.verticalScrollBar().setValue(0)
        QTimer.singleShot(0, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
        QTimer.singleShot(final_delay, self.scroll_to_bottom_check)
    
    def display_current_page(self):
        """显示当前页的词条"""
        # 禁用表格更新，减少闪烁
        self.table_widget.setUpdatesEnabled(False)
        
        # 清空表格
        self.table_widget.setRowCount(0)
        
        start_idx, current_page_entries = get_page_entries(
            self.filtered_entries,
            self.current_page,
            self.entries_per_page,
        )
        
        # 只设置实际数据的行数，不添加空行
        actual_rows = len(current_page_entries)
        
        # 确保设置足够的行数，即使是空行也需要
        self.table_widget.setRowCount(actual_rows)
        
        search_keywords = split_search_keywords(self.search_edit.text())
        
        # 预计算所有行的高度
        row_heights = []
        
        # 在表格中显示当前页的词条
        for i, entry in enumerate(current_page_entries):
            # 设置行号从1开始
            row_idx = start_idx + i + 1
            row_header = QTableWidgetItem(str(row_idx))
            row_header.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setVerticalHeaderItem(i, row_header)

            self._set_table_text_cell(i, 0, entry["word"], search_keywords, highlight=True)
            self._set_table_text_cell(i, 1, entry["readings"], search_keywords, highlight=True)
            self._set_table_text_cell(i, 2, entry["type"], search_keywords, highlight=False)
            row_heights.append(self._row_height_for_widgets(i))
        
        # 一次性设置所有行高，减少重绘次数
        self._set_table_row_heights(row_heights)
        
        # 设置表格外观
        self.setup_table_appearance()
        
        # 重新启用表格更新
        self.table_widget.setUpdatesEnabled(True)
        
        # 只检查滚动条，不强制调整所有行高
        QTimer.singleShot(100, self.scroll_to_bottom_check)

    def _set_table_text_cell(self, row, col, text, search_keywords, highlight=True):
        text = "" if text is None else str(text)
        item = QTableWidgetItem()
        item.setData(Qt.UserRole, text)
        item.setTextAlignment(Qt.AlignCenter)

        should_highlight = highlight and any(keyword in text.lower() for keyword in search_keywords)
        if should_highlight:
            item.setData(Qt.DisplayRole, "")
            display_text = highlight_text(text, search_keywords)
        else:
            display_text = text

        self.table_widget.setItem(row, col, item)
        self.table_widget.setCellWidget(row, col, self.create_rich_text_label(display_text))

    def _row_height_for_widgets(self, row):
        col_heights = []
        for col in range(3):
            cell_widget = self.table_widget.cellWidget(row, col)
            if isinstance(cell_widget, CenteredLabel):
                col_heights.append(cell_widget.minimumHeight())
        return max(max(col_heights), DEFAULT_MIN_ROW_HEIGHT) if col_heights else DEFAULT_MIN_ROW_HEIGHT
        
    def ensure_all_rows_visible(self, rows_count):
        """确保所有行都可见，包括最后一行，但不添加多余的底部空间"""
        if rows_count == 0:
            return

        self.table_widget.updateGeometries()
        self.table_widget.viewport().update()

    def scroll_to_bottom_check(self):
        """确保可以滚动到底部，确保最后一行完全可见，但不留太多空白"""
        rows = self.table_widget.rowCount()
        if rows <= 0:
            return

        self.table_widget.updateGeometries()

    def _calculate_vertical_scroll_max(self, rows_count=None):
        rows = self.table_widget.rowCount() if rows_count is None else min(rows_count, self.table_widget.rowCount())
        row_heights = [self.table_widget.rowHeight(i) for i in range(max(0, rows))]
        return calculate_table_scroll_max(
            row_heights,
            self.table_widget.viewport().height(),
            bottom_padding=DEFAULT_SCROLL_BOTTOM_PADDING,
        )
    
    def setup_table_appearance(self):
        """设置表格外观"""
        # 设置表格左上角按钮样式
        corner_button = self.table_widget.findChild(QWidget, "qt_table_vheader")
        if corner_button:
            corner_button.setStyleSheet(TABLE_CORNER_STYLE)
        
        # 确保所有行号都居中对齐
        for i in range(self.table_widget.rowCount()):
            if not self.table_widget.verticalHeaderItem(i):
                row_header = QTableWidgetItem(str(i + 1))
                row_header.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setVerticalHeaderItem(i, row_header)
    
    # 这些方法已重新实现为更高效的版本
    
    def on_section_resized(self, index, old_size, new_size):
        """处理列宽变化，确保每列都有合理的宽度"""
        if self.is_applying_column_widths:
            return

        # 标记为用户正在调整列宽
        self.is_user_resizing = True
        
        total_width = self.table_widget.viewport().width()
        column_widths = [self.table_widget.columnWidth(i) for i in range(3)]
        constrained_widths = constrain_resized_column_widths(
            total_width,
            column_widths,
            index,
            new_size,
        )
        self._set_table_column_widths(constrained_widths)
        
        # 延迟重置标志位，允许用户调整完成
        QTimer.singleShot(500, self.reset_resizing_flag)

    def on_row_resized(self, index, old_size, new_size):
        """用户调整行高后重新计算滚动范围，避免最后一行被遮挡。"""
        if self.is_applying_row_heights:
            return

        vsb = self.table_widget.verticalScrollBar()
        self.row_resize_keep_bottom = bool(vsb and vsb.value() >= max(0, vsb.maximum() - 2))
        if new_size < DEFAULT_MIN_ROW_HEIGHT:
            self._set_single_row_height(index, DEFAULT_MIN_ROW_HEIGHT)
        self.row_resize_timer.start(160)

    def _finish_row_resize(self):
        if QApplication.mouseButtons() & Qt.LeftButton:
            self.row_resize_timer.start(160)
            return

        vsb = self.table_widget.verticalScrollBar()
        self.ensure_all_rows_visible(self.table_widget.rowCount())
        if getattr(self, "row_resize_keep_bottom", False) and vsb:
            QTimer.singleShot(0, lambda: vsb.setValue(vsb.maximum()))
    
    def reset_resizing_flag(self):
        """重置用户调整标志位"""
        self.is_user_resizing = False

    def _set_table_column_widths(self, widths):
        self.is_applying_column_widths = True
        try:
            for col, width in enumerate(widths):
                if self.table_widget.columnWidth(col) != width:
                    self.table_widget.setColumnWidth(col, width)
        finally:
            self.is_applying_column_widths = False

    def _set_table_row_heights(self, heights):
        self.is_applying_row_heights = True
        try:
            for row, height in enumerate(heights):
                self.table_widget.setRowHeight(row, max(int(height), DEFAULT_MIN_ROW_HEIGHT))
        finally:
            self.is_applying_row_heights = False

    def _set_single_row_height(self, row, height):
        self.is_applying_row_heights = True
        try:
            self.table_widget.setRowHeight(row, max(int(height), DEFAULT_MIN_ROW_HEIGHT))
        finally:
            self.is_applying_row_heights = False
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        self.table_widget.setMinimumHeight(0)
        self.table_widget.setMaximumHeight(16777215)
        self.adjust_columns_to_fit()
        self.ensure_all_rows_visible(self.table_widget.rowCount())
    
    def adjust_columns_to_fit(self):
        """调整列宽以适应表格宽度"""
        # 获取表格可用宽度
        available_width = self.table_widget.width() - self.table_widget.verticalHeader().width()
        if self.table_widget.verticalScrollBar().isVisible():
            available_width -= self.table_widget.verticalScrollBar().width()
        
        # 应用列宽比例
        self._set_table_column_widths(ratio_column_widths(available_width, self.column_ratios))
            
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
        
        menu.exec(self.table_widget.viewport().mapToGlobal(position))
    
    def copy_selection(self):
        """复制选中的单元格内容到剪贴板"""
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            return

        selected_cells = {}
        for item in selected_items:
            row = self.table_widget.row(item)
            col = self.table_widget.column(item)
            selected_cells[(row, col)] = self._table_item_copy_text(item)

        QApplication.clipboard().setText(format_selected_cells_as_tsv(selected_cells))

    def _table_item_copy_text(self, item):
        data = item.data(Qt.UserRole)
        if data is not None:
            return data
        return item.text()
    
    def load_dict_data(self):
        """加载词典数据"""
        self.all_entries = list(iter_custom_dict_entries(self.parent.custom_dict))
        # 按词条排序
        self.all_entries.sort(key=lambda x: x['word'])
        
        # 应用当前过滤器和搜索
        self.filter_and_display_entries()
    
    def showEvent(self, event):
        """窗口显示时的处理"""
        super().showEvent(event)
        # 加载词典数据
        self.load_dict_data()
        
        # 禁用表格项的焦点框
        self.remove_focus_rect()
        
        # 居中显示
        center_on_parent(self, self.parent)
        
        # 调整列宽以适应内容
        self.adjust_columns_to_fit()
        QTimer.singleShot(200, lambda: self.ensure_all_rows_visible(self.table_widget.rowCount()))
        QTimer.singleShot(400, self.scroll_to_bottom_check)

    def create_rich_text_label(self, html_content):
        """创建富文本标签用于显示高亮文本"""
        return CenteredLabel(html_content, self)

    def on_cell_double_clicked(self, row, column):
        """处理单元格双击事件"""
        entry = entry_at_page_row(
            self.filtered_entries,
            self.current_page,
            self.entries_per_page,
            row,
        )
        if entry:
            # 获取双击的词条
            entry_type = entry['type']
            word = entry['word']  # 获取词条文本
            
            # 类型映射
            word_type = DISPLAY_NAME_TO_WORD_TYPE.get(entry_type)

            # 如果类型有效，打开对应的编辑窗口
            if word_type:
                self.parent.open_edit_dict_window(word_type, word)  # 传递词条文本
