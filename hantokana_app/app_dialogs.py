import os

from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QRadioButton,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .ui_shared import CustomCheckBox, SwitchCheckBox, _resolve_icon_path
from .app_config import (
    APP_VERSION,
)


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


def _fade_in(widget, duration=140):
    try:
        widget.setWindowOpacity(0.0)
        animation = QPropertyAnimation(widget, b"windowOpacity", widget)
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        widget._fade_animation = animation
    except Exception:
        pass


def _card(title, description=None):
    frame = QFrame()
    frame.setProperty("card", "true")
    frame.setAttribute(Qt.WA_StyledBackground, True)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(10)

    title_label = QLabel(title)
    title_label.setProperty("section", True)
    layout.addWidget(title_label)

    if description:
        desc_label = QLabel(description)
        desc_label.setProperty("muted", True)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

    return frame, layout


def _dialog_button(text, primary=False):
    button = QPushButton(text)
    button.setCursor(Qt.PointingHandCursor)
    button.setFixedHeight(34)
    if primary:
        button.setStyleSheet("""
            QPushButton {
                background-color: #2f7d67;
                color: white;
                border: 1px solid #2f7d67;
                border-radius: 10px;
                padding: 7px 14px;
                min-width: 96px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3b9378;
                border-color: #3b9378;
            }
            QPushButton:pressed {
                background-color: #256352;
                border-color: #256352;
            }
        """)
    else:
        button.setStyleSheet("""
            QPushButton {
                background-color: #f7f9fb;
                color: #344054;
                border: 1px solid #dbe3ea;
                border-radius: 10px;
                padding: 7px 14px;
                min-width: 84px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #eef7f3;
                border-color: #2f7d67;
                color: #2f7d67;
            }
            QPushButton:pressed {
                background-color: #e0efe9;
            }
        """)
    return button


def _settings_radio(text, object_name, checked=False):
    radio = QRadioButton(text)
    radio.setObjectName(object_name)
    radio.setChecked(checked)
    radio.setStyleSheet("""
        QRadioButton {
            background: transparent;
            border: none;
            padding: 0px;
            margin: 0px;
            spacing: 8px;
            color: #111827;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 1px solid #b7c0cb;
            background-color: white;
        }
        QRadioButton::indicator:checked {
            border-color: #2f7d67;
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.42, fx:0.5, fy:0.5,
                                        stop:0.0 #2f7d67, stop:0.65 #2f7d67, stop:0.7 white);
        }
        QRadioButton::indicator:hover {
            border-color: #3b9378;
        }
    """)
    return radio


