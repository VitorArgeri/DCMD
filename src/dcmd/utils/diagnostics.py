import json
from datetime import datetime, timezone
from pathlib import Path


def diagnostics_log_path(base_path: Path | None = None) -> Path:
    """Return the local diagnostics log path.

    Example:
        >>> diagnostics_log_path(Path("C:/Temp")).name
    """
    root_path = base_path if base_path is not None else _default_log_root()
    return root_path / "dcmd.log"


def log_diagnostic_event(
    event: str,
    *,
    log_path: Path | None = None,
    **fields: object,
) -> None:
    """Append one JSON diagnostics event for packaged-runtime troubleshooting.

    Example:
        >>> log_diagnostic_event("startup")
    """
    target_path = diagnostics_log_path() if log_path is None else log_path
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **{key: _stringify_field(value) for key, value in fields.items()},
    }
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
    except OSError:
        return


def _default_log_root() -> Path:
    return Path.home() / "AppData" / "Local" / "DCMD" / "logs"


def _stringify_field(value: object) -> str | int | float | bool | None:
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return str(value)
