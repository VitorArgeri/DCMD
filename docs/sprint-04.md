# Sprint 04 - Global Hotkey, History, and Autocomplete

## Goal

Make DCMD usable as a real background launcher.

By the end of this sprint, DCMD must remain available while the user works in other applications. Pressing the configured global hotkey must show or focus the existing launcher window. The command input must support session history navigation with the arrow keys and autocomplete with Tab.

## Scope

Included in this sprint:

- Implement configurable global hotkey support.
- Use `Ctrl + Shift + J` as the default hotkey.
- Load the hotkey from `settings.json`.
- Show the hidden window when the hotkey is pressed.
- Focus the existing window when the hotkey is pressed.
- Avoid opening multiple unnecessary launcher windows.
- Implement command history navigation with up and down arrows.
- Implement autocomplete for registered commands.
- Integrate autocomplete with direct commands, search engines, programs, and scripts.
- Add tests for history and autocomplete behavior.

Not included in this sprint:

- `.exe` packaging.
- Windows Startup folder integration.
- Full installer creation.
- Advanced fuzzy search.
- Persistent command history across application restarts.
- Advanced window management beyond show and focus.

## Proposed File Changes

Expected new or updated files:

- `src/dcmd/integrations/global_hotkey.py`
- `src/dcmd/integrations/single_instance.py`
- `src/dcmd/integrations/window_focus.py`
- `src/dcmd/core/autocomplete.py`
- `src/dcmd/core/history.py`
- `src/dcmd/ui/terminal_input.py`
- `src/dcmd/app.py`
- `config/settings.json`
- `tests/test_autocomplete.py`
- `tests/test_history.py`
- `tests/test_global_hotkey_config.py`

## Tasks

- [ ] Choose the global hotkey library after checking Windows behavior.
- [ ] Wrap the chosen hotkey library behind a project-owned interface.
- [ ] Load the configured hotkey from `settings.json`.
- [ ] Fall back to `ctrl+shift+j` when no custom hotkey is configured.
- [ ] Register the global hotkey during app startup.
- [ ] Ensure hotkey registration does not block the Qt event loop.
- [ ] Show the launcher window when the hotkey is pressed.
- [ ] Focus the launcher window when it is already visible.
- [ ] Prevent duplicate launcher windows inside the same process.
- [ ] Add initial single-instance protection if practical in this sprint.
- [ ] Implement command history storage for the current session.
- [ ] Navigate to the previous command with the up arrow.
- [ ] Navigate to the next command with the down arrow.
- [ ] Preserve unsent input where practical when navigating history.
- [ ] Implement autocomplete candidate generation.
- [ ] Complete the input with Tab when there is one match.
- [ ] Show suggestions when there are multiple matches.
- [ ] Include registered direct commands in autocomplete.
- [ ] Include `search <engine>` suggestions in autocomplete.
- [ ] Include `open <program>` suggestions in autocomplete.
- [ ] Include `exec <script>` suggestions in autocomplete.
- [ ] Add tests for history navigation.
- [ ] Add tests for autocomplete candidate generation.

## Acceptance Criteria

- The default hotkey is `Ctrl + Shift + J`.
- The hotkey can be changed through `settings.json`.
- Pressing the hotkey shows DCMD if it is hidden.
- Pressing the hotkey focuses DCMD if it is already open.
- Pressing the hotkey does not create multiple launcher windows.
- The up arrow moves to older commands in the current session.
- The down arrow moves toward newer commands in the current session.
- `Tab` completes the command when only one registered match exists.
- Multiple autocomplete matches are displayed or otherwise made visible to the user.
- Autocomplete uses commands from JSON configuration.
- Tests cover history navigation and autocomplete behavior.

## Deliverables

- Global hotkey integration.
- Hotkey configuration loading.
- Window show and focus behavior.
- Single-window protection inside the app.
- Command history navigation.
- Autocomplete engine.
- UI integration for Tab completion.
- Tests for autocomplete and history.

## Decisions

- The hotkey library will be hidden behind `global_hotkey.py`.
- Session history will stay in memory for the MVP.
- Autocomplete data will come from the command registry instead of hard-coded UI values.
- The input component will own keyboard-event behavior and delegate command knowledge to focused services.
- Duplicate window prevention is required; full OS-level single-instance locking can be completed in this sprint or documented for Sprint 05 if needed.

## Pending Items

- Confirm whether `keyboard` or `pynput` behaves better after PyInstaller packaging.
- Confirm whether global hotkey registration requires elevated permissions on the target Windows setup.
- Decide whether autocomplete suggestions should appear inline, in a popup, or in the history area.
- Decide whether autocomplete should support partial search queries after `search yt`.
- Decide whether OS-level single-instance locking is mandatory before packaging.

## Risks

- Some hotkey libraries can conflict with antivirus tools or Windows permissions.
- Hotkey callbacks can break UI behavior if they update Qt widgets from the wrong thread.
- Autocomplete can become inconsistent if it duplicates registry logic.
- History navigation can overwrite unsent user input if state transitions are not explicit.

## Test Plan

Run the project test command after implementation.

Expected command:

```text
pytest
```

Manual verification:

- Start DCMD.
- Focus another application.
- Press `Ctrl + Shift + J`.
- Confirm DCMD appears and receives focus.
- Press `Ctrl + Shift + J` again.
- Confirm the same window receives focus instead of a duplicate window opening.
- Submit multiple commands.
- Use up and down arrows to navigate previous inputs.
- Type a partial command and press Tab.
- Confirm autocomplete behavior matches the acceptance criteria.

Automated minimum tests:

- History starts empty.
- History returns previous command on up navigation.
- History returns next command on down navigation.
- Autocomplete returns direct command matches.
- Autocomplete returns search command matches.
- Autocomplete returns program command matches.
- Autocomplete returns script command matches.
- Hotkey configuration loader returns the default when missing.

## Final Checklist

- [ ] Configurable global hotkey works.
- [ ] Default hotkey is `Ctrl + Shift + J`.
- [ ] Window shows on hotkey.
- [ ] Window focuses on hotkey.
- [ ] Duplicate windows are avoided.
- [ ] Up and down history navigation works.
- [ ] Tab autocomplete works.
- [ ] Autocomplete uses JSON configuration.
- [ ] Tests pass with one command.
- [ ] Sprint documentation matches the implemented behavior.
