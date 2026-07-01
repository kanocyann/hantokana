from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QSizePolicy,
    QWidget,
)

from .dict_edit_core import (
    format_entry_text,
    parse_entry_display_text,
    set_dict_entry,
    split_entry_values,
)
from .dict_dialog_styles import (
    COMPACT_LINE_EDIT_STYLE,
    DICT_LIST_STYLE,
    FORM_LABEL_SPACED_STYLE,
    FORM_LABEL_STYLE,
    PATH_LABEL_STYLE,
    action_button_style,
)
from .dict_view_core import get_dict_type_meta
from .dict_migration_core import (
    DELETE_MARKED,
    DELETE_REMOVED,
    SOURCE_CUSTOM,
    SOURCE_DELETED,
    SOURCE_OFFICIAL,
    SOURCE_OVERRIDE,
    delete_custom_entry,
    dict_entry_source,
    source_label,
)
from .storage_core import resource_path as storage_resource_path
from .ui_shared import (
    CustomMessageBox,
    center_on_parent,
    SwitchCheckBox,
)


ROLE_WORD = Qt.UserRole
ROLE_VALUES = Qt.UserRole + 1
ROLE_SOURCE = Qt.UserRole + 2
ROLE_DISPLAY_TEXT = Qt.UserRole + 3


def _resolve_icon_path(parent, relative_path="icon.ico"):
    if parent and hasattr(parent, "resource_path"):
        try:
            return parent.resource_path(relative_path)
        except Exception:
            pass
    return storage_resource_path(relative_path, __file__)

