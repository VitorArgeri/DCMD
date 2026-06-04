from pathlib import Path

from dcmd.core.command_parser import (
    DirectCommand,
    ParsedError,
    ProgramCommand,
    ScriptCommand,
    SearchCommand,
    parse_command,
)
from dcmd.core.command_registry import load_command_registry


def test_parse_direct_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("yt", registry)
    assert result == DirectCommand(identifier="yt")


def test_parse_search_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("search yt gameplays", registry)
    assert result == SearchCommand(engine="yt", query="gameplays")


def test_parse_script_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("exec script-1", registry)
    assert result == ScriptCommand(identifier="script-1")


def test_parse_program_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("open vscode", registry)
    assert result == ProgramCommand(identifier="vscode")


def test_reject_empty_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("   ", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='non-empty command text'" in result.message


def test_reject_malformed_search_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("search yt", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='search <engine> <query>'" in result.message


def test_reject_malformed_script_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("exec", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='exec <script-id>'" in result.message


def test_reject_malformed_program_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("open", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='open <program-id>'" in result.message


def test_reject_unknown_direct_command() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("unknown", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='registered command'" in result.message


def test_reject_unknown_search_engine() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("search missing gameplays", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='registered search engine'" in result.message


def test_reject_unknown_script_identifier() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("exec missing", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='registered script identifier'" in result.message


def test_reject_unknown_program_identifier() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    result = parse_command("open missing", registry)
    assert isinstance(result, ParsedError)
    assert "expected format='registered program identifier'" in result.message
