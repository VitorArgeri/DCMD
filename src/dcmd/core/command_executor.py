from dataclasses import dataclass
from urllib.parse import quote_plus

from dcmd.core.command_parser import (
    DirectCommand,
    ParsedCommand,
    ParsedError,
    ProgramCommand,
    ScriptCommand,
    SearchCommand,
)
from dcmd.core.command_registry import (
    CommandRegistry,
    OpenProgramCommandConfig,
    OpenUrlCommandConfig,
    ScriptConfig,
    SearchEngineConfig,
)
from dcmd.integrations.process_launcher import ProcessLauncher
from dcmd.runners.script_runner import ScriptRunner


@dataclass(frozen=True)
class ExecutionResult:
    success: bool
    message: str


class CommandExecutor:
    """Execute parsed commands through controlled project-owned interfaces.

    Example:
        >>> isinstance(CommandExecutor, type)
    """

    def __init__(
        self,
        registry: CommandRegistry,
        process_launcher: ProcessLauncher,
        script_runner: ScriptRunner,
    ) -> None:
        self._registry = registry
        self._process_launcher = process_launcher
        self._script_runner = script_runner

    def execute(self, command: ParsedCommand | ParsedError) -> ExecutionResult:
        """Execute one parsed command and return a user-facing result.

        Example:
            >>> isinstance(self.execute, object)
        """
        if isinstance(command, ParsedError):
            return ExecutionResult(success=False, message=command.message)
        try:
            return self._dispatch(command)
        except ValueError as error:
            return ExecutionResult(success=False, message=str(error))

    def _dispatch(self, command: ParsedCommand) -> ExecutionResult:
        if isinstance(command, DirectCommand):
            return self._execute_registered_command(command.identifier)
        if isinstance(command, SearchCommand):
            return self._execute_search(command)
        if isinstance(command, ScriptCommand):
            return self._execute_script(command.identifier)
        return self._execute_program(command)

    def _execute_registered_command(self, identifier: str) -> ExecutionResult:
        command = self._get_registered_command(identifier)
        if isinstance(command, OpenUrlCommandConfig):
            return self._open_url_command(command)
        return self._open_program_command(command)

    def _open_url_command(self, command: OpenUrlCommandConfig) -> ExecutionResult:
        self._process_launcher.open_url(self._registry.browser.path, command.url)
        message = f"Opening {command.identifier} in {self._registry.browser.name}."
        return ExecutionResult(success=True, message=message)

    def _open_program_command(
        self,
        command: OpenProgramCommandConfig,
    ) -> ExecutionResult:
        self._process_launcher.open_program(command.path)
        message = f"Opening {command.identifier}."
        return ExecutionResult(success=True, message=message)

    def _execute_search(self, command: SearchCommand) -> ExecutionResult:
        engine = self._get_search_engine(command.engine)
        target_url = engine.url_template.format(query=quote_plus(command.query))
        self._process_launcher.open_url(self._registry.browser.path, target_url)
        message = f"Searching {engine.name} for {command.query!r}."
        return ExecutionResult(success=True, message=message)

    def _execute_script(self, identifier: str) -> ExecutionResult:
        script = self._get_script(identifier)
        self._script_runner.run_script(script)
        message = f"Running script {script.identifier}."
        return ExecutionResult(success=True, message=message)

    def _execute_program(self, command: ProgramCommand) -> ExecutionResult:
        registered_command = self._get_registered_command(command.identifier)
        if isinstance(registered_command, OpenProgramCommandConfig):
            return self._open_program_command(registered_command)
        raise ValueError(
            f"Invalid identifier value={command.identifier!r}; expected format='registered program identifier'."
        )

    def _get_registered_command(
        self,
        identifier: str,
    ) -> OpenUrlCommandConfig | OpenProgramCommandConfig:
        command = self._registry.commands.get(identifier)
        if command is not None:
            return command
        raise ValueError(
            f"Invalid identifier value={identifier!r}; expected format='registered command'."
        )

    def _get_search_engine(self, identifier: str) -> SearchEngineConfig:
        engine = self._registry.search_engines.get(identifier)
        if engine is not None:
            return engine
        raise ValueError(
            f"Invalid identifier value={identifier!r}; expected format='registered search engine'."
        )

    def _get_script(self, identifier: str) -> ScriptConfig:
        script = self._registry.scripts.get(identifier)
        if script is not None:
            return script
        raise ValueError(
            f"Invalid identifier value={identifier!r}; expected format='registered script identifier'."
        )
