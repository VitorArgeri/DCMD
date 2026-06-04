import sys
from pathlib import Path


def runtime_root(
    frozen: bool | None = None,
    executable_path: Path | None = None,
    module_file: Path | None = None,
    meipass_path: Path | None = None,
) -> Path:
    """Return the active application root for source or packaged runs.

    Example:
        >>> isinstance(runtime_root(), Path)
    """
    is_frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    if is_frozen:
        bundled_root = getattr(sys, "_MEIPASS", None)
        if meipass_path is not None:
            bundled_root = meipass_path
        if bundled_root is not None:
            return Path(bundled_root).resolve()
        executable = (
            Path(sys.executable) if executable_path is None else executable_path
        )
        return executable.resolve().parent
    file_path = Path(__file__) if module_file is None else module_file
    return file_path.resolve().parents[3]


def project_root() -> Path:
    """Return the repository root relative to the installed package.

    Example:
        >>> project_root().name
    """
    return runtime_root(module_file=Path(__file__))


def scripts_directory() -> Path:
    """Return the repository scripts directory.

    Example:
        >>> scripts_directory().name
    """
    return project_root() / "scripts"


def config_directory() -> Path:
    """Return the runtime configuration directory.

    Example:
        >>> config_directory().name
    """
    return project_root() / "config"


def startup_launch_command(
    executable_path: Path | None = None,
    frozen: bool | None = None,
) -> tuple[str, ...]:
    """Return the startup command for source or packaged execution.

    Example:
        >>> isinstance(startup_launch_command(), tuple)
    """
    is_frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    if is_frozen:
        executable = (
            Path(sys.executable) if executable_path is None else executable_path
        )
        return (str(executable.resolve()),)
    python_path = _python_startup_executable(
        Path(sys.executable) if executable_path is None else executable_path
    )
    return (str(python_path), "-m", "dcmd.main")


def startup_working_directory(frozen: bool | None = None) -> Path:
    """Return the working directory used by the Startup-folder launcher.

    Example:
        >>> isinstance(startup_working_directory(), Path)
    """
    is_frozen = getattr(sys, "frozen", False) if frozen is None else frozen
    if is_frozen:
        return project_root()
    return project_root() / "src"


def _python_startup_executable(executable_path: Path) -> Path:
    pythonw_path = executable_path.with_name("pythonw.exe")
    if pythonw_path.exists():
        return pythonw_path
    return executable_path
