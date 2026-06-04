from pathlib import Path

from dcmd.core.command_executor import CommandExecutor
from dcmd.core.command_parser import DirectCommand, ParsedError, ProgramCommand, ScriptCommand, SearchCommand
from dcmd.core.command_registry import (
    BrowserConfig,
    CommandRegistry,
    OpenProgramCommandConfig,
    OpenUrlCommandConfig,
    ScriptConfig,
    SearchEngineConfig,
)


class FakeProcessLauncher:
    def __init__(self) -> None:
        self.url_calls: list[tuple[Path, str]] = []
        self.program_calls: list[Path] = []

    def open_url(self, browser_path: Path, url: str) -> None:
        self.url_calls.append((browser_path, url))

    def open_program(self, program_path: Path) -> None:
        self.program_calls.append(program_path)


class FakeScriptRunner:
    def __init__(self) -> None:
        self.calls: list[ScriptConfig] = []

    def run_script(self, script: ScriptConfig) -> None:
        self.calls.append(script)


def test_execute_direct_url_command_delegates_to_process_launcher() -> None:
    executor, launcher, _ = build_executor()
    result = executor.execute(DirectCommand(identifier="yt"))
    assert result.success is True
    assert launcher.url_calls == [(Path("C:/Opera/launcher.exe"), "https://www.youtube.com")]


def test_execute_search_command_builds_encoded_url() -> None:
    executor, launcher, _ = build_executor()
    result = executor.execute(SearchCommand(engine="google", query="python decorators"))
    assert result.success is True
    assert launcher.url_calls == [
        (Path("C:/Opera/launcher.exe"), "https://www.google.com/search?q=python+decorators")
    ]


def test_execute_program_command_delegates_to_process_launcher() -> None:
    executor, launcher, _ = build_executor()
    result = executor.execute(ProgramCommand(identifier="vscode"))
    assert result.success is True
    assert launcher.program_calls == [Path("C:/Apps/Code.exe")]


def test_execute_script_command_delegates_to_script_runner() -> None:
    executor, _, script_runner = build_executor()
    result = executor.execute(ScriptCommand(identifier="script-1"))
    assert result.success is True
    assert script_runner.calls == [ScriptConfig("script-1", "script-1.py", "Example script")]


def test_execute_invalid_parse_result_returns_error() -> None:
    executor, _, _ = build_executor()
    result = executor.execute(ParsedError(message="Unknown command.", value="bad"))
    assert result.success is False
    assert result.message == "Unknown command."


def test_execute_unknown_direct_command_returns_error() -> None:
    executor, _, _ = build_executor()
    result = executor.execute(DirectCommand(identifier="missing"))
    assert result.success is False
    assert "expected format='registered command'" in result.message


def test_execute_unknown_search_engine_returns_error() -> None:
    executor, _, _ = build_executor()
    result = executor.execute(SearchCommand(engine="missing", query="topic"))
    assert result.success is False
    assert "expected format='registered search engine'" in result.message


def test_execute_unknown_script_identifier_returns_error() -> None:
    executor, _, _ = build_executor()
    result = executor.execute(ScriptCommand(identifier="missing"))
    assert result.success is False
    assert "expected format='registered script identifier'" in result.message


def test_execute_unknown_program_identifier_returns_error() -> None:
    executor, _, _ = build_executor()
    result = executor.execute(ProgramCommand(identifier="missing"))
    assert result.success is False
    assert "expected format='registered command'" in result.message


def build_executor() -> tuple[CommandExecutor, FakeProcessLauncher, FakeScriptRunner]:
    registry = CommandRegistry(
        browser=BrowserConfig("Opera GX", Path("C:/Opera/launcher.exe")),
        commands={
            "yt": OpenUrlCommandConfig("yt", "https://www.youtube.com"),
            "vscode": OpenProgramCommandConfig("vscode", Path("C:/Apps/Code.exe")),
        },
        search_engines={
            "google": SearchEngineConfig(
                "google",
                "Google",
                "https://www.google.com/search?q={query}",
            ),
        },
        scripts={"script-1": ScriptConfig("script-1", "script-1.py", "Example script")},
    )
    launcher = FakeProcessLauncher()
    script_runner = FakeScriptRunner()
    executor = CommandExecutor(registry, launcher, script_runner)
    return executor, launcher, script_runner
