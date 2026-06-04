from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from dcmd.core.autocomplete import AutocompleteEngine
from dcmd.core.command_executor import CommandExecutor, ExecutionResult
from dcmd.core.command_parser import ParsedError, parse_command
from dcmd.core.command_registry import CommandRegistry, load_command_registry
from dcmd.core.history import InputHistory, SessionHistory
from dcmd.integrations.global_hotkey import WindowsGlobalHotkey, load_hotkey_binding
from dcmd.integrations.process_launcher import ProcessLauncher, SubprocessCommandRunner
from dcmd.integrations.single_instance import SingleWindowFactory
from dcmd.runners.script_runner import SecureScriptRunner
from dcmd.utils.paths import project_root

PROMPT_TEXT = "What command do you want to use?"


@dataclass(frozen=True)
class SubmissionOutcome:
    accepted: bool
    message: str
    success: bool


class HotkeySignalBridge(QObject):
    activated = Signal()


class CommandSubmissionService:
    """Parse, execute, and record one launcher command at a time.

    Example:
        >>> isinstance(CommandSubmissionService, type)
    """

    def __init__(
        self,
        registry: CommandRegistry,
        executor: CommandExecutor,
        history: SessionHistory,
        input_history: InputHistory,
        autocomplete: AutocompleteEngine,
    ) -> None:
        self._registry = registry
        self._executor = executor
        self._history = history
        self._input_history = input_history
        self._autocomplete = autocomplete

    @property
    def history(self) -> SessionHistory:
        return self._history

    @property
    def input_history(self) -> InputHistory:
        return self._input_history

    @property
    def autocomplete(self) -> AutocompleteEngine:
        return self._autocomplete

    def submit(self, text: str) -> SubmissionOutcome:
        """Submit one command line and record history entries.

        Example:
            >>> isinstance(text, str)
        """
        command_text = text.strip()
        if not command_text:
            return SubmissionOutcome(accepted=False, message="", success=False)
        self._input_history.record(command_text)
        self._history.add_command(command_text)
        parsed = parse_command(command_text, self._registry)
        result = self._executor.execute(parsed)
        message = _display_message(parsed, result)
        self._history.add_result(message, is_error=not result.success)
        return SubmissionOutcome(accepted=True, message=message, success=result.success)


def build_command_service() -> CommandSubmissionService:
    """Create the default command submission service for the launcher UI.

    Example:
        >>> isinstance(build_command_service, object)
    """
    registry = load_command_registry(_commands_path())
    launcher = ProcessLauncher(SubprocessCommandRunner())
    executor = CommandExecutor(registry, launcher, SecureScriptRunner(launcher))
    return CommandSubmissionService(
        registry,
        executor,
        SessionHistory(),
        InputHistory(),
        AutocompleteEngine(registry),
    )


def run_application() -> int:
    """Start the graphical launcher application.

    Example:
        >>> isinstance(run_application, object)
    """
    from PySide6.QtWidgets import QApplication

    from dcmd.ui.main_window import MainWindow

    app = QApplication([])
    service = build_command_service()
    window_factory = SingleWindowFactory[MainWindow]()
    hotkey_bridge = HotkeySignalBridge()
    window = window_factory.get_or_create(lambda: MainWindow(service))
    hotkey_bridge.activated.connect(window.show_and_focus)
    listener = _build_hotkey_listener()
    _start_hotkey_listener(listener, hotkey_bridge)
    window.show_and_focus()
    exit_code = app.exec()
    listener.stop()
    return exit_code


def _commands_path() -> Path:
    return project_root() / "config" / "commands.json"


def _settings_path() -> Path:
    return project_root() / "config" / "settings.json"


def _build_hotkey_listener() -> WindowsGlobalHotkey:
    binding = load_hotkey_binding(_settings_path())
    return WindowsGlobalHotkey(binding)


def _start_hotkey_listener(
    listener: WindowsGlobalHotkey,
    bridge: HotkeySignalBridge,
) -> None:
    try:
        listener.start(bridge.activated.emit)
    except OSError:
        return


def _display_message(parsed: object, result: ExecutionResult) -> str:
    if isinstance(parsed, ParsedError):
        return "Unknown command."
    if result.success:
        return result.message
    return result.message
