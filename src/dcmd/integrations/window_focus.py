from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


def show_and_focus_window(window: QWidget) -> None:
    """Show one window and move focus to it.

    Example:
        >>> isinstance(window, QWidget)
    """
    window.show()
    window.showNormal()
    window.setWindowState(window.windowState() & ~Qt.WindowState.WindowMinimized)
    window.raise_()
    window.activateWindow()
    window.setFocus(Qt.FocusReason.ActiveWindowFocusReason)
