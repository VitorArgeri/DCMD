from pathlib import Path

from dcmd.integrations.process_launcher import ProcessLauncher


class FakeCommandRunner:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def start(self, command: list[str]) -> None:
        self.calls.append(command)


class FailingCommandRunner:
    def start(self, command: list[str]) -> None:
        raise FileNotFoundError("missing executable")


def test_open_url_builds_browser_command() -> None:
    runner = FakeCommandRunner()
    launcher = ProcessLauncher(runner)
    launcher.open_url(Path("C:/Opera/launcher.exe"), "https://www.youtube.com")
    assert runner.calls == [["C:\\Opera\\launcher.exe", "https://www.youtube.com"]]


def test_open_program_builds_program_command() -> None:
    runner = FakeCommandRunner()
    launcher = ProcessLauncher(runner)
    launcher.open_program(Path("C:/Apps/Code.exe"))
    assert runner.calls == [["C:\\Apps\\Code.exe"]]


def test_run_python_builds_python_command() -> None:
    runner = FakeCommandRunner()
    launcher = ProcessLauncher(runner)
    launcher.run_python(Path("C:/Python/python.exe"), Path("C:/scripts/tool.py"))
    assert runner.calls == [["C:\\Python\\python.exe", "C:\\scripts\\tool.py"]]


def test_open_program_returns_clear_error_for_missing_executable() -> None:
    launcher = ProcessLauncher(FailingCommandRunner())
    try:
        launcher.open_program(Path("C:/Apps/Missing.exe"))
    except ValueError as error:
        assert "expected format='existing program executable path'" in str(error)
    else:
        raise AssertionError("missing executable should raise ValueError")
