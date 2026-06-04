from dataclasses import dataclass
from pathlib import Path

from dcmd.core.command_executor import CommandExecutor, ExecutionResult
from dcmd.core.command_parser import ParsedError, parse_command
from dcmd.core.command_registry import CommandRegistry, load_command_registry
from dcmd.core.history import SessionHistory
from dcmd.integrations.process_launcher import ProcessLauncher, SubprocessCommandRunner
from dcmd.runners.script_runner import SecureScriptRunner
from dcmd.utils.paths import project_root


PROMPT_TEXT = "What command do you want to use?"


@dataclass(frozen=True)
class SubmissionOutcome:
    accepted: bool
    message: str
    success: bool


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
    ) -> None:
        self._registry = registry
        self._executor = executor
        self._history = history

    @property
    def history(self) -> SessionHistory:
        return self._history

    def submit(self, text: str) -> SubmissionOutcome:
        """Submit one command line and record history entries.

        Example:
            >>> isinstance(text, str)
        """
        command_text = text.strip()
        if not command_text:
            return SubmissionOutcome(accepted=False, message="", success=False)
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
    return CommandSubmissionService(registry, executor, SessionHistory())


def run_application() -> int:
    """Start the graphical launcher application.

    Example:
        >>> isinstance(run_application, object)
    """
    from PySide6.QtWidgets import QApplication

    from dcmd.ui.main_window import MainWindow

    app = QApplication([])
    window = MainWindow(build_command_service())
    window.show()
    return app.exec()


def _commands_path() -> Path:
    return project_root() / "config" / "commands.json"


def _display_message(parsed: object, result: ExecutionResult) -> str:
    if isinstance(parsed, ParsedError):
        return "Unknown command."
    if result.success:
        return result.message
    return result.message
