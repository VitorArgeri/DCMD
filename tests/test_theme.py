from dcmd.core.history import HistoryEntry
from dcmd.ui.theme import ThemeColors, format_history_html


def test_format_history_html_returns_empty_string_for_empty_history() -> None:
    assert format_history_html(tuple(), ThemeColors()) == ""


def test_format_history_html_renders_history_entries() -> None:
    html = format_history_html(
        (HistoryEntry(prefix=">", message="yt", tone="command"),),
        ThemeColors(),
    )

    assert "> yt" in html
