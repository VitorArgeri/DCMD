from pathlib import Path

from dcmd.utils.json_loader import load_json_object

STARTUP_FILE_NAME = "DCMD.cmd"
WATCHDOG_FILE_NAME = "DCMD-watchdog.ps1"
RESTART_DELAY_SECONDS = 5


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
        watchdog_path = self.watchdog_path()
        watchdog_path.write_text(
            _watchdog_script(command, working_directory),
            encoding="utf-8",
        )
        target_path.write_text(_startup_script(watchdog_path), encoding="utf-8")
        return target_path

    def disable(self) -> None:
        """Remove the DCMD Startup-folder command file if it exists.

        Example:
            >>> isinstance(self._startup_path, Path)
        """
        target_path = self.entry_path()
        if target_path.exists():
            target_path.unlink()
        watchdog_path = self.watchdog_path()
        if watchdog_path.exists():
            watchdog_path.unlink()

    def entry_path(self) -> Path:
        """Return the DCMD Startup-folder launcher path.

        Example:
            >>> isinstance(self.entry_path(), Path)
        """
        return self._startup_path / STARTUP_FILE_NAME

    def watchdog_path(self) -> Path:
        """Return the hidden watchdog script path used by the Startup entry.

        Example:
            >>> isinstance(self.watchdog_path(), Path)
        """
        return self._startup_path / WATCHDOG_FILE_NAME


def _startup_script(watchdog_path: Path) -> str:
    return (
        "@echo off\n"
        "start \"\" powershell.exe "
        "-NoProfile "
        "-ExecutionPolicy Bypass "
        "-WindowStyle Hidden "
        f"-File {_quote_windows_argument(str(watchdog_path))}\n"
    )


def _watchdog_script(command: tuple[str, ...], working_directory: Path) -> str:
    executable_path = _quote_powershell_string(command[0])
    arguments = ", ".join(_quote_powershell_string(part) for part in command[1:])
    working_directory_path = _quote_powershell_string(str(working_directory))
    return "\n".join(
        (
            _watchdog_header(executable_path, arguments, working_directory_path),
            _watchdog_logging(),
            _watchdog_process_lookup(),
            _watchdog_loop(),
        )
    )


def _watchdog_header(
    executable_path: str,
    arguments: str,
    working_directory_path: str,
) -> str:
    return (
        "$ErrorActionPreference = 'Continue'\n"
        f"$executable = {executable_path}\n"
        f"$arguments = @({arguments})\n"
        f"$workingDirectory = {working_directory_path}"
    )


def _watchdog_logging() -> str:
    return (
        "$logPath = Join-Path $env:LOCALAPPDATA 'DCMD\\logs\\watchdog.log'\n"
        "function Write-WatchdogLog([string] $message) {\n"
        "    New-Item -ItemType Directory -Force -Path (Split-Path $logPath) |\n"
        "        Out-Null\n"
        "    Add-Content -Path $logPath -Value \"$(Get-Date -Format o) $message\"\n"
        "}"
    )


def _watchdog_process_lookup() -> str:
    return (
        "function Get-DcmdProcess {\n"
        "    Get-Process -Name 'DCMD' -ErrorAction SilentlyContinue |\n"
        "        Select-Object -First 1\n"
        "}"
    )


def _watchdog_loop() -> str:
    return (
        "while ($true) {\n"
        "    if ($null -eq (Get-DcmdProcess)) {\n"
        "        try {\n"
        "            $process = Start-Process "
        "-FilePath $executable "
        "-ArgumentList $arguments "
        "-WorkingDirectory $workingDirectory "
        "-PassThru\n"
        "            Write-WatchdogLog \"started pid=$($process.Id)\"\n"
        "        } catch {\n"
        "            Write-WatchdogLog \"failed $($_.Exception.Message)\"\n"
        "        }\n"
        "    }\n"
        f"    Start-Sleep -Seconds {RESTART_DELAY_SECONDS}\n"
        "}\n"
    )


def _quote_windows_argument(value: str) -> str:
    escaped_value = value.replace('"', '\\"')
    return f'"{escaped_value}"'


def _quote_powershell_string(value: str) -> str:
    escaped_value = value.replace("'", "''")
    return f"'{escaped_value}'"


def _appdata_path() -> Path:
    appdata = Path.home() / "AppData" / "Roaming"
    return appdata
