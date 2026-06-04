from pathlib import Path

import pytest

from dcmd.main import run


def test_run_loads_registry_outside_repository_root(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    outside_path = Path(__file__).resolve().anchor
    monkeypatch.chdir(outside_path)
    exit_code = run(["yt"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "direct:yt"
