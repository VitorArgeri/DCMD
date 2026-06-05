from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from PySide6.QtCore import QMetaObject, QObject, Qt, Signal, Slot
from PySide6.QtWidgets import QApplication

from dcmd.core.autocomplete import AutocompleteEngine
from dcmd.core.command_executor import CommandExecutor, ExecutionResult
from dcmd.core.command_parser import ParsedError, parse_command
from dcmd.core.command_registry import CommandRegistry, load_command_registry
from dcmd.core.history import InputHistory, SessionHistory
from dcmd.integrations.global_hotkey import WindowsGlobalHotkey, load_hotkey_binding
from dcmd.integrations.process_launcher import ProcessLauncher, SubprocessCommandRunner
from dcmd.integrations.single_instance import (
    SingleInstanceGuard,
    SingleWindowFactory,
    WindowsNamedMutex,
)
from dcmd.integrations.windows_startup import (
    WindowsStartupManager,
    load_startup_enabled,
    startup_directory,
)
from dcmd.runners.script_runner import SecureScriptRunner
from dcmd.utils.diagnostics import log_diagnostic_event
from dcmd.utils.paths import (
    config_directory,
    startup_launch_command,
    startup_working_directory,
)

PROMPT_TEXT = "What command do you want to use?"


class LauncherWindow(Protocol):
    """Window behavior needed by the application bootstrap."""

    def show(self) -> None:
        """Show the window."""

    def hide(self) -> None:
        """Hide the window."""

    def show_and_focus(self) -> None:
        """Show the window and move focus to it."""

    def toggle_visibility(self) -> None:
        """Toggle the visible launcher state."""


@dataclass(frozen=True)
class SubmissionOutcome:
    accepted: bool
    message: str
    success: bool
    hide_window: bool = False


@dataclass(frozen=True)
class ApplicationRuntime:
    window: LauncherWindow
    hotkey_bridge: "HotkeySignalBridge"
    hotkey_listener: WindowsGlobalHotkey


class HotkeySignalBridge(QObject):
    activated = Signal()

    @Slot()
    def notify_activated(self) -> None:
        self.activated.emit()


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
        if command_text.lower() == "cls":
            self._history.clear()
            return SubmissionOutcome(accepted=True, message="", success=True)
        self._input_history.record(command_text)
        self._history.add_command(command_text)
        parsed = parse_command(command_text, self._registry)
        result = self._executor.execute(parsed)
        message = _display_message(parsed, result)
        self._history.add_result(message, is_error=not result.success)
        return SubmissionOutcome(
            accepted=True,
            message=message,
            success=result.success,
            hide_window=result.success,
        )


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


def run_application(show_on_startup: bool = True) -> int:
    """Start the graphical launcher application.

    Example:
        >>> isinstance(run_application, object)
    """
    log_diagnostic_event("run_application.start", show_on_startup=show_on_startup)
    instance_guard = SingleInstanceGuard(WindowsNamedMutex("DCMD"))
    if not instance_guard.acquire():
        log_diagnostic_event("run_application.instance_exists")
        return 0
    app = _create_qt_application()
    try:
        runtime = _build_application_runtime(show_on_startup)
        return _run_qt_event_loop(app, runtime)
    except Exception as error:
        log_diagnostic_event("run_application.exception", error=repr(error))
        raise
    finally:
        instance_guard.release()


def _create_qt_application() -> QApplication:
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    return app


def _build_application_runtime(show_on_startup: bool) -> ApplicationRuntime:
    window = _build_launcher_window()
    hotkey_bridge = HotkeySignalBridge()
    listener = _build_hotkey_listener()
    hotkey_bridge.activated.connect(window.toggle_visibility)
    _sync_startup_setting()
    _start_hotkey_listener(listener, hotkey_bridge)
    _show_initial_window_state(window, show_on_startup)
    return ApplicationRuntime(window, hotkey_bridge, listener)


def _build_launcher_window() -> LauncherWindow:
    from dcmd.ui.main_window import MainWindow

    service = build_command_service()
    window_factory = SingleWindowFactory[MainWindow]()
    return window_factory.get_or_create(lambda: MainWindow(service))


def _show_initial_window_state(
    window: LauncherWindow,
    show_on_startup: bool,
) -> None:
    if show_on_startup:
        window.show_and_focus()
        return
    _prepare_background_window(window)


def _run_qt_event_loop(
    app: QApplication,
    runtime: ApplicationRuntime,
) -> int:
    log_diagnostic_event("run_application.exec_enter")
    exit_code = app.exec()
    log_diagnostic_event("run_application.exec_exit", exit_code=exit_code)
    runtime.hotkey_listener.stop()
    return exit_code


def _commands_path() -> Path:
    return config_directory() / "commands.json"


def _settings_path() -> Path:
    return config_directory() / "settings.json"


def _build_hotkey_listener() -> WindowsGlobalHotkey:
    binding = load_hotkey_binding(_settings_path())
    return WindowsGlobalHotkey(binding)


def _start_hotkey_listener(
    listener: WindowsGlobalHotkey,
    bridge: HotkeySignalBridge,
) -> None:
    try:
        listener.start(lambda: _queue_hotkey_activation(bridge))
    except OSError as error:
        log_diagnostic_event("hotkey.listener_error", error=repr(error))
        return


def _queue_hotkey_activation(bridge: HotkeySignalBridge) -> None:
    QMetaObject.invokeMethod(
        bridge,
        "notify_activated",
        Qt.ConnectionType.QueuedConnection,
    )


def _prepare_background_window(window: LauncherWindow) -> None:
    window.show()
    window.hide()
    log_diagnostic_event("window.background_prepared")


def _sync_startup_setting() -> None:
    startup_enabled = load_startup_enabled(_settings_path())
    manager = WindowsStartupManager(startup_directory())
    try:
        manager.sync(
            startup_enabled,
            startup_launch_command(),
            startup_working_directory(),
        )
    except OSError as error:
        log_diagnostic_event("startup.sync_error", error=repr(error))
        return


def _display_message(parsed: object, result: ExecutionResult) -> str:
    if isinstance(parsed, ParsedError):
        return "Unknown command."
    if result.success:
        return result.message
    return result.message
