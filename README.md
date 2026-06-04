# DCMD

DCMD is a local Windows launcher with a command-style interface.

## Current Scope

- terminal-style PySide6 launcher window
- configurable global hotkey
- direct commands, searches, program launching, and secure script execution
- session history and autocomplete
- optional Windows Startup-folder integration
- PyInstaller packaging configuration

## Development Setup

```text
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run Locally

Source run:

```text
.\.venv\Scripts\python.exe -m dcmd.main
```

CLI smoke path:

```text
.\.venv\Scripts\python.exe src\dcmd\main.py yt
```

## Validation

```text
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check src tests
.\.venv\Scripts\mypy.exe src
```

## Packaging

Build the Windows executable with PyInstaller:

```text
.\.venv\Scripts\python.exe -m PyInstaller dcmd.spec
```

The generated launcher is placed under `dist/DCMD/DCMD.exe`.

PyInstaller packages the runtime contents under `dist/DCMD/_internal/`.

The packaged build includes these runtime folders:

- `_internal/config/`
- `_internal/scripts/`

DCMD resolves those packaged paths automatically at runtime.

## Configuration

Main files:

- `config/commands.json`
- `config/settings.json`

Relevant settings:

- `hotkey`: global launcher shortcut, default `ctrl+alt+j`
- `startup.enabled`: when `true`, DCMD writes `DCMD.cmd` into the Windows Startup folder

## Startup Behavior

DCMD uses the Windows Startup folder as the MVP startup mechanism.

- packaged runs create a Startup entry that launches the built `DCMD.exe`
- source runs create a Startup entry that launches `pythonw -m dcmd.main` from the `src` directory when available
