from pathlib import Path

import pytest

from dcmd.utils.json_loader import load_json_object


def test_load_json_object_returns_mapping(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text('{"name": "dcmd"}', encoding="utf-8")
    result = load_json_object(config_path)
    assert result == {"name": "dcmd"}


def test_load_json_object_rejects_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError, match="existing JSON file path"):
        load_json_object(missing_path)


def test_load_json_object_rejects_invalid_json(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text("{invalid", encoding="utf-8")
    with pytest.raises(ValueError, match="valid JSON object file"):
        load_json_object(config_path)


def test_load_json_object_rejects_non_object_payload(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text('["dcmd"]', encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object at top level"):
        load_json_object(config_path)


def test_load_json_object_rejects_non_json_suffix(tmp_path: Path) -> None:
    config_path = tmp_path / "config.txt"
    config_path.write_text('{"name": "dcmd"}', encoding="utf-8")
    with pytest.raises(ValueError, match="path ending with .json"):
        load_json_object(config_path)
