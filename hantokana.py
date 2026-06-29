import sys

from PySide6.QtCore import Qt

from hantokana_app.main_window import MainWindow
from hantokana_app.app_bootstrap import create_application
from hantokana_app.ui_shared import SingleInstanceApplication


def main():
    app = create_application(sys.argv)
    window_holder = {"window": None}

    def activate_window():
        window = window_holder["window"]
        if window is None:
            return
        window.setWindowState(window.windowState() & ~Qt.WindowMinimized)
        window.show()
        window.raise_()
        window.activateWindow()

    single_app = SingleInstanceApplication("hantokana-single-instance", activate_window)
    if not single_app.ensure_single_instance():
        print("应用程序已经在运行")
        return 0

    window_holder["window"] = MainWindow()
    window_holder["window"].show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
