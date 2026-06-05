from pathlib import Path

import pytest

from dcmd.core.command_registry import (
    BrowserConfig,
    CommandRegistry,
    OpenProgramCommandConfig,
    OpenUrlCommandConfig,
    ScriptConfig,
    SearchEngineConfig,
    WorkflowActionConfig,
    WorkflowCommandConfig,
    build_command_registry,
    load_command_registry,
)


def test_load_command_registry_returns_known_names() -> None:
    registry = load_command_registry(Path("config/commands.json"))
    assert registry == CommandRegistry(
        browser=BrowserConfig(
            name="Opera GX",
            path=Path("D:/Navegador/Opera/opera_new.exe"),
        ),
        commands={
            "yt": OpenUrlCommandConfig(
                identifier="yt",
                url="https://www.youtube.com",
            ),
            "vscode": OpenProgramCommandConfig(
                identifier="vscode",
                path=Path(
                    "C:/Users/<user>/AppData/Local/Programs/Microsoft VS Code/Code.exe"
                ),
            ),
            "modo estudo": WorkflowCommandConfig(
                identifier="modo estudo",
                actions=(
                    WorkflowActionConfig(
                        action_type="open_url",
                        target="https://vestibulares.estrategia.com/estudos-em-andamento?tab=recent_activities",
                    ),
                    WorkflowActionConfig(
                        action_type="open_program",
                        target="D:\\Anotacoes\\Anki\\anki.exe",
                    ),
                    WorkflowActionConfig(
                        action_type="open_program",
                        target="D:\\Anotacoes\\Obsidian-1.7.7.exe",
                    ),
                ),
            ),
        },
        search_engines={
            "yt": SearchEngineConfig(
                identifier="yt",
                name="YouTube",
                url_template="https://www.youtube.com/results?search_query={query}",
            ),
            "google": SearchEngineConfig(
                identifier="google",
                name="Google",
                url_template="https://www.google.com/search?q={query}",
            ),
            "github": SearchEngineConfig(
                identifier="github",
                name="GitHub",
                url_template="https://github.com/search?q={query}",
            ),
            "reddit": SearchEngineConfig(
                identifier="reddit",
                name="Reddit",
                url_template="https://www.reddit.com/search/?q={query}",
            ),
        },
        scripts={
            "script-1": ScriptConfig(
                identifier="script-1",
                file_name="script-1.py",
                description="Example script for testing script execution.",
            ),
        },
    )


def test_build_command_registry_requires_commands_mapping() -> None:
    payload = {
        "browser": {"name": "Opera GX", "path": "C:/Opera/launcher.exe"},
        "commands": [],
        "search_engines": {},
        "scripts": {},
    }
    with pytest.raises(ValueError, match="JSON object field"):
        build_command_registry(payload)


def test_build_command_registry_rejects_missing_query_placeholder() -> None:
    payload = {
        "browser": {"name": "Opera GX", "path": "C:/Opera/launcher.exe"},
        "commands": {},
        "search_engines": {"yt": {"name": "YouTube", "url_template": "https://x"}},
        "scripts": {},
    }
    with pytest.raises(ValueError, match="url_template containing"):
        build_command_registry(payload)


def test_build_command_registry_rejects_missing_program_path() -> None:
    payload = {
        "browser": {"name": "Opera GX", "path": "C:/Opera/launcher.exe"},
        "commands": {"vscode": {"type": "open_program"}},
        "search_engines": {},
        "scripts": {},
    }
    with pytest.raises(ValueError, match="non-empty string field"):
        build_command_registry(payload)


def test_build_command_registry_rejects_unsupported_workflow_action() -> None:
    payload = {
        "browser": {"name": "Opera GX", "path": "C:/Opera/launcher.exe"},
        "commands": {
            "modo estudo": {
                "type": "workflow",
                "actions": [{"type": "script", "target": "study-setup.py"}],
            }
        },
        "search_engines": {},
        "scripts": {},
    }
    with pytest.raises(ValueError, match="expected format='open_url or open_program'"):
        build_command_registry(payload)
