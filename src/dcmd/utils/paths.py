from pathlib import Path


def project_root() -> Path:
    """Return the repository root relative to the installed package.

    Example:
        >>> project_root().name
    """
    return Path(__file__).resolve().parents[3]


def scripts_directory() -> Path:
    """Return the repository scripts directory.

    Example:
        >>> scripts_directory().name
    """
    return project_root() / "scripts"
