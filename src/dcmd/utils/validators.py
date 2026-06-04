from dcmd.utils.json_loader import JsonObject


def require_mapping_keys(payload: JsonObject, key: str) -> JsonObject:
    """Return a mapping value for a required configuration key.

    Example:
        >>> require_mapping_keys({"commands": {}}, "commands")
    """
    value = payload.get(key)
    if isinstance(value, dict):
        return value
    raise ValueError(
        f"Invalid configuration value={key!r}; expected format='JSON object field'."
    )


def validate_known_identifier(
    value: str,
    known_values: frozenset[str],
    expected_format: str,
) -> str | None:
    """Validate that an identifier exists in a configured set.

    Example:
        >>> validate_known_identifier("yt", frozenset({"yt"}), "registered command")
    """
    normalized_value = value.strip()
    if normalized_value in known_values:
        return None
    return (
        f"Invalid identifier value={value!r}; expected format={expected_format!r}."
    )
