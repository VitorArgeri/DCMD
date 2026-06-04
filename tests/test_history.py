from dcmd.core.history import HistoryEntry, SessionHistory


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
