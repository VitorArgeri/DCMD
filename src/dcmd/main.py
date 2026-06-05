import sys

from dcmd.app import run_application
from dcmd.core.command_executor import CommandExecutor
from dcmd.core.command_parser import parse_command
from dcmd.core.command_registry import CommandRegistry, load_command_registry
from dcmd.integrations.process_launcher import ProcessLauncher, SubprocessCommandRunner
from dcmd.runners.script_runner import SecureScriptRunner
from dcmd.utils.paths import project_root


def run(argv: list[str] | None = None) -> int:
    """Parse a command string using the configured registry.

    Example:
        >>> run(["yt"])
    """
    args = sys.argv[1:] if argv is None else argv
    registry = _load_default_registry()
    executor = _build_default_executor(registry)
    text = " ".join(args)
    parsed = parse_command(text=text, registry=registry)
    result = executor.execute(parsed)
    print(result.message)
    return 0 if result.success else 1


def main(argv: list[str] | None = None) -> int:
    """Start the graphical launcher application.

    Example:
        >>> main()
    """
    args = sys.argv[1:] if argv is None else argv
    if _is_background_launch(args):
        return run_application(show_on_startup=False)
    if args:
        return run(args)
    return run_application()


def _build_default_executor(registry: CommandRegistry) -> CommandExecutor:
    process_launcher = ProcessLauncher(SubprocessCommandRunner())
    script_runner = SecureScriptRunner(process_launcher)
    return CommandExecutor(registry, process_launcher, script_runner)


def _load_default_registry() -> CommandRegistry:
    commands_path = project_root() / "config" / "commands.json"
    return load_command_registry(commands_path)


def _is_background_launch(args: list[str]) -> bool:
    return args == ["--background"]


if __name__ == "__main__":
    raise SystemExit(main())
