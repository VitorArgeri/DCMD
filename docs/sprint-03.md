# Sprint 03 - Graphical Launcher Interface

## Goal

Create the custom graphical launcher window for DCMD.

By the end of this sprint, the user must be able to type commands into a compact PySide6 window that looks and feels like a modern terminal launcher. The UI must display a fixed prompt, accept command input, show session history, and render simple success or error messages from the command execution layer.

## Scope

Included in this sprint:

- Build the first PySide6 application window.
- Apply a dark terminal-like visual identity.
- Use white text, light gray secondary text, and red accents.
- Create a floating centered window.
- Add the fixed prompt text from `PROJECT.md`.
- Add a command input field next to the prompt.
- Display recent session interactions.
- Wire submitted command text into the parser and executor.
- Display success and error messages in the history area.
- Keep the UI independent from command implementation details.

Not included in this sprint:

- Global hotkey registration.
- Running silently in the Windows tray.
- Autocomplete.
- Up and down arrow command history navigation.
- Preventing multiple app instances.
- Packaging as `.exe`.
- Windows Startup folder integration.

## Proposed File Changes

Expected new or updated files:

- `src/dcmd/app.py`
- `src/dcmd/main.py`
- `src/dcmd/ui/main_window.py`
- `src/dcmd/ui/terminal_input.py`
- `src/dcmd/ui/theme.py`
- `src/dcmd/core/history.py`
- `tests/test_history.py`
- `tests/test_ui_command_submission.py`

## Tasks

- [ ] Add PySide6 to the project dependencies.
- [ ] Create the application bootstrap that starts the Qt event loop.
- [ ] Create `MainWindow` for the floating launcher.
- [ ] Create a theme module for shared color and spacing values.
- [ ] Style the window with a black or near-black background.
- [ ] Use white as the main text color.
- [ ] Use red for accents, borders, cursor details, and errors.
- [ ] Add the prompt label with the exact text `What command do you want to use?`.
- [ ] Add a command input field beside or below the prompt depending on available width.
- [ ] Submit commands when the user presses Enter.
- [ ] Clear the input after successful submission.
- [ ] Add a visual history area for current-session interactions.
- [ ] Render submitted commands with a `>` prefix.
- [ ] Render command results below the submitted command.
- [ ] Render unknown commands as `Unknown command.`.
- [ ] Keep UI state in small focused classes.
- [ ] Add tests for session history behavior.
- [ ] Add tests for command submission flow where feasible without launching a real desktop window.

## Acceptance Criteria

- DCMD starts as a graphical application, not a raw Python console.
- The window appears centered on screen when launched.
- The window has a compact launcher layout.
- The main prompt uses the exact required text.
- The user can type a command and submit it with Enter.
- Submitted commands appear in the session history area.
- Executor result messages appear in the session history area.
- Invalid commands display `Unknown command.` or an equivalent simple error.
- The UI uses the project color direction: black, white, gray, and red.
- UI modules do not directly call subprocess or Windows integration APIs.

## Deliverables

- PySide6 launcher window.
- Theme module.
- Terminal input component.
- Visual session history.
- Command submission wiring.
- UI-facing command result display.
- Tests for non-visual UI logic and history behavior.

## Decisions

- PySide6 will be used for the graphical interface.
- The interface will be a custom window, not a terminal shell.
- The prompt text will be fixed and will not show the current folder path.
- The UI will display only current-session history.
- Persistent logs are not required for the MVP.
- UI styling values will be centralized so later polish does not require scattered edits.

## Pending Items

- Decide exact initial window dimensions.
- Decide whether the window should be frameless in the first UI version or after hotkey integration.
- Decide whether the app should hide after command execution.
- Decide whether command results should use icons or plain text.
- Decide how many history entries should be visible before scrolling.

## Risks

- UI code can become tightly coupled to command execution if dependencies are not injected.
- Visual polish can delay core usability if the first version is too ambitious.
- PySide6 tests can become fragile if they depend on real screen state.
- Long command output can break the compact window layout if not constrained.

## Test Plan

Run the project test command after implementation.

Expected command:

```text
pytest
```

Manual verification:

- Start the app.
- Confirm a graphical window appears.
- Confirm the visual style follows the black, white, and red direction.
- Type `yt` and press Enter.
- Confirm `> yt` appears in history.
- Confirm a result message appears below the command.
- Type an unknown command and press Enter.
- Confirm a simple error appears.

Automated minimum tests:

- Session history stores submitted commands.
- Session history stores result messages.
- Command submission calls the injected command service.
- Empty input is ignored or returns a clear validation result.

## Final Checklist

- [ ] PySide6 app starts.
- [ ] Launcher window exists.
- [ ] Prompt text is exact.
- [ ] Command input works.
- [ ] Visual history works.
- [ ] Success messages render.
- [ ] Error messages render.
- [ ] UI logic is separated from execution logic.
- [ ] Tests pass with one command.
- [ ] Sprint documentation matches the implemented behavior.
