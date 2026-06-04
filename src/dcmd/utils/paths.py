from pathlib import Path


def project_root() -> Path:
    """Return the repository root relative to the installed package.

    Example:
        >>> project_root().name
    """
    return Path(__file__).resolve().parents[3]
