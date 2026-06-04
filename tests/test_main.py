import pytest

from dcmd.core.command_executor import ExecutionResult
from dcmd.main import run


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
