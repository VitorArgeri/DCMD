from pathlib import Path

import pytest

from dcmd.app import CommandSubmissionService
from dcmd.core.autocomplete import AutocompleteEngine
from dcmd.core.command_executor import ExecutionResult
from dcmd.core.command_registry import load_command_registry
from dcmd.core.history import InputHistory, SessionHistory
from dcmd.ui.main_window import MainWindow


class FakeEvent:
    def __init__(self) -> None:
        self.ignored = False

    def ignore(self) -> None:
        self.ignored = True


class FakeExecutor:
    def execute(self, command: object) -> object:
        raise AssertionError("Executor should not be used in this test.")


class SuccessExecutor:
    def execute(self, command: object) -> ExecutionResult:
        return ExecutionResult(success=True, message="Opening yt in Opera GX.")


@pytest.fixture(scope="module")
def app():
    from PySide6.QtWidgets import QApplication

    existing_app = QApplication.instance()
    if existing_app is not None:
        return existing_app
    created_app = QApplication([])
    yield created_app
    created_app.quit()


def test_close_event_hides_window_instead_of_exiting(app) -> None:
    registry = load_command_registry(Path("config/commands.json"))
    service = CommandSubmissionService(
        registry,
        FakeExecutor(),
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )
    window = MainWindow(service)
    event = FakeEvent()

    window.closeEvent(event)  # type: ignore[arg-type]

    assert event.ignored is True
    assert window.isVisible() is False


def test_toggle_visibility_hides_when_window_is_active(
    app,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = load_command_registry(Path("config/commands.json"))
    service = CommandSubmissionService(
        registry,
        FakeExecutor(),
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )
    window = MainWindow(service)
    calls: list[str] = []
    monkeypatch.setattr(window, "isVisible", lambda: True)
    monkeypatch.setattr(window, "isActiveWindow", lambda: True)
    monkeypatch.setattr(window, "hide", lambda: calls.append("hide"))

    window.toggle_visibility()

    assert calls == ["hide"]


def test_toggle_visibility_shows_when_window_is_hidden(
    app,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = load_command_registry(Path("config/commands.json"))
    service = CommandSubmissionService(
        registry,
        FakeExecutor(),
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )
    window = MainWindow(service)
    calls: list[MainWindow] = []
    monkeypatch.setattr(
        "dcmd.ui.main_window.show_and_focus_window",
        lambda target: calls.append(target),
    )

    window.toggle_visibility()

    assert calls == [window]


def test_submit_successful_command_hides_window(
    app,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = load_command_registry(Path("config/commands.json"))
    service = CommandSubmissionService(
        registry,
        SuccessExecutor(),
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )
    window = MainWindow(service)
    calls: list[str] = []
    monkeypatch.setattr(window, "hide", lambda: calls.append("hide"))

    window._submit_command("yt")

    assert calls == ["hide"]


def test_submit_cls_keeps_window_visible(
    app,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    registry = load_command_registry(Path("config/commands.json"))
    service = CommandSubmissionService(
        registry,
        FakeExecutor(),
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )
    window = MainWindow(service)
    calls: list[str] = []
    monkeypatch.setattr(window, "hide", lambda: calls.append("hide"))

    window._submit_command("cls")

    assert calls == []
