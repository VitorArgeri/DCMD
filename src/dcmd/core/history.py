from dataclasses import dataclass


@dataclass(frozen=True)
class HistoryEntry:
    prefix: str
    message: str
    tone: str


class SessionHistory:
    """Store current-session launcher interactions for UI rendering.

    Example:
        >>> history = SessionHistory()
        >>> history.add_command("yt")
    """

    def __init__(self) -> None:
        self._entries: list[HistoryEntry] = []

    def add_command(self, command_text: str) -> None:
        """Append one submitted command entry.

        Example:
            >>> history = SessionHistory()
            >>> history.add_command("yt")
        """
        self._entries.append(HistoryEntry(prefix=">", message=command_text, tone="command"))

    def add_result(self, message: str, is_error: bool = False) -> None:
        """Append one execution result entry.

        Example:
            >>> history = SessionHistory()
            >>> history.add_result("Opening yt.")
        """
        tone = "error" if is_error else "result"
        self._entries.append(HistoryEntry(prefix="", message=message, tone=tone))

    def entries(self) -> tuple[HistoryEntry, ...]:
        """Return immutable session entries for rendering.

        Example:
            >>> history = SessionHistory()
            >>> history.entries()
        """
        return tuple(self._entries)
