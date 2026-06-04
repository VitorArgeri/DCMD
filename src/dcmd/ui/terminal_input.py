from collections.abc import Callable

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit

from dcmd.core.autocomplete import AutocompleteEngine
from dcmd.core.history import InputHistory


class TerminalInput(QLineEdit):
    """Command input widget that emits submitted text on Enter."""

    command_submitted = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._input_history: InputHistory | None = None
        self._autocomplete: AutocompleteEngine | None = None
        self._suggestions_handler: Callable[[tuple[str, ...]], None] | None = None
        self.setObjectName("terminalInput")
        self.returnPressed.connect(self._emit_submission)

    def set_input_history(self, input_history: InputHistory) -> None:
        self._input_history = input_history

    def set_autocomplete(self, autocomplete: AutocompleteEngine) -> None:
        self._autocomplete = autocomplete

    def set_suggestions_handler(
        self,
        handler: Callable[[tuple[str, ...]], None],
    ) -> None:
        self._suggestions_handler = handler

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Up:
            self._navigate_previous()
            return
        if event.key() == Qt.Key.Key_Down:
            self._navigate_next()
            return
        if event.key() == Qt.Key.Key_Tab:
            self._apply_completion()
            return
        super().keyPressEvent(event)
        self._publish_suggestions(tuple())

    def _emit_submission(self) -> None:
        self.command_submitted.emit(self.text())
        self._publish_suggestions(tuple())

    def _navigate_previous(self) -> None:
        if self._input_history is None:
            return
        self.setText(self._input_history.previous(self.text()))
        self.end(False)
        self._publish_suggestions(tuple())

    def _navigate_next(self) -> None:
        if self._input_history is None:
            return
        self.setText(self._input_history.next(self.text()))
        self.end(False)
        self._publish_suggestions(tuple())

    def _apply_completion(self) -> None:
        if self._autocomplete is None:
            return
        result = self._autocomplete.complete(self.text())
        if result.applied:
            self.setText(result.text)
            self.end(False)
        self._publish_suggestions(result.suggestions)

    def _publish_suggestions(self, suggestions: tuple[str, ...]) -> None:
        if self._suggestions_handler is not None:
            self._suggestions_handler(suggestions)
