from pathlib import Path

import pytest
from PySide6.QtCore import Qt

from dcmd.app import (
    HotkeySignalBridge,
    _prepare_background_window,
    _queue_hotkey_activation,
    _sync_startup_setting,
)


class FakeStartupManager:
    def __init__(self, startup_path: Path) -> None:
        self.startup_path = startup_path

    def sync(
        self,
        enabled: bool,
        command: tuple[str, ...],
        working_directory: Path,
    ) -> None:
        raise PermissionError("denied")


def test_sync_startup_setting_ignores_startup_write_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("dcmd.app.load_startup_enabled", lambda path: True)
    monkeypatch.setattr("dcmd.app._settings_path", lambda: Path("config/settings.json"))
    monkeypatch.setattr("dcmd.app.startup_directory", lambda: Path("C:/Startup"))
    monkeypatch.setattr(
        "dcmd.app.startup_launch_command",
        lambda: ("C:/Python/python.exe", "-m", "dcmd.main"),
    )
    monkeypatch.setattr(
        "dcmd.app.startup_working_directory",
        lambda: Path("C:/DCMD/src"),
    )
    monkeypatch.setattr("dcmd.app.WindowsStartupManager", FakeStartupManager)

    _sync_startup_setting()


def test_queue_hotkey_activation_invokes_bridge_on_qt_thread(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_calls: list[tuple[object, str, object]] = []

    def fake_invoke_method(
        target: object,
        method_name: str,
        connection_type: object,
    ) -> None:
        captured_calls.append((target, method_name, connection_type))

    monkeypatch.setattr("dcmd.app.QMetaObject.invokeMethod", fake_invoke_method)
    bridge = HotkeySignalBridge()

    _queue_hotkey_activation(bridge)

    assert captured_calls == [
        (
            bridge,
            "notify_activated",
            Qt.ConnectionType.QueuedConnection,
        )
    ]


def test_prepare_background_window_initializes_hidden_window() -> None:
    calls: list[str] = []

    class FakeWindow:
        def show(self) -> None:
            calls.append("show")

        def hide(self) -> None:
            calls.append("hide")

    _prepare_background_window(FakeWindow())  # type: ignore[arg-type]

    assert calls == ["show", "hide"]
