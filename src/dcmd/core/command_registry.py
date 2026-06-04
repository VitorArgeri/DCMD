from dataclasses import dataclass
from pathlib import Path

from dcmd.utils.json_loader import JsonObject, load_json_object
from dcmd.utils.validators import require_mapping_keys


@dataclass(frozen=True)
class CommandRegistry:
    command_names: frozenset[str]
    search_engine_names: frozenset[str]
    script_names: frozenset[str]
    program_names: frozenset[str]


def load_command_registry(path: Path) -> CommandRegistry:
    """Load command identifiers from the project JSON configuration.

    Example:
        >>> load_command_registry(Path("config/commands.json"))
    """
    payload = load_json_object(path)
    return build_command_registry(payload)


def build_command_registry(payload: JsonObject) -> CommandRegistry:
    """Build a registry with known command identifiers.

    Example:
        >>> build_command_registry({"commands": {}, "search_engines": {}, "scripts": {}})
    """
    commands = require_mapping_keys(payload, "commands")
    search_engines = require_mapping_keys(payload, "search_engines")
    scripts = require_mapping_keys(payload, "scripts")
    program_names = _collect_program_names(commands)
    return CommandRegistry(
        command_names=frozenset(commands.keys()),
        search_engine_names=frozenset(search_engines.keys()),
        script_names=frozenset(scripts.keys()),
        program_names=program_names,
    )


def _collect_program_names(commands: JsonObject) -> frozenset[str]:
    names = {name for name, details in commands.items() if _is_program_command(details)}
    return frozenset(names)


def _is_program_command(details: object) -> bool:
    if not isinstance(details, dict):
        return False
    command_type = details.get("type")
    return isinstance(command_type, str) and command_type == "open_program"
