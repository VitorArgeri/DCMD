from dataclasses import dataclass

from dcmd.core.command_registry import CommandRegistry


@dataclass(frozen=True)
class AutocompleteResult:
    text: str
    suggestions: tuple[str, ...]
    applied: bool


class AutocompleteEngine:
    """Build autocomplete candidates from the configured command registry.

    Example:
        >>> isinstance(AutocompleteEngine, type)
    """

    def __init__(self, registry: CommandRegistry) -> None:
        self._candidates = _build_candidates(registry)

    def suggestions(self, text: str) -> tuple[str, ...]:
        """Return matching command candidates for the current input.

        Example:
            >>> isinstance(text, str)
        """
        normalized_text = text.strip()
        if not normalized_text:
            return tuple()
        return tuple(
            candidate
            for candidate in self._candidates
            if candidate.startswith(normalized_text)
        )

    def complete(self, text: str) -> AutocompleteResult:
        """Return the next autocomplete state for one Tab action.

        Example:
            >>> isinstance(text, str)
        """
        matches = self.suggestions(text)
        if len(matches) != 1:
            return AutocompleteResult(text=text, suggestions=matches, applied=False)
        completed_text = _completed_text(matches[0])
        return AutocompleteResult(
            text=completed_text, suggestions=tuple(), applied=True
        )


def _build_candidates(registry: CommandRegistry) -> tuple[str, ...]:
    commands = tuple(sorted(registry.command_names))
    searches = tuple(f"search {name}" for name in sorted(registry.search_engine_names))
    programs = tuple(f"open {name}" for name in sorted(registry.program_names))
    scripts = tuple(f"exec {name}" for name in sorted(registry.script_names))
    return commands + searches + programs + scripts


def _completed_text(candidate: str) -> str:
    if candidate.startswith("search "):
        return f"{candidate} "
    return candidate
