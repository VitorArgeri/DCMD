import pytest

from dcmd.core.command_executor import ExecutionResult
from dcmd.main import main, run


class FakeExecutor:
    def execute(self, command: object) -> ExecutionResult:
        return ExecutionResult(success=True, message="Opening yt in Opera GX.")


def test_run_prints_execution_message(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "dcmd.main._build_default_executor", lambda registry: FakeExecutor()
    )
    exit_code = run(["yt"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Opening yt in Opera GX."


def test_main_runs_application_in_background_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_calls: list[bool] = []
    monkeypatch.setattr(
        "dcmd.main.run_application",
        lambda show_on_startup=True: captured_calls.append(show_on_startup) or 0,
    )

    exit_code = main(["--background"])

    assert exit_code == 0
    assert captured_calls == [False]
