from pathlib import Path

from dcmd.app import CommandSubmissionService
from dcmd.core.autocomplete import AutocompleteEngine
from dcmd.core.command_executor import ExecutionResult
from dcmd.core.command_registry import CommandRegistry, load_command_registry
from dcmd.core.history import InputHistory, SessionHistory


class FakeExecutor:
    def __init__(self) -> None:
        self.calls: list[object] = []

    def execute(self, command: object) -> ExecutionResult:
        self.calls.append(command)
        return ExecutionResult(success=True, message="Opening yt in Opera GX.")


class FakeErrorExecutor:
    def __init__(self) -> None:
        self.calls: list[object] = []

    def execute(self, command: object) -> ExecutionResult:
        self.calls.append(command)
        return ExecutionResult(success=False, message="Invalid command.")


def test_submit_records_command_and_result() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    executor = FakeExecutor()
    service = build_service(registry, executor)
    outcome = service.submit("yt")
    assert outcome.accepted is True
    assert outcome.success is True
    assert outcome.message == "Opening yt in Opera GX."
    assert outcome.hide_window is True
    assert len(executor.calls) == 1
    entries = service.history.entries()
    assert entries[0].message == "yt"
    assert entries[1].message == "Opening yt in Opera GX."


def test_submit_ignores_empty_input() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    executor = FakeExecutor()
    service = build_service(registry, executor)
    outcome = service.submit("   ")
    assert outcome.accepted is False
    assert service.history.entries() == ()
    assert executor.calls == []


def test_submit_rewrites_parse_error_for_ui() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    executor = FakeErrorExecutor()
    service = build_service(registry, executor)
    outcome = service.submit("unknown")
    assert outcome.accepted is True
    assert outcome.success is False
    assert outcome.message == "Unknown command."
    entries = service.history.entries()
    assert entries[0].message == "unknown"
    assert entries[1].message == "Unknown command."
    assert entries[1].tone == "error"


def test_submit_cls_clears_visible_history_without_running_executor() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    executor = FakeExecutor()
    service = build_service(registry, executor)
    service.submit("yt")

    outcome = service.submit("cls")

    assert outcome.accepted is True
    assert outcome.success is True
    assert outcome.message == ""
    assert outcome.hide_window is False
    assert service.history.entries() == ()
    assert len(executor.calls) == 1


def build_service(
    registry: CommandRegistry,
    executor: FakeExecutor | FakeErrorExecutor,
) -> CommandSubmissionService:
    return CommandSubmissionService(
        registry,
        executor,
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )
