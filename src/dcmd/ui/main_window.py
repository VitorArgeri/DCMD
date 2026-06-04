from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from dcmd.app import CommandSubmissionService, PROMPT_TEXT
from dcmd.ui.terminal_input import TerminalInput
from dcmd.ui.theme import ThemeColors, build_window_stylesheet, format_history_html


class MainWindow(QMainWindow):
    """Floating launcher window for DCMD."""

    def __init__(self, command_service: CommandSubmissionService) -> None:
        super().__init__()
        self._command_service = command_service
        self._colors = ThemeColors()
        self._history_view = QTextEdit()
        self._input = TerminalInput()
        self._prompt_label = QLabel(PROMPT_TEXT)
        self._configure_window()
        self._build_layout()
        self._connect_events()
        self._render_history()

    def showEvent(self, event: object) -> None:
        super().showEvent(event)
        self._center_on_screen()
        self._input.setFocus(Qt.FocusReason.ActiveWindowFocusReason)

    def _configure_window(self) -> None:
        self.setWindowTitle("DCMD")
        self.resize(960, 420)
        root = QWidget()
        root.setObjectName("launcherRoot")
        self.setCentralWidget(root)
        self.setStyleSheet(build_window_stylesheet(self._colors))

    def _build_layout(self) -> None:
        root = self.centralWidget()
        assert root is not None
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(14)
        self._history_view.setObjectName("historyView")
        self._history_view.setReadOnly(True)
        self._history_view.setFont(QFont("Consolas", 11))
        self._prompt_label.setObjectName("promptLabel")
        self._prompt_label.setWordWrap(True)
        prompt_row = QHBoxLayout()
        prompt_row.setSpacing(12)
        prompt_row.addWidget(self._prompt_label, 2)
        prompt_row.addWidget(self._input, 3)
        root_layout.addWidget(self._history_view, 1)
        root_layout.addLayout(prompt_row)

    def _connect_events(self) -> None:
        self._input.command_submitted.connect(self._submit_command)

    def _submit_command(self, text: str) -> None:
        outcome = self._command_service.submit(text)
        if outcome.accepted:
            self._input.clear()
        self._render_history()

    def _render_history(self) -> None:
        html = format_history_html(self._command_service.history.entries(), self._colors)
        self._history_view.setHtml(html)
        self._history_view.moveCursor(QTextCursor.MoveOperation.End)

    def _center_on_screen(self) -> None:
        screen = self.screen()
        if screen is None:
            return
        geometry = screen.availableGeometry()
        x_pos = geometry.x() + (geometry.width() - self.width()) // 2
        y_pos = geometry.y() + (geometry.height() - self.height()) // 2
        self.move(x_pos, y_pos)
