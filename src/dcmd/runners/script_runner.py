import sys
from pathlib import Path
from typing import Protocol

from dcmd.core.command_registry import ScriptConfig
from dcmd.integrations.process_launcher import ProcessLauncher
from dcmd.utils.paths import scripts_directory


class ScriptRunner(Protocol):
    """Run an authorized script through a project-owned interface.

    Example:
        >>> isinstance(self, ScriptRunner)
    """

    def run_script(self, script: ScriptConfig) -> None:
        """Run one authorized script configuration.

        Example:
            >>> isinstance(script.identifier, str)
        """


class SecureScriptRunner:
    """Resolve and run only registered Python scripts inside scripts/."""

    def __init__(
        self,
        process_launcher: ProcessLauncher,
        allowed_directory: Path | None = None,
        python_path: Path | None = None,
    ) -> None:
        self._process_launcher = process_launcher
        self._allowed_directory = (
            scripts_directory() if allowed_directory is None else allowed_directory
        )
        self._python_path = Path(sys.executable) if python_path is None else python_path

    def run_script(self, script: ScriptConfig) -> None:
        """Run one authorized Python script after strict path validation.

        Example:
            >>> isinstance(script.file_name, str)
        """
        script_path = self._resolve_script_path(script.file_name)
        self._process_launcher.run_python(self._python_path, script_path)

    def _resolve_script_path(self, file_name: str) -> Path:
        self._validate_python_suffix(file_name)
        candidate = (self._allowed_directory / file_name).resolve()
        allowed_root = self._allowed_directory.resolve()
        self._validate_allowed_path(file_name, candidate, allowed_root)
        self._validate_existing_file(file_name, candidate)
        return candidate

    def _validate_python_suffix(self, file_name: str) -> None:
        if file_name.endswith(".py"):
            return
        raise ValueError(
            "Invalid script "
            f"value={file_name!r}; "
            "expected format='registered .py file inside scripts folder'."
        )

    def _validate_allowed_path(
        self,
        file_name: str,
        candidate: Path,
        allowed_root: Path,
    ) -> None:
        try:
            candidate.relative_to(allowed_root)
        except ValueError as error:
            raise ValueError(
                "Invalid script "
                f"value={file_name!r}; "
                "expected format='path inside scripts folder'."
            ) from error

    def _validate_existing_file(self, file_name: str, candidate: Path) -> None:
        if candidate.is_file():
            return
        raise ValueError(
            "Invalid script "
            f"value={file_name!r}; "
            "expected format='existing registered script file'."
        )
