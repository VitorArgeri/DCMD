from dcmd.core.history import HistoryEntry, InputHistory, SessionHistory


def test_history_stores_command_and_result_entries() -> None:
    history = SessionHistory()
    history.add_command("yt")
    history.add_result("Opening yt.")
    assert history.entries() == (
        HistoryEntry(prefix=">", message="yt", tone="command"),
        HistoryEntry(prefix="", message="Opening yt.", tone="result"),
    )


def test_history_marks_error_entries() -> None:
    history = SessionHistory()
    history.add_result("Unknown command.", is_error=True)
    assert history.entries() == (
        HistoryEntry(prefix="", message="Unknown command.", tone="error"),
    )


def test_input_history_returns_previous_commands() -> None:
    history = InputHistory()
    history.record("yt")
    history.record("open vscode")
    assert history.previous("") == "open vscode"
    assert history.previous("") == "yt"


def test_input_history_restores_draft_on_next() -> None:
    history = InputHistory()
    history.record("yt")
    history.record("open vscode")
    assert history.previous("sea") == "open vscode"
    assert history.next("") == "sea"
