# Sprint 02 - Command Executor and Opera GX Integration

## Goal

Implement real execution for registered DCMD commands.

By the end of this sprint, command text that was parsed in Sprint 01 must be connected to controlled actions: opening URLs in Opera GX, opening registered programs, running configurable searches, and executing only authorized Python scripts stored in the `scripts` folder.

Security is central in this sprint. DCMD must never execute arbitrary shell commands typed by the user.

## Scope

Included in this sprint:

- Implement command registry validation against `commands.json`.
- Implement URL opening through the configured Opera GX browser path.
- Implement registered program launching.
- Implement configurable search engines using URL templates.
- Implement secure Python script execution for registered scripts.
- Validate script paths before execution.
- Block scripts outside the `scripts` folder.
- Block scripts that are not registered in configuration.
- Block non-Python script files.
- Add tests for executor, registry, search URL building, and script validation.

Not included in this sprint:

- PySide6 graphical interface.
- Visual command history.
- Global hotkey registration.
- Autocomplete UI.
- Windows Startup folder integration.
- `.exe` packaging.

## Proposed File Changes

Expected new or updated files:

- `config/commands.json`
- `src/dcmd/core/command_executor.py`
- `src/dcmd/core/command_registry.py`
- `src/dcmd/integrations/process_launcher.py`
- `src/dcmd/runners/script_runner.py`
- `src/dcmd/utils/paths.py`
- `src/dcmd/utils/validators.py`
- `tests/test_command_executor.py`
- `tests/test_command_registry.py`
- `tests/test_process_launcher.py`
- `tests/test_script_runner.py`

## Tasks

- [ ] Create a command registry that loads configured commands, scripts, programs, and search engines.
- [ ] Validate that direct command identifiers exist before execution.
- [ ] Validate that program identifiers exist before execution.
- [ ] Validate that search engine identifiers exist before building a search URL.
- [ ] Validate that script identifiers exist before execution.
- [ ] Implement URL opening for `open_url` commands.
- [ ] Implement Opera GX launching with a URL argument.
- [ ] Implement registered program launching from configured executable paths.
- [ ] Implement search URL construction using `{query}` templates.
- [ ] URL-encode search query text before inserting it into search templates.
- [ ] Implement `script_runner.py` with strict path resolution.
- [ ] Verify that resolved script paths stay inside the project `scripts` folder.
- [ ] Verify that registered script targets end with `.py`.
- [ ] Execute scripts through the configured Python interpreter.
- [ ] Return simple user-facing success messages.
- [ ] Return simple user-facing error messages for blocked actions.
- [ ] Create named fake launcher classes for tests.
- [ ] Create named fake script runner classes for executor tests.
- [ ] Add regression tests for unregistered scripts.
- [ ] Add regression tests for path traversal attempts such as `../bad.py`.
- [ ] Add regression tests for non-Python script targets.

## Acceptance Criteria

- The command `yt` opens the configured YouTube URL through Opera GX.
- The command `search yt gameplays` builds a YouTube search URL for `gameplays`.
- The command `search google python decorators` builds the configured Google search URL.
- The command `open vscode` launches only the configured Visual Studio Code executable.
- The command `exec script-1` executes only the registered `script-1.py` inside `scripts`.
- Unregistered scripts are blocked.
- Script paths outside `scripts` are blocked even if a malicious relative path is configured.
- Non-`.py` script targets are blocked.
- Unknown command identifiers return a simple error.
- External process execution is wrapped behind a project-owned interface.
- Tests do not launch real programs, real browsers, or real scripts.

## Deliverables

- Command executor.
- Command registry validation.
- Process launcher interface.
- Secure script runner.
- Search URL builder behavior.
- Tests for command execution decisions.
- Tests for blocked script execution.
- Updated example configuration if new fields are needed.

## Decisions

- Third-party and OS process calls will be wrapped behind project-owned classes.
- Tests will use named fake classes instead of calling real Windows processes.
- The command executor will return messages that the UI can display later.
- Path validation will use resolved absolute paths, not raw string comparisons.
- Search engines will stay configurable through JSON URL templates.
- Opera GX will be the default browser target for URL actions in the MVP.

## Pending Items

- Confirm the exact Opera GX path on the target machine.
- Decide whether browser path belongs in `commands.json` or `settings.json`.
- Decide whether script output should be captured and shown in the UI.
- Decide whether long-running scripts should run in a detached process.
- Decide whether program path validation should happen at startup or execution time.

## Risks

- Direct use of `subprocess` in business logic would make tests slow and unsafe.
- Loose script path handling could allow arbitrary local script execution.
- Search URL templates can fail silently if `{query}` is missing.
- Program paths can be machine-specific, so configuration errors must be clear.

## Test Plan

Run the project test command after implementation.

Expected command:

```text
pytest
```

Minimum tests:

- Direct URL command execution delegates to the process launcher.
- Program command execution delegates to the process launcher.
- Search command execution builds the expected encoded URL.
- Unknown search engine returns an error.
- Registered script execution delegates to the script runner.
- Unregistered script execution is blocked.
- Script path traversal is blocked.
- Non-Python script target is blocked.
- Missing executable path produces a clear validation error.

## Final Checklist

- [ ] Executor supports `open_url`.
- [ ] Executor supports `open_program`.
- [ ] Executor supports `search`.
- [ ] Executor supports `script`.
- [ ] Script runner blocks unsafe paths.
- [ ] Process calls are wrapped.
- [ ] Tests use fakes for external I/O.
- [ ] Tests pass with one command.
- [ ] Sprint documentation matches the implemented behavior.
