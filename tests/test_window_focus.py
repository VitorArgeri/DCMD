import pytest
from PySide6.QtCore import Qt

from dcmd.integrations.window_focus import show_and_focus_window


class FakeWindow:
    def __init__(self) -> None:
        self.calls: list[str] = []
        self.focus_reason: Qt.FocusReason | None = None
        self.state = Qt.WindowState.WindowMinimized

    def show(self) -> None:
        self.calls.append("show")

    def showNormal(self) -> None:
        self.calls.append("showNormal")

    def windowState(self) -> Qt.WindowState:
        return self.state

    def setWindowState(self, state: Qt.WindowState) -> None:
        self.calls.append("setWindowState")
        self.state = state

    def raise_(self) -> None:
        self.calls.append("raise")

    def activateWindow(self) -> None:
        self.calls.append("activateWindow")

    def setFocus(self, reason: Qt.FocusReason) -> None:
        self.calls.append("setFocus")
        self.focus_reason = reason


def test_show_and_focus_window_restores_and_focuses_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_window = FakeWindow()
    native_calls: list[FakeWindow] = []
    monkeypatch.setattr(
        "dcmd.integrations.window_focus._focus_window_natively",
        lambda window: native_calls.append(window),
    )

    show_and_focus_window(fake_window)  # type: ignore[arg-type]

    assert fake_window.calls == [
        "show",
        "showNormal",
        "setWindowState",
        "raise",
        "activateWindow",
        "setFocus",
    ]
    assert fake_window.state == Qt.WindowState.WindowNoState
    assert fake_window.focus_reason == Qt.FocusReason.ActiveWindowFocusReason
    assert native_calls == [fake_window]
