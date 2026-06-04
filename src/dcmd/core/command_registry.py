from dataclasses import dataclass
from pathlib import Path

from dcmd.utils.json_loader import JsonObject, JsonValue, load_json_object
from dcmd.utils.validators import require_mapping_keys, require_string


@dataclass(frozen=True)
class BrowserConfig:
    name: str
    path: Path


@dataclass(frozen=True)
class OpenUrlCommandConfig:
    identifier: str
    url: str
    kind: str = "open_url"


@dataclass(frozen=True)
class OpenProgramCommandConfig:
    identifier: str
    path: Path
    kind: str = "open_program"


RegisteredCommand = OpenUrlCommandConfig | OpenProgramCommandConfig


@dataclass(frozen=True)
class SearchEngineConfig:
    identifier: str
    name: str
    url_template: str


@dataclass(frozen=True)
class ScriptConfig:
    identifier: str
    file_name: str
    description: str


@dataclass(frozen=True)
class CommandRegistry:
    browser: BrowserConfig
    commands: dict[str, RegisteredCommand]
    search_engines: dict[str, SearchEngineConfig]
    scripts: dict[str, ScriptConfig]

    @property
    def command_names(self) -> frozenset[str]:
        return frozenset(self.commands.keys())

    @property
    def search_engine_names(self) -> frozenset[str]:
        return frozenset(self.search_engines.keys())

    @property
    def script_names(self) -> frozenset[str]:
        return frozenset(self.scripts.keys())

    @property
    def program_names(self) -> frozenset[str]:
        return frozenset(
            name
            for name, command in self.commands.items()
            if command.kind == "open_program"
        )


def load_command_registry(path: Path) -> CommandRegistry:
    """Load executable command configuration from JSON.

    Example:
        >>> load_command_registry(Path("config/commands.json"))
    """
    payload = load_json_object(path)
    return build_command_registry(payload)


def build_command_registry(payload: JsonObject) -> CommandRegistry:
    """Build a structured command registry from raw JSON data.

    Example:
        >>> build_command_registry(
        ...     {"browser": {}, "commands": {}, "search_engines": {}, "scripts": {}}
        ... )
    """
    browser = _build_browser_config(payload)
    commands = _build_commands(payload)
    search_engines = _build_search_engines(payload)
    scripts = _build_scripts(payload)
    return CommandRegistry(browser, commands, search_engines, scripts)


def _build_browser_config(payload: JsonObject) -> BrowserConfig:
    browser = require_mapping_keys(payload, "browser")
    name = require_string(browser, "name")
    path = Path(require_string(browser, "path"))
    return BrowserConfig(name=name, path=path)


def _build_commands(payload: JsonObject) -> dict[str, RegisteredCommand]:
    commands = require_mapping_keys(payload, "commands")
    return {name: _build_command(name, item) for name, item in commands.items()}


def _build_command(identifier: str, item: JsonValue) -> RegisteredCommand:
    command = _require_object(item, identifier)
    command_type = require_string(command, "type")
    if command_type == "open_url":
        url = require_string(command, "url")
        return OpenUrlCommandConfig(identifier=identifier, url=url)
    if command_type == "open_program":
        path = Path(require_string(command, "path"))
        return OpenProgramCommandConfig(identifier=identifier, path=path)
    raise ValueError(
        "Invalid command "
        f"value={identifier!r}; "
        "expected format='supported type open_url or open_program'."
    )


def _build_search_engines(payload: JsonObject) -> dict[str, SearchEngineConfig]:
    engines = require_mapping_keys(payload, "search_engines")
    return {name: _build_search_engine(name, item) for name, item in engines.items()}


def _build_search_engine(identifier: str, item: JsonValue) -> SearchEngineConfig:
    engine = _require_object(item, identifier)
    name = require_string(engine, "name")
    url_template = require_string(engine, "url_template")
    _validate_query_template(identifier, url_template)
    return SearchEngineConfig(
        identifier=identifier, name=name, url_template=url_template
    )


def _build_scripts(payload: JsonObject) -> dict[str, ScriptConfig]:
    scripts = require_mapping_keys(payload, "scripts")
    return {name: _build_script(name, item) for name, item in scripts.items()}


def _build_script(identifier: str, item: JsonValue) -> ScriptConfig:
    script = _require_object(item, identifier)
    file_name = require_string(script, "file")
    description = require_string(script, "description")
    return ScriptConfig(
        identifier=identifier, file_name=file_name, description=description
    )


def _require_object(value: JsonValue, identifier: str) -> JsonObject:
    if isinstance(value, dict):
        return value
    raise ValueError(
        "Invalid configuration "
        f"value={identifier!r}; "
        "expected format='JSON object field'."
    )


def _validate_query_template(identifier: str, url_template: str) -> None:
    if "{query}" in url_template:
        return
    raise ValueError(
        "Invalid search engine "
        f"value={identifier!r}; "
        "expected format='url_template containing {query}'."
    )