class DictEditDialog(QDialog):
    """词典编辑对话框"""
    def __init__(self, parent, word_type, custom_dict, official_dict=None):
        super().__init__(parent)
        self.word_type = word_type
        self.custom_dict = custom_dict
        self.official_dict = official_dict if isinstance(official_dict, dict) else {}
        meta = get_dict_type_meta(word_type)

        self.setWindowTitle(f"编辑{meta['dialog_title']}词典")
        self.setWindowFlags(Qt.Window)
        self.setModal(True)
        self.setMinimumSize(920, 680)
        self.setStyleSheet("QDialog { background-color: #f4f6f8; }")
        
        # 设置窗口图标 - 添加错误处理
        try:
            self.setWindowIcon(QIcon(_resolve_icon_path(parent, "icon.ico")))
        except Exception:
            pass
        
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(18, 18, 18, 18)

        header = QFrame()
        header.setProperty("card", "true")
        header.setAttribute(Qt.WA_StyledBackground, True)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(16, 14, 16, 14)
        header_layout.setSpacing(6)

        title_label = QLabel(f"编辑 {meta['dialog_title']} 词典")
        title_label.setProperty("title", "true")
        header_layout.addWidget(title_label)

        path_label = QLabel(f"当前用户词典路径: {parent.current_dict_path}")
        path_label.setStyleSheet(PATH_LABEL_STYLE)
        path_label.setWordWrap(True)
        header_layout.addWidget(path_label)
        layout.addWidget(header)

        form_card = QFrame()
        form_card.setProperty("card", "true")
        form_card.setAttribute(Qt.WA_StyledBackground, True)
        input_layout = QVBoxLayout(form_card)
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(16, 16, 16, 16)
        
        # 添加标签，去掉底框线
        word_label = QLabel(meta["word_label"])
        word_label.setStyleSheet(FORM_LABEL_STYLE)
        input_layout.addWidget(word_label)
        
        self.kanji_edit = QLineEdit()
        self.kanji_edit.setPlaceholderText(meta["word_placeholder"])
        self.kanji_edit.setStyleSheet(COMPACT_LINE_EDIT_STYLE)
        input_layout.addWidget(self.kanji_edit)
        
        # 添加标签，去掉底框线
        self.reading_label = QLabel(meta["reading_label"])
        self.reading_label.setStyleSheet(FORM_LABEL_SPACED_STYLE)
        input_layout.addWidget(self.reading_label)
        
        self.readings_edit = QLineEdit()
        self.readings_edit.setPlaceholderText(meta["reading_placeholder"])
        self.readings_edit.setStyleSheet(COMPACT_LINE_EDIT_STYLE)
        input_layout.addWidget(self.readings_edit)

        self.source_hint_label = QLabel("来源：我的词条")
        self.source_hint_label.setStyleSheet(PATH_LABEL_STYLE)
        self.source_hint_label.setWordWrap(True)
        input_layout.addWidget(self.source_hint_label)
        
        layout.addWidget(form_card)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_button = QPushButton("保存词条")
        add_button.setStyleSheet(action_button_style("#73BBA3", "#88D66C", "#5A9D8C"))
        add_button.clicked.connect(self.add_entry)
        
        edit_button = QPushButton("编辑词条")
        edit_button.setStyleSheet(action_button_style("#FFA500", "#FFB700", "#FF8C00"))
        edit_button.clicked.connect(self.edit_entry)
        
        delete_button = QPushButton("删除选中")
        delete_button.setStyleSheet(action_button_style("#F49BAB", "#FFAAAA", "#FF9898"))
        delete_button.clicked.connect(self.delete_selected)
        
        copy_all_button = QPushButton("复制全部")
        copy_all_button.setStyleSheet(action_button_style("#1890ff", "#40a9ff", "#096dd9"))
        copy_all_button.clicked.connect(self.copy_all)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(copy_all_button)
        
        layout.addLayout(button_layout)

        list_card = QFrame()
        list_card.setProperty("card", "true")
        list_card.setAttribute(Qt.WA_StyledBackground, True)
        list_layout = QVBoxLayout(list_card)
        list_layout.setContentsMargins(12, 12, 12, 12)
        list_layout.setSpacing(8)

        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.list_widget.setStyleSheet(DICT_LIST_STYLE)
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout.addWidget(self.list_widget)
        layout.addWidget(list_card, 1)

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
        center_on_parent(self, parent)
        
        # 连接信号
        self.copy_on_select.toggled.connect(self.on_selection_changed)
        self.last_selected_item = None  # 添加标志位

    def _entry_source(self, word):
        return dict_entry_source(self.official_dict, self.custom_dict, self.word_type, word)

    def _entry_values(self, word):
        custom_bucket = self.custom_dict.get(self.word_type, {})
        official_bucket = self.official_dict.get(self.word_type, {})
        if word in custom_bucket and custom_bucket[word]:
            return custom_bucket[word]
        return official_bucket.get(word, [])

    def _iter_visible_entries(self):
        custom_bucket = self.custom_dict.get(self.word_type, {})
        official_bucket = self.official_dict.get(self.word_type, {})
        for word in sorted(set(official_bucket) | set(custom_bucket)):
            source = self._entry_source(word)
            yield word, self._entry_values(word), source

    def _format_visible_entry_text(self, word, values, source):
        if source == SOURCE_DELETED:
            return f"{word} → (已删除)"
        return format_entry_text(word, values)

    def _source_badge_style(self, source):
        colors = {
            SOURCE_OFFICIAL: ("#eef4ff", "#315aa8", "#cbdaf8"),
            SOURCE_CUSTOM: ("#e8f5ef", "#1f6f58", "#b8dfd0"),
            SOURCE_OVERRIDE: ("#fff3e0", "#9a5b00", "#ffd59a"),
            SOURCE_DELETED: ("#fff1f2", "#b42318", "#fecdd3"),
        }
        background, color, border = colors.get(source, ("#f3f4f6", "#4b5563", "#d1d5db"))
        return f"""
        QLabel {{
            background-color: {background};
            color: {color};
            border: 1px solid {border};
            border-radius: 9px;
            padding: 2px 8px;
            font-size: 12px;
            font-weight: 600;
            min-width: 58px;
        }}
        """

    def _create_entry_row_widget(self, word, values, source):
        row = QWidget()
        row.setAttribute(Qt.WA_StyledBackground, True)
        row.setStyleSheet("QWidget { background: transparent; }")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 4, 10, 4)
        row_layout.setSpacing(10)

        entry_label = QLabel(self._format_visible_entry_text(word, values, source))
        entry_label.setMinimumWidth(0)
        entry_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        entry_label.setToolTip(entry_label.text())
        entry_label.setStyleSheet("QLabel { color: #111827; font-size: 13px; background: transparent; }")

        badge_label = QLabel(source_label(source))
        badge_label.setAlignment(Qt.AlignCenter)
        badge_label.setMinimumSize(66, 24)
        badge_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        badge_label.setStyleSheet(self._source_badge_style(source))

        row_layout.addWidget(entry_label, 1)
        row_layout.addWidget(badge_label, 0, Qt.AlignRight | Qt.AlignVCenter)
        return row

    def _item_display_text(self, item):
        return item.data(ROLE_DISPLAY_TEXT) or item.text()

    def _set_source_hint(self, source, word=None):
        label = source_label(source)
        if source == SOURCE_OFFICIAL:
            text = "来源：官方词条。修改后会写入用户词典；删除会在用户词典中记录删除标记。"
        elif source == SOURCE_OVERRIDE:
            text = "来源：已修改。当前显示并转换时优先使用你的版本。"
        elif source == SOURCE_DELETED:
            text = "来源：已删除。转换时不会使用该官方词条；保存非空读音可恢复或重新覆盖。"
        elif source == SOURCE_CUSTOM:
            text = "来源：我的词条。只会保存到用户词典。"
        else:
            text = f"来源：{label}"
        if word:
            text = f"{text}（{word}）"
        self.source_hint_label.setText(text)

    def focus_entry(self, target_word):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(ROLE_WORD) == target_word:
                self.list_widget.setCurrentItem(item)
                self.list_widget.scrollToItem(item)
                self.edit_entry()
                return True

        values = self._entry_values(target_word)
        source = self._entry_source(target_word)
        if values:
            self.kanji_edit.setText(target_word)
            self.readings_edit.setText(", ".join(str(value) for value in values))
            self._set_source_hint(source, target_word)
            self.readings_edit.setFocus()
            self.readings_edit.selectAll()
            return True
        return False
    
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        item = self.list_widget.itemAt(position)

        if item:
            edit_action = menu.addAction("编辑")
            edit_action.triggered.connect(self.edit_entry)
            menu.addSeparator()

        copy_action = menu.addAction("复制")
        copy_action.triggered.connect(self.copy_selected)

        menu.exec(self.list_widget.viewport().mapToGlobal(position))
    
    def copy_selected(self):
        """复制选中的词条"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            CustomMessageBox(self, "提示", "请先选择要复制的词条", style='info').exec()
            return
        
        text = "\n".join(self._item_display_text(item) for item in selected_items)
        QApplication.clipboard().setText(text)
        CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
    
    def update_dict_view(self):
        """更新词典列表显示"""
        self.list_widget.clear()

        for word, values, source in self._iter_visible_entries():
            display_text = self._format_visible_entry_text(word, values, source)
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 46))
            item.setData(ROLE_WORD, word)
            item.setData(ROLE_VALUES, list(values or []))
            item.setData(ROLE_SOURCE, source)
            item.setData(ROLE_DISPLAY_TEXT, display_text)
            if source == SOURCE_OFFICIAL:
                item.setToolTip("官方词条；修改会创建用户版本，删除会记录删除标记。")
            elif source == SOURCE_OVERRIDE:
                item.setToolTip("用户词条正在覆盖官方词条。")
            elif source == SOURCE_DELETED:
                item.setToolTip("该官方词条已被用户删除，转换时不会使用。")
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, self._create_entry_row_widget(word, values, source))
    
    def split_readings(self, raw):
        """分割假名字符串为列表"""
        return split_entry_values(raw)
    
    def add_entry(self):
        """添加词条"""
        # 使用主界面上的输入框
        word = self.kanji_edit.text().strip()
        reading = self.readings_edit.text().strip()
        
        if not word or not reading:
            CustomMessageBox(self, "警告", "词条和读音不能为空", style='warning').exec()
            return
        
        source_before_save = self._entry_source(word)
        readings_list = self.split_readings(reading)
        if not readings_list:
            CustomMessageBox(self, "警告", "读音不能为空", style='warning').exec()
            return

        official_values = list(self.official_dict.get(self.word_type, {}).get(word, []))
        custom_bucket = self.custom_dict.setdefault(self.word_type, {})
        restored_official = bool(official_values) and readings_list == official_values
        if restored_official:
            is_edit = word in custom_bucket
            custom_bucket.pop(word, None)
        else:
            is_edit = set_dict_entry(self.custom_dict, self.word_type, word, readings_list)
        
        self.update_dict_view()
        
        # 保存到文件
        try:
            parent = self.parent()
            if parent and hasattr(parent, "save_custom_dict"):
                parent.save_custom_dict()
            else:
                raise RuntimeError("无法保存词典：父窗口不可用")
        except Exception as e:
            CustomMessageBox(self, "错误", f"保存词条时出错: {str(e)}", style='error').exec()
            return
        
        # 清空输入框
        self.kanji_edit.clear()
        self.readings_edit.clear()
        
        if restored_official:
            CustomMessageBox(self, "成功", "已恢复为官方词条", style='success').exec()
        elif source_before_save == SOURCE_OFFICIAL:
            CustomMessageBox(self, "成功", "已保存为用户词条，并覆盖官方版本", style='success').exec()
        elif source_before_save == SOURCE_DELETED:
            CustomMessageBox(self, "成功", "已重新启用该词条，并保存为用户词条", style='success').exec()
        elif is_edit:
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
        item_text = self._item_display_text(item)
        
        word = item.data(ROLE_WORD)
        values = item.data(ROLE_VALUES)
        source = item.data(ROLE_SOURCE)
        if not word:
            word, reading_part = parse_entry_display_text(item_text)
        elif values is not None:
            reading_part = ", ".join(str(value) for value in values)
        else:
            _word, reading_part = parse_entry_display_text(item_text)

        self.kanji_edit.setText(word)
        self.readings_edit.setText(reading_part)
        self._set_source_hint(source, word)
        
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
            marked_count = 0
            removed_count = 0
            for item in selected_items:
                word = item.data(ROLE_WORD)
                if not word:
                    word, _values = parse_entry_display_text(self._item_display_text(item))
                self.custom_dict, action = delete_custom_entry(
                    self.official_dict,
                    self.custom_dict,
                    self.word_type,
                    word,
                )
                if action == DELETE_MARKED:
                    marked_count += 1
                elif action == DELETE_REMOVED:
                    removed_count += 1
            
            self.update_dict_view()
            
            # 保存到文件
            try:
                parent = self.parent()
                if parent and hasattr(parent, "save_custom_dict"):
                    parent.save_custom_dict()
                else:
                    raise RuntimeError("无法保存词典：父窗口不可用")
            except Exception as e:
                CustomMessageBox(self, "错误", f"保存词条时出错: {str(e)}", style='error').exec()
                return

            if marked_count and removed_count:
                message = "官方词条已记录删除标记，我的词条已从用户词典移除。"
            elif marked_count:
                message = "已在用户词典中记录官方词条删除标记。"
            else:
                message = "已从用户词典中删除。"
            CustomMessageBox(self, "成功", message, style='success').exec()
    
    def copy_all(self):
        """复制所有词条"""
        visible_entries = list(self._iter_visible_entries())
        if not visible_entries:
            CustomMessageBox(self, "提示", "词典为空", style='info').exec()
            return
        
        text = "\n".join(
            self._format_visible_entry_text(word, values, source)
            for word, values, source in visible_entries
        )
        QApplication.clipboard().setText(text)
        CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
    
    def on_selection_changed(self):
        """当选中列表项时，如果启用了'选中即复制'，则复制选中项"""
        if self.copy_on_select.isChecked():
            selected_items = self.list_widget.selectedItems()
            if selected_items:
                current_item = self._item_display_text(selected_items[0])
                if current_item != self.last_selected_item:  # 检查是否与上次选中项相同
                    QApplication.clipboard().setText(current_item)
                    CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
                    self.last_selected_item = current_item  # 更新标志位
            else:
                QApplication.clipboard().clear()
                self.last_selected_item = None  # 清空标志位
