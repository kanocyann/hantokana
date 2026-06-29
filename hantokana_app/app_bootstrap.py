import os

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QStyleFactory

from .ui_styles import APP_STYLE_SHEET


def _build_qt_argv(argv):
    qt_argv = list(argv)
    if os.name == "nt":
        has_platform_arg = any(
            arg in ("-platform", "--platform")
            or arg.startswith("-platform")
            or arg.startswith("--platform")
            for arg in qt_argv
        )
        if not has_platform_arg:
            qt_argv.extend(["-platform", "windows:dpiawareness=1"])
    return qt_argv


def create_application(argv):
    app = QApplication(_build_qt_argv(argv))
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setStyleSheet(APP_STYLE_SHEET)
    app.setFont(QFont("Microsoft YaHei UI", 9))
    return app
