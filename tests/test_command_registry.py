from pathlib import Path

import pytest

from dcmd.core.command_registry import CommandRegistry, build_command_registry, load_command_registry


def test_load_command_registry_returns_known_names() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    assert registry == CommandRegistry(
        command_names=frozenset({"yt", "vscode"}),
        search_engine_names=frozenset({"yt", "google", "github", "reddit"}),
        script_names=frozenset({"script-1"}),
        program_names=frozenset({"vscode"}),
    )


def test_build_command_registry_requires_commands_mapping() -> None:
    payload = {"commands": [], "search_engines": {}, "scripts": {}}
    with pytest.raises(ValueError, match="JSON object field"):
        build_command_registry(payload)
