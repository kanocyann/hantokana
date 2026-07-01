from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QSizePolicy,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
import pykakasi
from fugashi import Tagger
from .conversion_core import (
    kana_to_romaji,
    empty_custom_dict,
)
from .ui_shared import (
    CustomCheckBox,
    SwitchCheckBox,
    PlainTextEdit,
    CustomMessageBox,
)
from .storage_core import (
    get_dict_path as storage_get_dict_path,
    get_effective_dict_path as storage_get_effective_dict_path,
    get_official_dict_path as storage_get_official_dict_path,
    get_config_path as storage_get_config_path,
    sync_official_dict_to_appdata as storage_sync_official_dict_to_appdata,
    resource_path as storage_resource_path,
    load_config as storage_load_config,
    save_config as storage_save_config,
    load_custom_dict as storage_load_custom_dict,
    save_custom_dict as storage_save_custom_dict,
    save_effective_dict as storage_save_effective_dict,
    import_dict_file as storage_import_dict_file,
)
from .app_dialogs import (
    build_about_dialog,
    build_close_choice_dialog,
    build_settings_dialog,
)
from .app_config import DEFAULT_APP_CONFIG
from .conversion_service import convert_text_payload
from .dict_migration_core import (
    build_effective_dict_cache,
    dict_entry_source,
    prune_redundant_custom_entries,
    source_label,
)
from .dict_dialogs import DictEditDialog, DictSearchDialog
from .ui_styles import (
    MAIN_TEXT_EDIT_STYLE,
    MAIN_WINDOW_STYLE_SHEET,
    PRIMARY_ACTION_BUTTON_STYLE,
    SECONDARY_ACTION_BUTTON_STYLE,
    TERTIARY_ACTION_BUTTON_STYLE,
)

