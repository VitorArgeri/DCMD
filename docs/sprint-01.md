# Sprint 01 - Project Foundation and Command Parser

## Goal

Create the project foundation and the first usable command interpretation layer for DCMD.

By the end of this sprint, the project must have a predictable Python structure, editable JSON configuration files, and a parser capable of understanding the first command formats described in `PROJECT.md`.

This sprint does not need to execute real actions yet. Its purpose is to make command text understandable and testable before UI, hotkey handling, and Windows execution are added.

## Scope

Included in this sprint:

- Create the initial repository structure.
- Create Python package folders under `src/dcmd`.
- Create the initial `config/commands.json`.
- Create the initial `config/settings.json`.
- Create the authorized `scripts` folder.
- Create a sample `scripts/script-1.py` file.
- Implement JSON loading with validation-friendly errors.
- Implement command parsing for direct commands, searches, script execution, and program opening.
- Implement basic command syntax validation.
- Implement parser-facing data types.
- Add initial tests for the command parser and JSON loading.

Not included in this sprint:

- Opening websites.
- Opening installed programs.
- Running Python scripts.
- Building the PySide6 graphical interface.
- Registering the global hotkey.
- Packaging the app as `.exe`.
- Starting the app automatically with Windows.

## Proposed File Changes

Expected new or updated files:

- `pyproject.toml`
- `requirements.txt`
- `.gitignore`
- `config/commands.json`
- `config/settings.json`
- `scripts/script-1.py`
- `src/dcmd/__init__.py`
- `src/dcmd/main.py`
- `src/dcmd/core/command_parser.py`
- `src/dcmd/core/command_registry.py`
- `src/dcmd/utils/json_loader.py`
- `src/dcmd/utils/validators.py`
- `tests/test_command_parser.py`
- `tests/test_json_loader.py`

## Tasks

- [ ] Create the initial folder structure described in `PROJECT.md`.
- [ ] Configure `pyproject.toml` with Python version, test command, `black`, `ruff`, and type-checking settings.
- [ ] Add project dependencies to `requirements.txt`.
- [ ] Create `commands.json` with examples for `yt`, `vscode`, `script-1`, and search engines.
- [ ] Create `settings.json` with the default hotkey `ctrl+alt+j`, theme values, and window defaults.
- [ ] Create a typed JSON loader that reads a file path and returns validated parsed content.
- [ ] Make JSON loader errors include the offending path and expected JSON format.
- [ ] Create parser result types for direct commands, search commands, script commands, and program commands.
- [ ] Parse direct command input such as `yt`.
- [ ] Parse search input such as `search yt gameplays`.
- [ ] Parse script input such as `exec script-1`.
- [ ] Parse program input such as `open vscode`.
- [ ] Reject empty commands with a simple validation result.
- [ ] Reject malformed search commands that do not include an engine and query.
- [ ] Reject malformed script commands that do not include a script identifier.
- [ ] Reject malformed open-program commands that do not include a program identifier.
- [ ] Add tests for valid direct command parsing.
- [ ] Add tests for valid search command parsing.
- [ ] Add tests for valid script command parsing.
- [ ] Add tests for valid program command parsing.
- [ ] Add regression-style tests for malformed commands.

## Acceptance Criteria

- The repository contains the initial folder structure from the project plan.
- A single documented test command can run all Sprint 01 tests.
- `commands.json` can be loaded from disk.
- `settings.json` can be loaded from disk.
- The parser returns a typed result instead of raw unstructured text.
- The command `yt` is recognized as a direct registered command name.
- The command `search yt gameplays` is recognized as a search command with engine `yt` and query `gameplays`.
- The command `exec script-1` is recognized as a script command with identifier `script-1`.
- The command `open vscode` is recognized as an open-program command with identifier `vscode`.
- Invalid syntax returns a clear error instead of raising an unhandled exception.
- Error messages include the offending value and the expected format when validation fails.
- Tests cover success and failure paths for the parser.

## Deliverables

- Initial Python package structure.
- Initial JSON configuration files.
- Initial sample authorized script.
- Command parser module.
- JSON loader utility.
- Parser tests.
- JSON loader tests.
- Updated documentation if implementation choices differ from `PROJECT.md`.

## Decisions

- Command parsing will be independent from command execution.
- The parser will not decide whether a command is allowed to run; it will only identify the command shape.
- Command validation that depends on configuration will belong to the registry layer.
- JSON files will remain manually editable.
- Direct shell command execution is out of scope and must not be introduced.
- The test suite will be created early so later execution and UI work can build on stable parser behavior.

## Pending Items

- Confirm the final dependency list after implementation starts.
- Decide whether parser results should use `dataclass`, `NamedTuple`, or a small typed class hierarchy.
- Confirm the final type checker: `mypy` or `pyright`.
- Decide whether `commands.json` and `settings.json` should have schema validation in Sprint 01 or later.
- Decide whether command aliases should be case-sensitive.

## Risks

- Parser rules can become difficult to extend if command types are handled with deeply nested conditionals.
- JSON validation can become too permissive if all configuration is loaded as generic dictionaries.
- Test names can become unclear if parser behavior is not split by command type.

## Test Plan

Run the project test command after implementation.

Expected command:

```text
pytest
```

Minimum tests:

- Direct command parsing.
- Search command parsing.
- Script command parsing.
- Program command parsing.
- Empty input handling.
- Malformed search input handling.
- Malformed script input handling.
- Malformed program input handling.
- Missing JSON file handling.
- Invalid JSON format handling.

## Final Checklist

- [ ] Folder structure exists.
- [ ] Configuration files exist.
- [ ] Parser supports the initial command formats.
- [ ] Parser returns typed results.
- [ ] Parser handles invalid syntax.
- [ ] JSON loading has useful validation errors.
- [ ] Tests pass with one command.
- [ ] Sprint documentation matches the implemented behavior.
