import ctypes
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from threading import Event, Thread
from typing import Callable

from dcmd.utils.diagnostics import log_diagnostic_event
from dcmd.utils.json_loader import load_json_object

WM_HOTKEY = 0x0312
WM_QUIT = 0x0012
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
MOD_NOREPEAT = 0x4000
HOTKEY_ID = 1
DEFAULT_HOTKEY = "ctrl+shift+j"
USER32 = ctypes.windll.user32


@dataclass(frozen=True)
class HotkeyBinding:
    label: str
    modifiers: int
    virtual_key: int


def load_hotkey_binding(path: Path) -> HotkeyBinding:
    """Load the configured hotkey or return the default binding.

    Example:
        >>> isinstance(load_hotkey_binding(path), HotkeyBinding)
    """
    payload = load_json_object(path)
    hotkey = payload.get("hotkey")
    if not isinstance(hotkey, str) or not hotkey.strip():
        return parse_hotkey(DEFAULT_HOTKEY)
    return parse_hotkey(hotkey)


def parse_hotkey(hotkey_text: str) -> HotkeyBinding:
    """Parse one hotkey string into Windows registration values.

    Example:
        >>> parse_hotkey("ctrl+shift+j")
    """
    normalized = hotkey_text.strip().lower()
    parts = tuple(part.strip() for part in normalized.split("+") if part.strip())
    modifiers = _parse_modifiers(parts)
    virtual_key = _parse_key(parts)
    return HotkeyBinding(label=normalized, modifiers=modifiers, virtual_key=virtual_key)


class WindowsGlobalHotkey:
    """Register one global Windows hotkey on a background message thread."""

    def __init__(self, binding: HotkeyBinding) -> None:
        self._binding = binding
        self._thread: Thread | None = None
        self._thread_id = 0
        self._ready = Event()
        self._failed = Event()
        self._error_message = ""

    def start(self, callback: Callable[[], None]) -> None:
        """Start the hotkey listener in a background thread.

        Example:
            >>> callable(callback)
        """
        if self._thread is not None:
            return
        log_diagnostic_event("hotkey.start", binding=self._binding.label)
        self._thread = Thread(target=self._run, args=(callback,), daemon=True)
        self._thread.start()
        self._ready.wait(timeout=2)
        if self._failed.is_set():
            log_diagnostic_event(
                "hotkey.start_failed",
                binding=self._binding.label,
                error=self._error_message,
            )
            raise OSError(self._error_message)

    def stop(self) -> None:
        """Stop the hotkey listener and unregister the hotkey.

        Example:
            >>> isinstance(self._thread, object)
        """
        if self._thread is None:
            return
        USER32.PostThreadMessageW(self._thread_id, WM_QUIT, 0, 0)
        self._thread.join(timeout=2)
        self._thread = None

    def _run(self, callback: Callable[[], None]) -> None:
        self._thread_id = ctypes.windll.kernel32.GetCurrentThreadId()
        modifiers = self._binding.modifiers | MOD_NOREPEAT
        success = USER32.RegisterHotKey(
            None, HOTKEY_ID, modifiers, self._binding.virtual_key
        )
        if not success:
            self._error_message = (
                "Failed to register hotkey "
                f"value={self._binding.label!r}; "
                "expected format='available global hotkey'."
            )
            self._failed.set()
            self._ready.set()
            return
        log_diagnostic_event("hotkey.registered", binding=self._binding.label)
        self._ready.set()
        message = wintypes.MSG()
        while USER32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
            if message.message == WM_HOTKEY:
                log_diagnostic_event("hotkey.triggered", binding=self._binding.label)
                callback()
        USER32.UnregisterHotKey(None, HOTKEY_ID)


def _parse_modifiers(parts: tuple[str, ...]) -> int:
    modifiers = 0
    for part in parts[:-1]:
        if part == "ctrl":
            modifiers |= MOD_CONTROL
        elif part == "alt":
            modifiers |= MOD_ALT
        elif part == "shift":
            modifiers |= MOD_SHIFT
        elif part == "win":
            modifiers |= MOD_WIN
        else:
            raise ValueError(
                "Invalid hotkey "
                f"value={'+'.join(parts)!r}; "
                "expected format='ctrl+shift+j'."
            )
    if modifiers:
        return modifiers
    raise ValueError(
        f"Invalid hotkey value={'+'.join(parts)!r}; expected format='modifier+key'."
    )


def _parse_key(parts: tuple[str, ...]) -> int:
    key = parts[-1]
    if len(key) == 1 and key.isalnum():
        return ord(key.upper())
    function_keys = {f"f{index}": 0x6F + index for index in range(1, 13)}
    if key in function_keys:
        return function_keys[key]
    raise ValueError(
        f"Invalid hotkey value={'+'.join(parts)!r}; expected format='modifier+key'."
    )