class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("日文汉字-假名/罗马音 转换工具")
        self.setMinimumSize(1000, 720)
        self.setStyleSheet(MAIN_WINDOW_STYLE_SHEET)
        
        # 设置窗口图标
        icon_path = storage_resource_path("icon.ico", __file__)
        self.setWindowIcon(QIcon(icon_path))
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("日文汉字-假名/罗马音 转换工具")
        
        # 创建托盘菜单
        self.tray_menu = QMenu()
        self.restore_action = QAction("显示主窗口", self)
        self.restore_action.triggered.connect(self.showNormal)
        self.quit_action = QAction("退出", self)
        self.quit_action.triggered.connect(self.quit_application)
        self.tray_menu.addAction(self.restore_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # 托盘图标点击事件
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # 显示托盘图标
        self.tray_icon.show()
        
        # 初始化变量
        self.official_dict = empty_custom_dict()
        self.custom_dict = {
            "normal_words": {},
            "compound_words": {},
            "prefix_combinations": {},
            "suffix_combinations": {}
        }
        self.effective_dict = empty_custom_dict()
        self.effective_dict_path = storage_get_effective_dict_path()
        self.current_dict_path = None
        self.tagger = None
        self.conv = None
        self.dict_search_dialog = None  # 添加词典搜索对话框变量
        self.enable_conflict_detection = DEFAULT_APP_CONFIG["enable_conflict_detection"]
        self._window_fade_animation = None
        
        # 加载配置和字典
        self.load_config()
        self.load_dictionaries()
        
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

    def showEvent(self, event):
        super().showEvent(event)
        self._fade_in_window()

    def _fade_in_window(self):
        try:
            self.setWindowOpacity(0.0)
            animation = QPropertyAnimation(self, b"windowOpacity", self)
            animation.setDuration(160)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.OutCubic)
            animation.start()
            self._window_fade_animation = animation
        except Exception:
            pass
    
    def setup_ui(self):
        """设置UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        self.create_menu()

        input_card, input_layout = self._build_card("输入文本")
        self.text_input = PlainTextEdit()
        self.text_input.setMinimumHeight(240)
        self.text_input.setPlaceholderText("请输入要转换的日文文本")
        self.text_input.setStyleSheet(MAIN_TEXT_EDIT_STYLE)
        input_layout.addWidget(self.text_input, 1)

        self.use_hira = CustomCheckBox("平假名")
        self.use_hira.setChecked(True)
        self.use_kata = CustomCheckBox("片假名")
        self.use_kata.setChecked(True)
        self.use_roma = CustomCheckBox("罗马音")
        self.use_roma.setChecked(True)

        input_actions = QHBoxLayout()
        input_actions.setSpacing(12)
        input_actions.addWidget(self.use_hira)
        input_actions.addWidget(self.use_kata)
        input_actions.addWidget(self.use_roma)
        input_actions.addStretch(1)
        clear_input_button = self._build_action_button("清空输入", self.text_input.clear, tertiary=True)
        convert_button = self._build_action_button("开始转换", self.convert_text, primary=True)
        input_actions.addWidget(clear_input_button)
        input_actions.addWidget(convert_button)
        input_layout.addLayout(input_actions)
        layout.addWidget(input_card, 1)

        output_card, output_layout = self._build_card("转换结果")
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setPlaceholderText("转换结果将显示在这里")
        self.text_output.setMinimumHeight(240)
        self.text_output.setStyleSheet(MAIN_TEXT_EDIT_STYLE)
        output_layout.addWidget(self.text_output, 1)

        output_actions = QHBoxLayout()
        output_actions.setSpacing(8)
        output_actions.addStretch(1)
        clear_output_button = self._build_action_button("清空结果", self.text_output.clear, tertiary=True)
        copy_button = self._build_action_button("复制结果", self.copy_result, secondary=True)
        output_actions.addWidget(clear_output_button)
        output_actions.addWidget(copy_button)
        output_layout.addLayout(output_actions)
        layout.addWidget(output_card, 1)

    def _build_card(self, title, subtitle=None):
        frame = QFrame()
        frame.setProperty("card", "true")
        frame.setAttribute(Qt.WA_StyledBackground, True)
        layout = QVBoxLayout(frame)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        title_label = QLabel(title)
        title_label.setProperty("section", "true")
        layout.addWidget(title_label)

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setProperty("muted", "true")
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)

        return frame, layout

    def _build_action_button(self, text, slot, secondary=False, primary=False, tertiary=False):
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button.setFixedHeight(34)
        if primary:
            button.setStyleSheet(PRIMARY_ACTION_BUTTON_STYLE)
        elif tertiary:
            button.setStyleSheet(TERTIARY_ACTION_BUTTON_STYLE)
        elif secondary:
            button.setStyleSheet(SECONDARY_ACTION_BUTTON_STYLE)
        else:
            button.setStyleSheet(SECONDARY_ACTION_BUTTON_STYLE)
        button.clicked.connect(lambda _checked=False, _slot=slot: _slot())
        return button

    def _format_dict_path_label(self):
        path = self.current_dict_path or storage_get_dict_path()
        return f"当前用户词典：{path}"

    def _refresh_home_status(self):
        dict_text = self._format_dict_path_label()
        if hasattr(self, "dict_path_label"):
            self.dict_path_label.setText(dict_text)
        if hasattr(self, "status_dict_label"):
            self.status_dict_label.setText(dict_text)
        if hasattr(self, "conflict_state_label"):
            state = "已启用" if self.enable_conflict_detection else "已关闭"
            self.conflict_state_label.setText(f"冲突检测：{state}")
    
    def create_menu(self):
        """创建菜单"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        import_action = QAction("导入词典", self)
        import_action.triggered.connect(self.load_dict)
        file_menu.addAction(import_action)

        file_menu.addSeparator()
        
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
        edit_combinations_action.triggered.connect(lambda: self.open_edit_dict_window("suffix_combinations"))
        file_menu.addAction(edit_combinations_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 设置菜单
        settings_menu = menubar.addMenu("设置")
        dict_path_action = QAction("默认项设置", self)
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
            config_path = storage_get_config_path()
            config = storage_load_config(config_path)
            self.current_dict_path = config.get("current_dict_path") or storage_get_dict_path()
            self.enable_conflict_detection = config.get(
                "enable_conflict_detection",
                DEFAULT_APP_CONFIG["enable_conflict_detection"],
            )
        except Exception as e:
            print(f"加载配置时出错: {e}")
            # 如果加载失败，使用默认配置
            self.current_dict_path = storage_get_dict_path()
            self.enable_conflict_detection = DEFAULT_APP_CONFIG["enable_conflict_detection"]
        self._refresh_home_status()
        return config  # 始终返回一个字典，即使是空的
    
    def load_dictionaries(self):
        """加载官方词典和用户词典。"""
        custom_dict_path = (self.current_dict_path or "").strip() or storage_get_dict_path()

        try:
            official_resource_path = storage_resource_path("custom_dict.json", __file__)
            self.official_dict, _official_path = storage_sync_official_dict_to_appdata(
                official_resource_path,
                storage_get_official_dict_path(),
            )
        except Exception as e:
            print(f"加载官方词典失败: {str(e)}")
            self.official_dict = empty_custom_dict()

        try:
            self.custom_dict, custom_dict_path = storage_load_custom_dict(custom_dict_path)
            self.custom_dict, did_prune_custom = prune_redundant_custom_entries(
                self.official_dict,
                self.custom_dict,
            )
            if did_prune_custom:
                storage_save_custom_dict(custom_dict_path, self.custom_dict)
            self.current_dict_path = custom_dict_path
        except Exception as e:
            print(f"加载用户词典失败: {str(e)}")
            fallback_path = storage_get_dict_path()
            try:
                self.custom_dict, fallback_path = storage_load_custom_dict(fallback_path)
                self.current_dict_path = fallback_path
            except Exception as fallback_error:
                print(f"加载默认用户词典失败: {str(fallback_error)}")
                self.custom_dict = empty_custom_dict()
                self.current_dict_path = fallback_path

        self._refresh_effective_dict()
        self._refresh_home_status()

    def load_custom_dict(self):
        self.load_dictionaries()

    def _refresh_effective_dict(self):
        self.effective_dict = build_effective_dict_cache(self.official_dict, self.custom_dict)
        try:
            storage_save_effective_dict(self.effective_dict_path, self.effective_dict)
        except Exception as e:
            print(f"保存运行词典缓存失败: {e}")

    def get_entry_source(self, word_type, word):
        return dict_entry_source(self.official_dict, self.custom_dict, word_type, word)

    def get_entry_values_for_edit(self, word_type, word):
        custom_bucket = self.custom_dict.get(word_type, {})
        if word in custom_bucket:
            return custom_bucket[word]
        return self.official_dict.get(word_type, {}).get(word, [])

    def describe_entry_source(self, word_type, word):
        return source_label(self.get_entry_source(word_type, word))
    
    def save_custom_dict(self):
        """保存自定义词典"""
        dict_path = self.current_dict_path or storage_get_dict_path()
        try:
            self.custom_dict, _did_prune_custom = prune_redundant_custom_entries(
                self.official_dict,
                self.custom_dict,
            )
            storage_save_custom_dict(dict_path, self.custom_dict)
            self._refresh_effective_dict()
        except Exception as e:
            print(f"保存字典文件失败: {str(e)}")

    def save_config(self, config):
        """保存配置到文件"""
        try:
            storage_save_config(storage_get_config_path(), config)
            self._refresh_home_status()
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def init_tagger(self):
        """初始化分词器"""
        try:
            return Tagger('-r "' + storage_resource_path('dicdir/mecabrc', __file__) + '" -d "' + storage_resource_path('dicdir', __file__) + '"')
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
        try:
            result = convert_text_payload(
                self.text_input.toPlainText(),
                self.effective_dict,
                self.tagger,
                self.conv,
                self.use_hira.isChecked(),
                self.use_kata.isChecked(),
                self.use_roma.isChecked(),
                self.convert_to_romaji,
                conflict_detection=self.enable_conflict_detection,
            )
            self.text_output.setPlainText((result or "").strip())
        except Exception as e:
            CustomMessageBox(self, "错误", str(e), style='error').exec()

    def convert_to_romaji(self, kana_text, surface_text=None):
        """将假名转换为罗马音，正确处理促音和拗音"""
        return kana_to_romaji(kana_text, surface_text)

   
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
            icon_path = storage_resource_path("icon.ico", __file__)
            file_dialog.setWindowIcon(QIcon(icon_path))
        except Exception:
            # 如果设置图标失败，忽略错误继续执行
            pass
        
        if file_dialog.exec() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if not file_path:
                return
            try:
                merged = storage_import_dict_file(self.custom_dict, file_path)
                if isinstance(merged, dict):
                    self.custom_dict = merged
                    self.save_custom_dict()
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
        dialog = DictEditDialog(self, word_type, self.custom_dict, self.official_dict)
        # 设置窗口图标
        icon_path = storage_resource_path("icon.ico", __file__)
        dialog.setWindowIcon(QIcon(icon_path))
        
        # 如果指定了目标词条，尝试定位
        if target_word:
            dialog.focus_entry(target_word)
        
        if dialog.exec() == QDialog.Accepted:
            # 更新主窗口的词典数据
            self.custom_dict = dialog.custom_dict
            # 保存到文件
            self.save_custom_dict()
    
    def open_settings_window(self):
        """打开设置窗口"""
        dialog = build_settings_dialog(self)
        dialog.exec()
    
    def select_path(self, path_edit):
        """选择词库路径"""
        parent_dialog = path_edit.window()  # 获取设置窗口作为父窗口
        
        # 创建文件对话框并设置图标
        file_dialog = QFileDialog(parent_dialog)
        file_dialog.setWindowTitle("选择默认用户词典文件")
        file_dialog.setNameFilter("JSON 文件 (*.json)")
        
        # 设置窗口图标
        try:
            icon_path = storage_resource_path("icon.ico", __file__)
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
        # 保存配置到JSON文件
        config = self.load_config()

        new_path = path_edit.text().strip() or storage_get_dict_path()
        self.current_dict_path = new_path
        config["current_dict_path"] = self.current_dict_path
        
        # 保存关闭行为。继续写入旧配置字段，兼容已有配置和关闭弹窗逻辑。
        tray_ask_radio = settings_window.findChild(QRadioButton, "tray_policy_ask_radio")
        minimize_radio = settings_window.findChild(QRadioButton, "minimize_radio")
        exit_radio = settings_window.findChild(QRadioButton, "exit_radio")
        if tray_ask_radio and minimize_radio and exit_radio:
            if tray_ask_radio.isChecked():
                config["minimize_to_tray_without_asking"] = False
            elif minimize_radio.isChecked():
                config["minimize_to_tray_without_asking"] = True
                config["close_action"] = "minimize"
            elif exit_radio.isChecked():
                config["minimize_to_tray_without_asking"] = True
                config["close_action"] = "exit"
        
        # 保存冲突检测设置
        if hasattr(self, 'conflict_detection_checkbox'):
            self.enable_conflict_detection = self.conflict_detection_checkbox.isChecked()
            config["enable_conflict_detection"] = self.enable_conflict_detection

        # 保存配置
        self.save_config(config)
        self.load_dictionaries()
        self._refresh_home_status()
        
        settings_window.accept()
    
    def open_about_window(self):
        """打开关于页面"""
        dialog = build_about_dialog(self)
        dialog.exec()
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        # 如果用户之前选择了记住选择，则根据保存的选择执行操作
        config = self.load_config()
        if config.get("minimize_to_tray_without_asking", False):
            close_action = config.get("close_action", "minimize")
            if close_action == "minimize":
                # 直接最小化到托盘
                self.hide()
                event.ignore()
                return
            elif close_action == "exit":
                # 直接退出程序
                self.quit_application()
                return
            
        dialog = build_close_choice_dialog(self)
        result = dialog.exec()
        
        # 保存用户选择
        remember_choice = dialog.findChild(CustomCheckBox, "remember_choice_checkbox")
        if remember_choice and remember_choice.isChecked():
            config = self.load_config()
            if result == QDialog.Accepted:  # 用户选择了最小化到托盘
                config["close_action"] = "minimize"
                config["minimize_to_tray_without_asking"] = True
            elif result == 2:  # 用户选择了退出程序
                config["close_action"] = "exit"
                config["minimize_to_tray_without_asking"] = True
            self.save_config(config)
        
        if result == QDialog.Accepted:  # 最小化到托盘
            self.hide()
            event.ignore()
        elif result == 2:  # 退出程序
            self.quit_application()
        else:  # 取消
            event.ignore()
    
    def tray_icon_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 单击托盘图标，显示/隐藏主窗口
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.activateWindow()  # 激活窗口，使其获得焦点
    
    def quit_application(self):
        """退出应用程序"""
        # 移除托盘图标
        self.tray_icon.hide()
        # 退出应用程序
        QApplication.quit()
    
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

