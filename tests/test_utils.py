from pathlib import Path

import pytest

from dcmd.utils.paths import project_root, scripts_directory
from dcmd.utils.validators import require_mapping_keys, require_string, validate_known_identifier


def test_project_root_returns_repository_path() -> None:
    expected_path = Path(__file__).resolve().parents[1]
    assert project_root() == expected_path


def test_require_mapping_keys_returns_mapping() -> None:
    payload = {"commands": {"yt": {"type": "open_url"}}}
    result = require_mapping_keys(payload, "commands")
    assert result == {"yt": {"type": "open_url"}}


def test_validate_known_identifier_accepts_known_value() -> None:
    result = validate_known_identifier("yt", frozenset({"yt"}), "registered command")
    assert result is None


def test_validate_known_identifier_rejects_unknown_value() -> None:
    result = validate_known_identifier("bad", frozenset({"yt"}), "registered command")
    assert result == "Invalid identifier value='bad'; expected format='registered command'."


def test_require_mapping_keys_rejects_non_mapping() -> None:
    payload = {"commands": []}
    with pytest.raises(ValueError, match="JSON object field"):
        require_mapping_keys(payload, "commands")


def test_require_string_returns_string() -> None:
    payload = {"name": "dcmd"}
    assert require_string(payload, "name") == "dcmd"


def test_scripts_directory_uses_project_root() -> None:
    assert scripts_directory() == project_root() / "scripts"
