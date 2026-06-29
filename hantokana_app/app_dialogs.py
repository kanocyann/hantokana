import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QRadioButton,
    QPushButton,
    QVBoxLayout,
)

from .ui_shared import CustomCheckBox, SwitchCheckBox, _resolve_icon_path

APP_VERSION = "0.4.0"


def _set_window_icon(widget, parent, relative_path="icon.ico"):
    try:
        widget.setWindowIcon(QIcon(_resolve_icon_path(parent, relative_path)))
    except Exception:
        pass


def _position_dialog(dialog, top_ratio=0.4):
    screen = QApplication.primaryScreen().availableGeometry()
    dialog_size = dialog.size()
    y_position = int((screen.height() - dialog_size.height()) * top_ratio)
    dialog.move(int((screen.width() - dialog_size.width()) / 2), y_position)


def build_settings_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("默认项设置")
    dialog.setWindowFlags(Qt.Window)
    dialog.setModal(True)

    _set_window_icon(dialog, main_window)

    dialog.setStyleSheet("""
        QDialog {
            background-color: #f8f9fa;
        }
        QLabel[heading="true"] {
            font-size: 16px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 8px;
            padding-bottom: 4px;
            border-bottom: 1px solid #e8e8e8;
        }
        QLabel[description="true"] {
            font-size: 12px;
            color: #666666;
            margin-bottom: 8px;
            margin-left: 4px;
        }
        QFrame[section="true"] {
            background-color: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
        }
    """)

    main_layout = QVBoxLayout(dialog)
    main_layout.setSpacing(16)
    main_layout.setContentsMargins(24, 24, 24, 24)

    columns_layout = QHBoxLayout()
    columns_layout.setSpacing(16)

    left_column = QVBoxLayout()
    left_column.setSpacing(16)

    dict_section = QFrame()
    dict_section.setProperty("section", "true")
    dict_layout = QVBoxLayout(dict_section)
    dict_layout.setSpacing(12)
    dict_layout.setContentsMargins(16, 16, 16, 16)

    dict_title = QLabel("词典默认路径设置")
    dict_title.setProperty("heading", "true")
    dict_layout.addWidget(dict_title)

    dict_desc = QLabel("设置词典文件的默认保存路径，用于保存自定义词典数据。")
    dict_desc.setProperty("description", "true")
    dict_desc.setWordWrap(True)
    dict_layout.addWidget(dict_desc)

    path_layout = QHBoxLayout()
    path_layout.setSpacing(8)

    path_edit = QLineEdit()
    path_edit.setText(main_window.current_dict_path or "")
    path_edit.setPlaceholderText("请选择或输入词典文件路径")
    path_edit.setStyleSheet("""
        QLineEdit {
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
            font-size: 13px;
            min-height: 18px;
        }
        QLineEdit:focus {
            border-color: #73BBA3;
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
            border-color: #73BBA3;
            color: #73BBA3;
        }
        QPushButton:pressed {
            background-color: #f0f0f0;
        }
    """)
    select_button.clicked.connect(lambda: main_window.select_path(path_edit))
    path_layout.addWidget(select_button)

    dict_layout.addLayout(path_layout)
    left_column.addWidget(dict_section)

    conflict_section = QFrame()
    conflict_section.setProperty("section", "true")
    conflict_layout = QVBoxLayout(conflict_section)
    conflict_layout.setSpacing(12)
    conflict_layout.setContentsMargins(16, 16, 16, 16)

    conflict_title = QLabel("词典规则冲突检测")
    conflict_title.setProperty("heading", "true")
    conflict_layout.addWidget(conflict_title)

    conflict_desc = QLabel("启用此功能可以检测词典规则冲突导致的词汇丢失问题，并在转换结果中显示冲突报告。")
    conflict_desc.setProperty("description", "true")
    conflict_desc.setWordWrap(True)
    conflict_layout.addWidget(conflict_desc)

    main_window.conflict_detection_checkbox = SwitchCheckBox("启用词典规则冲突检测")
    main_window.conflict_detection_checkbox.setChecked(main_window.enable_conflict_detection)
    main_window.conflict_detection_checkbox.setStyleSheet("""
        font-size: 14px;
        color: #333333;
        margin-top: 4px;
    """)
    conflict_layout.addWidget(main_window.conflict_detection_checkbox)

    left_column.addWidget(conflict_section)
    columns_layout.addLayout(left_column)

    right_column = QVBoxLayout()
    right_column.setSpacing(16)

    tray_section = QFrame()
    tray_section.setProperty("section", "true")
    tray_layout = QVBoxLayout(tray_section)
    tray_layout.setSpacing(12)
    tray_layout.setContentsMargins(16, 16, 16, 16)

    tray_title = QLabel("托盘设置")
    tray_title.setProperty("heading", "true")
    tray_layout.addWidget(tray_title)

    tray_desc = QLabel("设置关闭窗口时的行为，可以选择最小化到系统托盘或完全退出程序。")
    tray_desc.setProperty("description", "true")
    tray_desc.setWordWrap(True)
    tray_layout.addWidget(tray_desc)

    config = main_window.load_config()
    show_close_prompt = not config.get("minimize_to_tray_without_asking", False)
    close_action = config.get("close_action", "minimize")

    prompt_frame = QFrame()
    prompt_frame.setStyleSheet("background: transparent; margin-top: 4px;")
    prompt_layout = QVBoxLayout(prompt_frame)
    prompt_layout.setContentsMargins(0, 0, 0, 8)
    prompt_layout.setSpacing(4)

    close_prompt_checkbox = SwitchCheckBox("关闭窗口时显示提示对话框")
    close_prompt_checkbox.setChecked(show_close_prompt)
    close_prompt_checkbox.setStyleSheet("""
        font-size: 14px;
        color: #333333;
    """)
    close_prompt_checkbox.setObjectName("close_prompt_checkbox")
    prompt_layout.addWidget(close_prompt_checkbox)

    prompt_desc = QLabel("启用此选项后，关闭窗口时将显示提示对话框，询问是否最小化到托盘或退出程序。")
    prompt_desc.setWordWrap(True)
    prompt_desc.setStyleSheet("""
        font-size: 12px;
        color: #666666;
        margin-left: 20px;
    """)
    prompt_layout.addWidget(prompt_desc)

    tray_layout.addWidget(prompt_frame)

    action_label = QLabel("默认关闭行为（当不显示提示对话框时）：")
    action_label.setStyleSheet("""
        font-size: 14px;
        color: #333333;
        margin-top: 8px;
    """)
    tray_layout.addWidget(action_label)

    radio_frame = QFrame()
    radio_frame.setStyleSheet("background: transparent; margin-left: 24px;")
    radio_layout = QVBoxLayout(radio_frame)
    radio_layout.setContentsMargins(0, 4, 0, 0)
    radio_layout.setSpacing(12)

    radio_style = """
        QRadioButton {
            font-size: 13px;
            color: #333333;
            spacing: 10px;
            padding: 2px 0;
        }

        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 1px solid #aaaaaa;
            background-color: white;
        }

        QRadioButton::indicator:checked {
            border: 1px solid #73BBA3;
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.4, fx:0.5, fy:0.5,
                                       stop:0.0 #73BBA3, stop:0.65 #73BBA3, stop:0.7 white);
        }

        QRadioButton::indicator:hover {
            border-color: #88D66C;
        }

        QRadioButton:hover {
            color: #73BBA3;
        }
    """

    minimize_radio = QRadioButton("最小化到托盘 - 应用程序将继续在后台运行")
    minimize_radio.setChecked(close_action == "minimize")
    minimize_radio.setObjectName("minimize_radio")
    minimize_radio.setStyleSheet(radio_style)
    radio_layout.addWidget(minimize_radio)

    exit_radio = QRadioButton("退出程序 - 完全关闭应用程序")
    exit_radio.setChecked(close_action == "exit")
    exit_radio.setObjectName("exit_radio")
    exit_radio.setStyleSheet(radio_style)
    radio_layout.addWidget(exit_radio)

    tray_layout.addWidget(radio_frame)

    action_desc = QLabel("选择关闭窗口时的默认行为，仅在不显示提示对话框时生效。")
    action_desc.setWordWrap(True)
    action_desc.setStyleSheet("""
        font-size: 12px;
        color: #666666;
        margin-left: 24px;
    """)
    tray_layout.addWidget(action_desc)

    right_column.addWidget(tray_section)
    columns_layout.addLayout(right_column)

    main_layout.addLayout(columns_layout)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(12)
    button_layout.addStretch()

    cancel_button = QPushButton("取消")
    cancel_button.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: #333333;
            border: 1px solid #d9d9d9;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 13px;
            min-width: 80px;
        }
        QPushButton:hover {
            border-color: #F49BAB;
            color: #F49BAB;
        }
        QPushButton:pressed {
            background-color: #f5f5f5;
        }
    """)
    cancel_button.clicked.connect(dialog.reject)

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
            background-color: #5A9D8C;
        }
    """)
    save_button.clicked.connect(lambda: main_window.save_settings(path_edit, dialog))

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(save_button)
    button_layout.addStretch()

    main_layout.addLayout(button_layout)
    dialog.setMinimumSize(950, 450)
    _position_dialog(dialog)
    return dialog


