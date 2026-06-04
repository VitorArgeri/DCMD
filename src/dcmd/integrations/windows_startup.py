from pathlib import Path

from dcmd.utils.json_loader import load_json_object

STARTUP_FILE_NAME = "DCMD.cmd"


def load_startup_enabled(path: Path) -> bool:
    """Return whether Startup-folder integration is enabled in settings.

    Example:
        >>> isinstance(load_startup_enabled(path), bool)
    """
    payload = load_json_object(path)
    startup = payload.get("startup")
    if not isinstance(startup, dict):
        return False
    enabled = startup.get("enabled")
    return isinstance(enabled, bool) and enabled


def startup_directory(appdata_path: Path | None = None) -> Path:
    """Return the Windows Startup-folder path.

    Example:
        >>> isinstance(startup_directory(Path('C:/Users/test/AppData/Roaming')), Path)
    """
    base_path = appdata_path if appdata_path is not None else _appdata_path()
    return (
        base_path
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )


class WindowsStartupManager:
    """Create or remove the DCMD Startup-folder launcher file."""

    def __init__(self, startup_path: Path) -> None:
        self._startup_path = startup_path

    def sync(
        self,
        enabled: bool,
        command: tuple[str, ...],
        working_directory: Path,
    ) -> None:
        """Apply the configured startup state.

        Example:
            >>> isinstance(enabled, bool)
        """
        if enabled:
            self.enable(command, working_directory)
            return
        self.disable()

    def enable(self, command: tuple[str, ...], working_directory: Path) -> Path:
        """Create the Startup-folder command file for DCMD.

        Example:
            >>> isinstance(command, tuple)
        """
        self._startup_path.mkdir(parents=True, exist_ok=True)
        target_path = self.entry_path()
        target_path.write_text(
            _startup_script(command, working_directory),
            encoding="utf-8",
        )
        return target_path

    def disable(self) -> None:
        """Remove the DCMD Startup-folder command file if it exists.

        Example:
            >>> isinstance(self._startup_path, Path)
        """
        target_path = self.entry_path()
        if target_path.exists():
            target_path.unlink()

    def entry_path(self) -> Path:
        """Return the DCMD Startup-folder launcher path.

        Example:
            >>> isinstance(self.entry_path(), Path)
        """
        return self._startup_path / STARTUP_FILE_NAME


def _startup_script(command: tuple[str, ...], working_directory: Path) -> str:
    quoted_command = " ".join(_quote_windows_argument(part) for part in command)
    return (
        "@echo off\n"
        f'cd /d "{working_directory}"\n'
        f"{quoted_command}\n"
    )


def _quote_windows_argument(value: str) -> str:
    escaped_value = value.replace('"', '\\"')
    return f'"{escaped_value}"'


def _appdata_path() -> Path:
    appdata = Path.home() / "AppData" / "Roaming"
    return appdata
