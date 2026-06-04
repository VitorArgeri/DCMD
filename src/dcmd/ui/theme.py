from dataclasses import dataclass

from dcmd.app import PROMPT_TEXT
from dcmd.core.history import HistoryEntry


@dataclass(frozen=True)
class ThemeColors:
    background: str = "#050505"
    surface: str = "#0f0f10"
    border: str = "#2a2a2d"
    text: str = "#ffffff"
    muted: str = "#b8b8c0"
    accent: str = "#ff3b30"


def build_window_stylesheet(colors: ThemeColors) -> str:
    """Return the main launcher stylesheet.

    Example:
        >>> isinstance(build_window_stylesheet(ThemeColors()), str)
    """
    return (
        "QWidget#launcherRoot {"
        f"background-color: {colors.background};"
        f"border: 1px solid {colors.border};"
        "border-radius: 8px;"
        "}"
        "QLabel#promptLabel {"
        f"color: {colors.text};"
        "font-size: 15px;"
        "font-weight: 600;"
        "}"
        "QTextEdit#historyView {"
        f"background-color: {colors.surface};"
        f"color: {colors.muted};"
        f"border: 1px solid {colors.border};"
        "border-radius: 6px;"
        "padding: 12px;"
        "}"
        "QLineEdit#terminalInput {"
        f"background-color: {colors.surface};"
        f"color: {colors.text};"
        f"border: 1px solid {colors.border};"
        f"selection-background-color: {colors.accent};"
        "border-radius: 6px;"
        "padding: 10px 12px;"
        "}"
        "QLabel#suggestionsLabel {"
        f"color: {colors.muted};"
        "font-size: 12px;"
        "padding-left: 2px;"
        "}"
    )


def format_history_html(entries: tuple[HistoryEntry, ...], colors: ThemeColors) -> str:
    """Convert session history entries into styled HTML.

    Example:
        >>> format_history_html(tuple(), ThemeColors())
    """
    if not entries:
        return f"<span style='color:{colors.muted};'>" f"{PROMPT_TEXT}" "</span>"
    return "".join(_entry_html(entry, colors) for entry in entries)


def _entry_html(entry: HistoryEntry, colors: ThemeColors) -> str:
    prefix = entry.prefix
    message = entry.message
    tone = entry.tone
    color = _tone_color(tone, colors)
    rendered_prefix = f"{prefix} " if prefix else ""
    return (
        "<div style='margin-bottom:10px;'>"
        f"<span style='color:{color};'>{rendered_prefix}{message}</span>"
        "</div>"
    )


def _tone_color(tone: str, colors: ThemeColors) -> str:
    if tone == "command":
        return colors.text
    if tone == "error":
        return colors.accent
    return colors.muted
