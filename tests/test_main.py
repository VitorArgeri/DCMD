import pytest

from dcmd.main import run


def test_run_prints_parsed_command(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = run(["yt"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "direct:yt"
