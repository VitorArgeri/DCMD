import json
from pathlib import Path

from dcmd.utils.diagnostics import diagnostics_log_path, log_diagnostic_event


def test_diagnostics_log_path_uses_given_base_path(tmp_path: Path) -> None:
    assert diagnostics_log_path(tmp_path) == tmp_path / "dcmd.log"


def test_log_diagnostic_event_appends_json_line(tmp_path: Path) -> None:
    log_path = tmp_path / "dcmd.log"

    log_diagnostic_event("startup", log_path=log_path, mode="background")

    lines = log_path.read_text(encoding="utf-8").splitlines()
    payload = json.loads(lines[0])
    assert payload["event"] == "startup"
    assert payload["mode"] == "background"
