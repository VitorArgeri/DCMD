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
        self._entries.append(
            HistoryEntry(prefix=">", message=command_text, tone="command")
        )

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

    def clear(self) -> None:
        """Remove all session entries from the rendered history.

        Example:
            >>> history = SessionHistory()
            >>> history.clear()
        """
        self._entries.clear()


class InputHistory:
    """Navigate previously submitted commands during the current session.

    Example:
        >>> history = InputHistory()
        >>> history.record("yt")
    """

    def __init__(self) -> None:
        self._commands: list[str] = []
        self._navigation_index: int | None = None
        self._draft_text = ""

    def record(self, command_text: str) -> None:
        """Store one submitted command and reset navigation state.

        Example:
            >>> history = InputHistory()
            >>> history.record("yt")
        """
        self._commands.append(command_text)
        self._navigation_index = None
        self._draft_text = ""

    def previous(self, current_text: str) -> str:
        """Return the previous command in history.

        Example:
            >>> history = InputHistory()
            >>> history.previous("")
        """
        if not self._commands:
            return current_text
        if self._navigation_index is None:
            self._draft_text = current_text
            self._navigation_index = len(self._commands) - 1
        else:
            self._navigation_index = max(0, self._navigation_index - 1)
        return self._commands[self._navigation_index]

    def next(self, current_text: str) -> str:
        """Return the next command in history or restore draft input.

        Example:
            >>> history = InputHistory()
            >>> history.next("")
        """
        if self._navigation_index is None:
            return current_text
        if self._navigation_index >= len(self._commands) - 1:
            self._navigation_index = None
            return self._draft_text
        self._navigation_index += 1
        return self._commands[self._navigation_index]
