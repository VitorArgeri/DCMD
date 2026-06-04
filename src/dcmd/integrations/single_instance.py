import ctypes
from collections.abc import Callable
from typing import Generic, Protocol, TypeVar

WindowType = TypeVar("WindowType")
KERNEL32 = ctypes.windll.kernel32
ERROR_ALREADY_EXISTS = 183


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


class MutexProtocol(Protocol):
    """Minimal process mutex protocol for single-instance control."""

    def acquire(self) -> bool:
        """Acquire the instance lock once.

        Example:
            >>> isinstance(self.acquire(), bool)
        """

    def release(self) -> None:
        """Release the instance lock.

        Example:
            >>> self.release()
        """


class WindowsNamedMutex:
    """Windows named mutex used to prevent duplicate DCMD processes."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._handle: int | None = None

    def acquire(self) -> bool:
        """Acquire the named mutex.

        Example:
            >>> isinstance(self.acquire(), bool)
        """
        handle = KERNEL32.CreateMutexW(None, False, self._name)
        if handle == 0:
            raise OSError(
                "Failed to create mutex "
                f"value={self._name!r}; "
                "expected format='available Windows mutex name'."
            )
        self._handle = handle
        error_code = int(KERNEL32.GetLastError())
        return error_code != ERROR_ALREADY_EXISTS

    def release(self) -> None:
        """Release the named mutex if held.

        Example:
            >>> self.release()
        """
        if self._handle is None:
            return
        KERNEL32.CloseHandle(self._handle)
        self._handle = None


class SingleInstanceGuard:
    """Own the process lock that prevents duplicate launcher instances."""

    def __init__(self, mutex: MutexProtocol) -> None:
        self._mutex = mutex

    def acquire(self) -> bool:
        """Acquire the guard lock for the current process.

        Example:
            >>> isinstance(self.acquire(), bool)
        """
        return self._mutex.acquire()

    def release(self) -> None:
        """Release the guard lock.

        Example:
            >>> self.release()
        """
        self._mutex.release()