def build_about_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("关于")
    dialog.setWindowFlags(Qt.Window)
    dialog.setModal(True)

    _set_window_icon(dialog, main_window)

    layout = QVBoxLayout(dialog)
    layout.setSpacing(8)
    layout.setContentsMargins(16, 16, 16, 16)

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
    main_layout.setSpacing(8)

    title_label = QLabel("日文汉字 - 假名/罗马音转换工具")
    title_label.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #1f1f1f;
        margin-bottom: 2px;
    """)
    title_label.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title_label)

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

    try:
        image_path = _resolve_icon_path(main_window, "hantokana.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            image_label = QLabel()
            image_label.setPixmap(pixmap)
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

    version_label = QLabel(f"版本: {APP_VERSION}")
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

    ok_button = QPushButton("确定")
    ok_button.setFixedWidth(100)
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

    dialog.setMinimumSize(450, 400)
    _position_dialog(dialog)
    return dialog


def build_close_choice_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("关闭选项")
    dialog.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
    dialog.setFixedWidth(400)
    dialog.setStyleSheet("""
        QDialog {
            background-color: #fafafa;
            border-radius: 8px;
        }
    """)

    _set_window_icon(dialog, main_window)

    layout = QVBoxLayout(dialog)
    layout.setSpacing(20)
    layout.setContentsMargins(24, 24, 24, 24)

    title_layout = QHBoxLayout()

    icon_label = QLabel("?")
    icon_label.setStyleSheet("""
        QLabel {
            font-size: 28px;
            color: #73BBA3;
            font-weight: bold;
        }
    """)
    title_layout.addWidget(icon_label)

    title_text = QLabel("关闭程序")
    title_text.setStyleSheet("""
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #333333;
        }
    """)
    title_layout.addWidget(title_text)
    title_layout.addStretch()
    layout.addLayout(title_layout)

    message_label = QLabel("您希望如何处理应用程序？")
    message_label.setWordWrap(True)
    message_label.setStyleSheet("""
        QLabel {
            font-size: 14px;
            color: #333333;
            margin-bottom: 10px;
        }
    """)
    layout.addWidget(message_label)

    minimize_info = QLabel("• 最小化到托盘：应用程序将继续在后台运行，您可以通过点击系统托盘图标重新打开。")
    minimize_info.setWordWrap(True)
    minimize_info.setStyleSheet("""
        QLabel {
            font-size: 13px;
            color: #666666;
            margin-bottom: 5px;
        }
    """)
    layout.addWidget(minimize_info)

    exit_info = QLabel("• 退出程序：完全关闭应用程序，您需要重新启动才能使用。")
    exit_info.setWordWrap(True)
    exit_info.setStyleSheet("""
        QLabel {
            font-size: 13px;
            color: #666666;
            margin-bottom: 15px;
        }
    """)
    layout.addWidget(exit_info)

    remember_choice_checkbox = CustomCheckBox("记住我的选择，下次无需询问")
    remember_choice_checkbox.setStyleSheet("""
        QCheckBox {
            font-size: 13px;
            color: #666666;
            margin-bottom: 15px;
        }
    """)
    remember_choice_checkbox.setObjectName("remember_choice_checkbox")
    layout.addWidget(remember_choice_checkbox)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(20)

    minimize_button = QPushButton("最小化到托盘")
    minimize_button.setStyleSheet("""
        QPushButton {
            background-color: #73BBA3;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 13px;
            min-width: 140px;
        }
        QPushButton:hover {
            background-color: #88D66C;
        }
        QPushButton:pressed {
            background-color: #5A9D8C;
        }
    """)
    minimize_button.clicked.connect(dialog.accept)

    exit_button = QPushButton("退出程序")
    exit_button.setStyleSheet("""
        QPushButton {
            background-color: #F49BAB;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 13px;
            min-width: 140px;
        }
        QPushButton:hover {
            background-color: #FFAAAA;
        }
        QPushButton:pressed {
            background-color: #FF9898;
        }
    """)
    exit_button.clicked.connect(lambda: dialog.done(2))

    button_layout.addStretch(1)
    button_layout.addWidget(minimize_button)
    button_layout.addStretch(1)
    button_layout.addWidget(exit_button)
    button_layout.addStretch(1)
    layout.addLayout(button_layout)

    _position_dialog(dialog)
    return dialog
