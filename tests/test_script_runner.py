from pathlib import Path

import pytest

from dcmd.core.command_registry import ScriptConfig
from dcmd.runners.script_runner import SecureScriptRunner


class FakeProcessLauncher:
    def __init__(self) -> None:
        self.calls: list[tuple[Path, Path]] = []

    def run_python(self, python_path: Path, script_path: Path) -> None:
        self.calls.append((python_path, script_path))


def test_run_script_executes_registered_python_file(tmp_path: Path) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    script_path = scripts_dir / "script-1.py"
    script_path.write_text("print('ok')", encoding="utf-8")
    launcher = FakeProcessLauncher()
    runner = SecureScriptRunner(launcher, scripts_dir, Path("C:/Python/python.exe"))
    runner.run_script(ScriptConfig("script-1", "script-1.py", "Example script"))
    assert launcher.calls == [(Path("C:/Python/python.exe"), script_path.resolve())]


def test_run_script_blocks_path_traversal(tmp_path: Path) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    launcher = FakeProcessLauncher()
    runner = SecureScriptRunner(launcher, scripts_dir, Path("C:/Python/python.exe"))
    script = ScriptConfig("script-1", "../bad.py", "Example script")
    with pytest.raises(ValueError, match="path inside scripts folder"):
        runner.run_script(script)


def test_run_script_blocks_non_python_file(tmp_path: Path) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    launcher = FakeProcessLauncher()
    runner = SecureScriptRunner(launcher, scripts_dir, Path("C:/Python/python.exe"))
    script = ScriptConfig("script-1", "bad.txt", "Example script")
    with pytest.raises(ValueError, match="registered \\.py file"):
        runner.run_script(script)


def test_run_script_blocks_missing_file(tmp_path: Path) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    launcher = FakeProcessLauncher()
    runner = SecureScriptRunner(launcher, scripts_dir, Path("C:/Python/python.exe"))
    script = ScriptConfig("script-1", "missing.py", "Example script")
    with pytest.raises(ValueError, match="existing registered script file"):
        runner.run_script(script)
