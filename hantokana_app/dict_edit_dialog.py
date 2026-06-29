from PySide6.QtCore import Qt
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
)

from .dict_edit_core import (
    delete_dict_entries,
    format_entry_text,
    iter_edit_entries,
    parse_entry_display_text,
    set_dict_entry,
    split_entry_values,
)
from .dict_dialog_styles import (
    COMPACT_LINE_EDIT_STYLE,
    DICT_LIST_STYLE,
    FORM_LABEL_SPACED_STYLE,
    FORM_LABEL_STYLE,
    PANEL_FRAME_STYLE,
    PATH_LABEL_STYLE,
    action_button_style,
)
from .dict_view_core import get_dict_type_meta
from .storage_core import resource_path as storage_resource_path
from .ui_shared import (
    CustomMessageBox,
    center_on_parent,
    SwitchCheckBox,
)


def _resolve_icon_path(parent, relative_path="icon.ico"):
    if parent and hasattr(parent, "resource_path"):
        try:
            return parent.resource_path(relative_path)
        except Exception:
            pass
    return storage_resource_path(relative_path, __file__)

class DictEditDialog(QDialog):
    """词典编辑对话框"""
    def __init__(self, parent, word_type, custom_dict):
        super().__init__(parent)
        self.word_type = word_type
        self.custom_dict = custom_dict
        meta = get_dict_type_meta(word_type)

        self.setWindowTitle(f"编辑{meta['dialog_title']}词典")
        self.setWindowFlags(Qt.Window)
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        # 设置窗口图标 - 添加错误处理
        try:
            self.setWindowIcon(QIcon(_resolve_icon_path(parent, "icon.ico")))
        except Exception:
            pass
        
        # 创建布局
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 路径显示
        path_label = QLabel(f"当前词典文件路径: {parent.current_dict_path}")
        path_label.setStyleSheet(PATH_LABEL_STYLE)
        layout.addWidget(path_label)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel)
        input_frame.setStyleSheet(PANEL_FRAME_STYLE)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(8)  # 减小间距
        input_layout.setContentsMargins(12, 12, 12, 12)  # 设置内边距
        
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
        
        layout.addWidget(input_frame)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
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
        
        # 词典列表
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        self.list_widget.setStyleSheet(DICT_LIST_STYLE)
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
        center_on_parent(self, parent)
        
        # 连接信号
        self.copy_on_select.toggled.connect(self.on_selection_changed)
        self.last_selected_item = None  # 添加标志位
    
    
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
        
        text = "\n".join(item.text() for item in selected_items)
        QApplication.clipboard().setText(text)
        CustomMessageBox(self, "成功", "已复制到剪贴板", style='success').exec()
    
    def update_dict_view(self):
        """更新词典列表显示"""
        self.list_widget.clear()

        for word, values in iter_edit_entries(self.custom_dict, self.word_type):
            item = QListWidgetItem(format_entry_text(word, values))
            item.setData(Qt.UserRole, word)
            self.list_widget.addItem(item)
    
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
        
        readings_list = self.split_readings(reading)
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
        
        word = item.data(Qt.UserRole)
        if not word:
            word, reading_part = parse_entry_display_text(item_text)
        else:
            _word, reading_part = parse_entry_display_text(item_text)

        self.kanji_edit.setText(word)
        self.readings_edit.setText(reading_part)
        
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
            words = []
            for item in selected_items:
                word = item.data(Qt.UserRole)
                if not word:
                    word, _values = parse_entry_display_text(item.text())
                words.append(word)
            delete_dict_entries(self.custom_dict, self.word_type, words)
            
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
            
            CustomMessageBox(self, "成功", "词条删除成功", style='success').exec()
    
    def copy_all(self):
        """复制所有词条"""
        if not self.custom_dict.get(self.word_type):
            CustomMessageBox(self, "提示", "词典为空", style='info').exec()
            return
        
        text = "\n".join(
            format_entry_text(word, values)
            for word, values in iter_edit_entries(self.custom_dict, self.word_type)
        )
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
