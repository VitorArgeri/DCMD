import json
from pathlib import Path
from typing import cast

JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject = dict[str, JsonValue]


def load_json_object(path: Path) -> JsonObject:
    """Load a JSON object from disk with validation-friendly errors.

    Example:
        >>> load_json_object(Path("config/settings.json"))
    """
    _validate_json_suffix(path)
    raw_text = _read_text(path)
    payload = _parse_json(path, raw_text)
    if isinstance(payload, dict):
        return payload
    raise ValueError(
        f"Invalid JSON value={str(path)!r}; expected format='JSON object at top level'."
    )


def _validate_json_suffix(path: Path) -> None:
    if path.suffix.lower() == ".json":
        return
    raise ValueError(
        f"Invalid path value={str(path)!r}; expected format='path ending with .json'."
    )


def _read_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    raise FileNotFoundError(
        f"Invalid path value={str(path)!r}; expected format='existing JSON file path'."
    )


def _parse_json(path: Path, raw_text: str) -> JsonValue:
    try:
        payload = json.loads(raw_text)
        return cast(JsonValue, payload)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Invalid JSON "
            f"value={str(path)!r}; "
            "expected format='valid JSON object file'."
        ) from error
