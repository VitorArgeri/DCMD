from pathlib import Path

from dcmd.core.autocomplete import AutocompleteEngine
from dcmd.core.command_registry import load_command_registry


def test_autocomplete_returns_direct_command_matches() -> None:
    engine = build_engine()
    assert engine.suggestions("y") == ("yt",)


def test_autocomplete_returns_search_command_matches() -> None:
    engine = build_engine()
    assert engine.suggestions("search g") == ("search github", "search google")


def test_autocomplete_returns_program_command_matches() -> None:
    engine = build_engine()
    assert engine.suggestions("open v") == ("open vscode",)


def test_autocomplete_returns_script_command_matches() -> None:
    engine = build_engine()
    assert engine.suggestions("exec s") == ("exec script-1",)


def test_autocomplete_completes_single_search_with_trailing_space() -> None:
    engine = build_engine()
    result = engine.complete("search y")
    assert result.applied is True
    assert result.text == "search yt "


def test_autocomplete_returns_multiple_suggestions_without_applying() -> None:
    engine = build_engine()
    result = engine.complete("search g")
    assert result.applied is False
    assert result.suggestions == ("search github", "search google")


def build_engine() -> AutocompleteEngine:
    registry = load_command_registry(Path("config/commands.json"))
    return AutocompleteEngine(registry)
