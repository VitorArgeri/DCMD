from pathlib import Path

from dcmd.integrations.global_hotkey import (
    DEFAULT_HOTKEY,
    load_hotkey_binding,
    parse_hotkey,
)


def test_load_hotkey_binding_returns_default_when_missing(tmp_path: Path) -> None:
    payload_path = tmp_path / "settings.json"
    payload_path.write_text("{}", encoding="utf-8")
    binding = load_hotkey_binding(payload_path)
    assert binding.label == DEFAULT_HOTKEY


def test_parse_hotkey_returns_windows_binding() -> None:
    binding = parse_hotkey("ctrl+shift+j")
    assert binding.label == "ctrl+shift+j"
    assert binding.modifiers > 0
    assert binding.virtual_key == ord("J")
