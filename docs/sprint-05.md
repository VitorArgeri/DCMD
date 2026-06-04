# Sprint 05 - Packaging, Windows Startup, and Polish

## Goal

Prepare DCMD for real Windows usage as a local executable application.

By the end of this sprint, DCMD should be packageable as a `.exe`, able to start with Windows when configured, and polished enough for daily use through the configured global hotkey.

This sprint turns the working application into something the user can run without manually launching Python.

## Scope

Included in this sprint:

- Configure PyInstaller packaging.
- Generate a Windows `.exe`.
- Document the packaging process.
- Implement optional startup with Windows.
- Use the Windows Startup folder as the MVP startup solution.
- Improve window focus behavior after packaging.
- Improve simple error messages.
- Review configuration examples.
- Review project documentation.
- Create installation and usage instructions.
- Run a final end-to-end verification checklist.

Not included in this sprint:

- A full graphical installer.
- Cloud sync.
- External APIs.
- External databases.
- Windows Task Scheduler automation unless Startup folder behavior is insufficient.
- Persistent command logs.
- Advanced plugin marketplace or dynamic extension loading.

## Proposed File Changes

Expected new or updated files:

- `pyproject.toml`
- `requirements.txt`
- `dcmd.spec`
- `README.md`
- `docs/PROJECT.md`
- `docs/sprint-05.md`
- `config/commands.json`
- `config/settings.json`
- `src/dcmd/integrations/windows_startup.py`
- `src/dcmd/integrations/single_instance.py`
- `src/dcmd/integrations/window_focus.py`
- `tests/test_windows_startup.py`
- `tests/test_single_instance.py`

## Tasks

- [ ] Add PyInstaller to the development packaging workflow.
- [ ] Create or generate the PyInstaller spec file.
- [ ] Ensure required config files are included in the packaged app.
- [ ] Ensure the `scripts` folder is discoverable from the packaged app.
- [ ] Ensure PySide6 assets and plugins are bundled correctly.
- [ ] Build the `.exe`.
- [ ] Run the `.exe` outside the development command.
- [ ] Verify that the launcher window opens correctly from the `.exe`.
- [ ] Verify that the global hotkey works from the packaged app.
- [ ] Verify that `yt` opens YouTube in Opera GX from the packaged app.
- [ ] Verify that `search yt gameplays` opens a YouTube search from the packaged app.
- [ ] Verify that `exec script-1` runs only the registered script.
- [ ] Implement Windows Startup folder shortcut creation.
- [ ] Implement Windows Startup folder shortcut removal if startup is disabled.
- [ ] Add a setting for enabling or disabling startup with Windows.
- [ ] Keep startup behavior optional.
- [ ] Improve focus behavior if the packaged app behaves differently from development mode.
- [ ] Improve invalid command messages while keeping them simple.
- [ ] Review README with installation, configuration, and usage instructions.
- [ ] Review `PROJECT.md` and sprint archives for consistency.
- [ ] Run the full test suite.

## Acceptance Criteria

- A PyInstaller build command exists and is documented.
- A `.exe` can be generated successfully.
- The packaged `.exe` starts DCMD without requiring the user to manually run Python.
- The packaged app loads `commands.json` and `settings.json`.
- The packaged app can locate authorized scripts.
- The global hotkey works from the packaged app.
- DCMD can optionally start with Windows through the Startup folder.
- Startup can be disabled without manual file cleanup.
- The app avoids multiple unnecessary instances after packaging.
- User-facing installation and usage instructions exist.
- The final documentation matches the implemented MVP behavior.

## Deliverables

- PyInstaller packaging configuration.
- Generated `.exe` build process.
- Windows Startup folder integration.
- Startup enable and disable behavior.
- Improved focus behavior.
- Improved simple error messages.
- Installation instructions.
- Usage instructions.
- Final documentation review.
- Final MVP verification checklist.

## Decisions

- PyInstaller will be the packaging tool for the MVP.
- The Windows Startup folder will be the first startup mechanism because it is simple and user-visible.
- Windows Task Scheduler will remain a future option if more control is needed.
- Startup with Windows will be optional and configuration-driven.
- The packaged app must preserve the same security rules as development mode.
- Documentation must explain editable JSON configuration instead of hiding configuration behind a UI.

## Pending Items

- Confirm the final executable name.
- Confirm whether the build should be one-file or one-folder.
- Confirm whether configuration files should be copied beside the `.exe` or embedded with first-run extraction.
- Confirm whether Startup folder integration should use a shortcut or a small launcher script.
- Confirm whether the app should show a tray icon while running in the background.
- Confirm whether the release artifact should include default example scripts.

## Risks

- PyInstaller can miss PySide6 plugins or runtime assets without explicit configuration.
- One-file packaging can complicate access to editable JSON files and user scripts.
- Startup behavior can be confusing if the user cannot easily disable it.
- Hotkey behavior can differ between source execution and packaged execution.
- Antivirus tools may flag packaged executables that register hotkeys or launch processes.

## Test Plan

Run the project test command after implementation.

Expected command:

```text
pytest
```

Build verification:

```text
pyinstaller dcmd.spec
```

Manual verification:

- Build the executable.
- Start DCMD from the generated `.exe`.
- Confirm the launcher window appears.
- Focus another application and press `Ctrl + Alt + J`.
- Confirm DCMD appears and receives focus.
- Run `yt`.
- Run `search yt gameplays`.
- Run `open vscode` if the local path is configured.
- Run `exec script-1`.
- Try an unknown command.
- Try an unregistered script.
- Enable startup with Windows.
- Confirm the Startup folder shortcut is created.
- Disable startup with Windows.
- Confirm the Startup folder shortcut is removed.

Automated minimum tests:

- Startup shortcut path is resolved correctly.
- Startup enable behavior delegates to the Windows integration layer.
- Startup disable behavior removes only the DCMD shortcut.
- Packaged path resolution keeps scripts restricted to the authorized folder.
- Single-instance behavior prevents duplicate app startup where implemented.

## Final Checklist

- [ ] PyInstaller configuration exists.
- [ ] `.exe` build succeeds.
- [ ] Packaged app starts.
- [ ] Packaged app loads configuration.
- [ ] Packaged app finds authorized scripts.
- [ ] Global hotkey works after packaging.
- [ ] Startup with Windows can be enabled.
- [ ] Startup with Windows can be disabled.
- [ ] Focus behavior is acceptable.
- [ ] Error messages are simple and useful.
- [ ] README explains installation and usage.
- [ ] Documentation is reviewed.
- [ ] Tests pass with one command.
- [ ] Final MVP checklist is complete.