def build_settings_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("默认项设置")
    dialog.setWindowFlags(Qt.Window)
    dialog.setModal(True)
    dialog.setObjectName("settings_dialog")

    _set_window_icon(dialog, main_window)
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f4f6f8;
        }
        QLabel[title="true"] {
            font-size: 18px;
            font-weight: 700;
            color: #111827;
        }
        QLabel[muted="true"] {
            color: #667085;
            font-size: 12px;
        }
    """)

    main_layout = QVBoxLayout(dialog)
    main_layout.setSpacing(12)
    main_layout.setContentsMargins(16, 16, 16, 16)

    header = QFrame()
    header.setProperty("card", "true")
    header.setAttribute(Qt.WA_StyledBackground, True)
    header_layout = QVBoxLayout(header)
    header_layout.setContentsMargins(16, 14, 16, 14)
    header_layout.setSpacing(6)

    title = QLabel("默认项设置")
    title.setProperty("title", "true")
    header_layout.addWidget(title)

    desc = QLabel("这里控制用户词典路径、词典诊断和关闭行为。")
    desc.setProperty("muted", "true")
    desc.setWordWrap(True)
    header_layout.addWidget(desc)
    main_layout.addWidget(header)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setSpacing(12)
    content_layout.setContentsMargins(0, 0, 0, 0)

    config = main_window.load_config()
    show_close_prompt = not config.get("minimize_to_tray_without_asking", False)
    close_action = config.get("close_action", "minimize")

    dict_section, dict_layout = _card(
        "默认用户词典",
        "官方词典会随程序自动加载；这里选择的是你的个人词典文件。",
    )
    path_row = QHBoxLayout()
    path_row.setSpacing(8)
    path_edit = QLineEdit()
    path_edit.setText(main_window.current_dict_path or "")
    path_edit.setPlaceholderText("请选择或输入用户词典文件路径")
    path_edit.setMinimumHeight(34)
    path_row.addWidget(path_edit, 1)
    select_button = _dialog_button("选择文件")
    select_button.clicked.connect(lambda: main_window.select_path(path_edit))
    path_row.addWidget(select_button)
    dict_layout.addLayout(path_row)
    content_layout.addWidget(dict_section)

    conflict_section, conflict_layout = _card("词典诊断", "默认关闭。启用后只在诊断模式下提示潜在冲突。")
    main_window.conflict_detection_checkbox = SwitchCheckBox("启用词典规则冲突检测")
    main_window.conflict_detection_checkbox.setChecked(main_window.enable_conflict_detection)
    conflict_layout.addWidget(main_window.conflict_detection_checkbox)
    content_layout.addWidget(conflict_section)

    tray_section, tray_layout = _card("托盘行为", "控制关闭窗口时的默认动作。")
    tray_group = QVBoxLayout()
    tray_group.setSpacing(8)

    tray_ask_radio = _settings_radio("每次询问我", "tray_policy_ask_radio", show_close_prompt)
    tray_group.addWidget(tray_ask_radio)
    minimize_radio = _settings_radio("最小化到托盘", "minimize_radio", not show_close_prompt and close_action == "minimize")
    tray_group.addWidget(minimize_radio)
    exit_radio = _settings_radio("退出程序", "exit_radio", not show_close_prompt and close_action == "exit")
    tray_group.addWidget(exit_radio)
    tray_layout.addLayout(tray_group)
    content_layout.addWidget(tray_section)
    content_layout.addStretch(1)

    scroll.setWidget(content)
    main_layout.addWidget(scroll, 1)

    button_row = QHBoxLayout()
    button_row.setSpacing(10)
    button_row.addStretch(1)
    cancel_button = _dialog_button("取消")
    cancel_button.clicked.connect(dialog.reject)
    save_button = _dialog_button("保存设置", primary=True)
    save_button.clicked.connect(lambda: main_window.save_settings(path_edit, dialog))
    button_row.addWidget(cancel_button)
    button_row.addWidget(save_button)
    main_layout.addLayout(button_row)

    dialog.setMinimumSize(780, 620)
    _position_dialog(dialog, top_ratio=0.28)
    _fade_in(dialog)
    return dialog


def build_about_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("关于")
    dialog.setWindowFlags(Qt.Window)
    dialog.setModal(True)

    _set_window_icon(dialog, main_window)

    dialog.setStyleSheet("""
        QDialog {
            background-color: #f4f6f8;
        }
    """)

    layout = QVBoxLayout(dialog)
    layout.setSpacing(14)
    layout.setContentsMargins(20, 20, 20, 20)

    main_frame = QFrame()
    main_frame.setProperty("card", "true")
    main_frame.setAttribute(Qt.WA_StyledBackground, True)
    main_layout = QVBoxLayout(main_frame)
    main_layout.setSpacing(10)
    main_layout.setContentsMargins(18, 18, 18, 18)

    title_label = QLabel("日文汉字 - 假名/罗马音转换工具")
    title_label.setProperty("title", "true")
    title_label.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(title_label)

    desc_label = QLabel("用于把日文汉字转换为假名和罗马音，方便临时查读音。")
    desc_label.setProperty("muted", "true")
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setWordWrap(True)
    main_layout.addWidget(desc_label)

    feature_label = QLabel("支持官方基底词典、用户词典增量、常用搭配与前后缀组合。")
    feature_label.setProperty("muted", "true")
    feature_label.setAlignment(Qt.AlignCenter)
    feature_label.setWordWrap(True)
    main_layout.addWidget(feature_label)

    try:
        image_path = _resolve_icon_path(main_window, "hantokana.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(image_label)
    except Exception as e:
        print(f"加载图片失败: {str(e)}")

    version_label = QLabel(f"版本: {APP_VERSION}")
    version_label.setAlignment(Qt.AlignCenter)
    version_label.setProperty("muted", "true")
    main_layout.addWidget(version_label)

    github_label = QLabel("github.com/kanocyann/hantokana")
    github_label.setAlignment(Qt.AlignCenter)
    github_label.setStyleSheet("color: #2f7d67;")
    github_label.setCursor(Qt.PointingHandCursor)
    github_label.mousePressEvent = lambda e: QDesktopServices.openUrl(QUrl("https://github.com/kanocyann/hantokana"))
    main_layout.addWidget(github_label)

    layout.addWidget(main_frame)

    ok_button = _dialog_button("确定", primary=True)
    ok_button.setFixedWidth(120)
    ok_button.clicked.connect(dialog.accept)
    layout.addWidget(ok_button, alignment=Qt.AlignCenter)

    dialog.setMinimumSize(460, 420)
    _position_dialog(dialog)
    _fade_in(dialog)
    return dialog


def build_close_choice_dialog(main_window):
    dialog = QDialog(main_window)
    dialog.setWindowTitle("关闭选项")
    dialog.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
    dialog.setFixedWidth(480)
    dialog.setStyleSheet("""
        QDialog {
            background-color: #f4f6f8;
        }
        QLabel[title="true"] {
            font-size: 18px;
            font-weight: 700;
            color: #111827;
        }
        QLabel[muted="true"] {
            color: #667085;
            font-size: 12px;
        }
        QLabel[option="true"] {
            color: #344054;
            font-size: 12px;
            line-height: 18px;
        }
        QFrame[card="true"] {
            background-color: white;
            border: 1px solid #dbe3ea;
            border-radius: 14px;
        }
        QFrame[hint="true"] {
            background-color: #f8fafb;
            border: 1px solid #e6ebf0;
            border-radius: 10px;
        }
    """)

    _set_window_icon(dialog, main_window)

    layout = QVBoxLayout(dialog)
    layout.setSpacing(12)
    layout.setContentsMargins(18, 18, 18, 18)

    card = QFrame()
    card.setProperty("card", "true")
    card.setAttribute(Qt.WA_StyledBackground, True)
    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(18, 16, 18, 16)
    card_layout.setSpacing(12)

    title_text = QLabel("关闭程序")
    title_text.setProperty("title", "true")
    card_layout.addWidget(title_text)

    message_label = QLabel("请选择关闭后的动作。")
    message_label.setWordWrap(True)
    message_label.setProperty("muted", "true")
    card_layout.addWidget(message_label)

    hint_frame = QFrame()
    hint_frame.setProperty("hint", "true")
    hint_frame.setAttribute(Qt.WA_StyledBackground, True)
    hint_layout = QVBoxLayout(hint_frame)
    hint_layout.setContentsMargins(12, 10, 12, 10)
    hint_layout.setSpacing(6)

    minimize_info = QLabel("最小化到托盘：程序保持运行，可从托盘重新打开。")
    minimize_info.setWordWrap(True)
    minimize_info.setProperty("option", "true")
    hint_layout.addWidget(minimize_info)

    exit_info = QLabel("退出程序：彻底关闭，下次使用需要重新启动。")
    exit_info.setWordWrap(True)
    exit_info.setProperty("option", "true")
    hint_layout.addWidget(exit_info)
    card_layout.addWidget(hint_frame)

    remember_choice_checkbox = CustomCheckBox("记住我的选择，下次无需询问")
    remember_choice_checkbox.setObjectName("remember_choice_checkbox")
    card_layout.addWidget(remember_choice_checkbox)

    layout.addWidget(card)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(12)
    minimize_button = _dialog_button("最小化到托盘", primary=True)
    minimize_button.setFixedHeight(40)
    minimize_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    minimize_button.clicked.connect(dialog.accept)
    exit_button = _dialog_button("退出程序")
    exit_button.setFixedHeight(40)
    exit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    exit_button.clicked.connect(lambda: dialog.done(2))
    button_layout.addWidget(minimize_button, 1)
    button_layout.addWidget(exit_button, 1)
    layout.addLayout(button_layout)

    _position_dialog(dialog)
    _fade_in(dialog)
    return dialog
