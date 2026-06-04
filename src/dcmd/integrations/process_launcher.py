from pathlib import Path
from subprocess import Popen
from typing import Protocol, Sequence


class CommandRunner(Protocol):
    """Start an external process without exposing subprocess to core logic.

    Example:
        >>> isinstance(self, CommandRunner)
    """

    def start(self, command: Sequence[str]) -> None:
        """Start one external command.

        Example:
            >>> isinstance(command, Sequence)
        """


class SubprocessCommandRunner:
    """Launch external processes with subprocess."""

    def start(self, command: Sequence[str]) -> None:
        """Start one external command without waiting for completion.

        Example:
            >>> isinstance(command, Sequence)
        """
        Popen(list(command))


class ProcessLauncher:
    """Project-owned wrapper for program and browser execution."""

    def __init__(self, runner: CommandRunner) -> None:
        self._runner = runner

    def open_url(self, browser_path: Path, url: str) -> None:
        """Open one URL with the configured browser executable.

        Example:
            >>> isinstance(url, str)
        """
        command = [str(browser_path), url]
        self._start(command, browser_path, "existing browser executable path")

    def open_program(self, program_path: Path) -> None:
        """Open one registered local program.

        Example:
            >>> isinstance(program_path, Path)
        """
        command = [str(program_path)]
        self._start(command, program_path, "existing program executable path")

    def run_python(self, python_path: Path, script_path: Path) -> None:
        """Run one authorized Python script.

        Example:
            >>> isinstance(script_path, Path)
        """
        command = [str(python_path), str(script_path)]
        self._start(command, python_path, "existing Python executable path")

    def _start(
        self,
        command: Sequence[str],
        executable_path: Path,
        expected_format: str,
    ) -> None:
        try:
            self._runner.start(command)
        except OSError as error:
            raise ValueError(
                "Invalid path "
                f"value={str(executable_path)!r}; "
                f"expected format={expected_format!r}."
            ) from error
