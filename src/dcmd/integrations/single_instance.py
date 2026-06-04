from collections.abc import Callable
from typing import Generic, TypeVar

WindowType = TypeVar("WindowType")


class SingleWindowFactory(Generic[WindowType]):
    """Create one window instance per process and reuse it.

    Example:
        >>> isinstance(SingleWindowFactory, type)
    """

    def __init__(self) -> None:
        self._window: WindowType | None = None

    def get_or_create(self, factory: Callable[[], WindowType]) -> WindowType:
        """Return the existing window or create it once.

        Example:
            >>> callable(factory)
        """
        if self._window is None:
            self._window = factory()
        return self._window
