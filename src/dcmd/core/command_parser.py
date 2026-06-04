from dataclasses import dataclass

from dcmd.core.command_registry import CommandRegistry
from dcmd.utils.validators import validate_known_identifier


@dataclass(frozen=True)
class DirectCommand:
    identifier: str
    kind: str = "direct"


@dataclass(frozen=True)
class SearchCommand:
    engine: str
    query: str
    identifier: str = "search"
    kind: str = "search"


@dataclass(frozen=True)
class ScriptCommand:
    identifier: str
    kind: str = "script"


@dataclass(frozen=True)
class ProgramCommand:
    identifier: str
    kind: str = "program"


@dataclass(frozen=True)
class ParsedError:
    message: str
    value: str
    kind: str = "error"


ParsedCommand = DirectCommand | SearchCommand | ScriptCommand | ProgramCommand


def parse_command(text: str, registry: CommandRegistry) -> ParsedCommand | ParsedError:
    """Parse user input into a typed command result.

    Example:
        >>> registry = CommandRegistry({"yt"}, {"yt"}, {"script-1"}, {"vscode"})
        >>> parse_command("yt", registry)
    """
    normalized_text = text.strip()
    if not normalized_text:
        return _invalid_command(text, "non-empty command text")
    if _has_command_keyword(normalized_text, "search"):
        return _parse_search_command(normalized_text, registry)
    if _has_command_keyword(normalized_text, "exec"):
        return _parse_script_command(normalized_text, registry)
    if _has_command_keyword(normalized_text, "open"):
        return _parse_program_command(normalized_text, registry)
    return _parse_direct_command(normalized_text, registry)


def _has_command_keyword(text: str, keyword: str) -> bool:
    return text == keyword or text.startswith(f"{keyword} ")


def _parse_direct_command(
    text: str,
    registry: CommandRegistry,
) -> DirectCommand | ParsedError:
    message = validate_known_identifier(text, registry.command_names, "registered command")
    if message is not None:
        return ParsedError(message=message, value=text)
    return DirectCommand(identifier=text)


def _parse_search_command(
    text: str,
    registry: CommandRegistry,
) -> SearchCommand | ParsedError:
    parts = text.split(maxsplit=2)
    if len(parts) < 3:
        return _invalid_command(text, "search <engine> <query>")
    engine = parts[1].strip()
    query = parts[2].strip()
    if not query:
        return _invalid_command(text, "search <engine> <query>")
    message = validate_known_identifier(engine, registry.search_engine_names, "registered search engine")
    if message is not None:
        return ParsedError(message=message, value=engine)
    return SearchCommand(engine=engine, query=query)


def _parse_script_command(
    text: str,
    registry: CommandRegistry,
) -> ScriptCommand | ParsedError:
    parts = text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return _invalid_command(text, "exec <script-id>")
    identifier = parts[1].strip()
    message = validate_known_identifier(identifier, registry.script_names, "registered script identifier")
    if message is not None:
        return ParsedError(message=message, value=identifier)
    return ScriptCommand(identifier=identifier)


def _parse_program_command(
    text: str,
    registry: CommandRegistry,
) -> ProgramCommand | ParsedError:
    parts = text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        return _invalid_command(text, "open <program-id>")
    identifier = parts[1].strip()
    message = validate_known_identifier(identifier, registry.program_names, "registered program identifier")
    if message is not None:
        return ParsedError(message=message, value=identifier)
    return ProgramCommand(identifier=identifier)


def _invalid_command(value: str, expected_format: str) -> ParsedError:
    message = (
        f"Invalid command value={value!r}; expected format={expected_format!r}."
    )
    return ParsedError(message=message, value=value)
