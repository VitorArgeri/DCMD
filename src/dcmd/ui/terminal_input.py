from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit


class TerminalInput(QLineEdit):
    """Command input widget that emits submitted text on Enter."""

    command_submitted = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("terminalInput")
        self.returnPressed.connect(self._emit_submission)

    def _emit_submission(self) -> None:
        self.command_submitted.emit(self.text())
