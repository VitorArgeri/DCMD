import ctypes
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

SW_RESTORE = 9
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2


def show_and_focus_window(window: QWidget) -> None:
    """Show one window and move focus to it.

    Example:
        >>> isinstance(window, QWidget)
    """
    window.show()
    window.showNormal()
    window.setWindowState(window.windowState() & ~Qt.WindowState.WindowMinimized)
    _focus_window_natively(window)
    window.raise_()
    window.activateWindow()
    window.setFocus(Qt.FocusReason.ActiveWindowFocusReason)


def _focus_window_natively(window: QWidget) -> None:
    if os.name != "nt":
        return
    hwnd = int(window.winId())
    if hwnd == 0:
        return
    user32 = ctypes.windll.user32
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    user32.SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    user32.SetForegroundWindow(hwnd)
