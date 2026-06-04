from pathlib import Path
import sys

from dcmd.core.command_parser import ParsedCommand, ParsedError, parse_command
from dcmd.core.command_registry import CommandRegistry, load_command_registry
from dcmd.utils.paths import project_root


def run(argv: list[str] | None = None) -> int:
    """Parse a command string using the configured registry.

    Example:
        >>> run(["yt"])
    """
    args = sys.argv[1:] if argv is None else argv
    registry = _load_default_registry()
    text = " ".join(args)
    result = parse_command(text=text, registry=registry)
    print(_render_result(result))
    return 0


def main() -> int:
    """Run the lightweight Sprint 01 CLI entrypoint.

    Example:
        >>> main()
    """
    return run()


def _load_default_registry() -> CommandRegistry:
    commands_path = project_root() / "config" / "commands.json"
    return load_command_registry(commands_path)


def _render_result(result: ParsedCommand | ParsedError) -> str:
    if isinstance(result, ParsedError):
        return result.message
    return f"{result.kind}:{result.identifier}"


if __name__ == "__main__":
    raise SystemExit(main())
