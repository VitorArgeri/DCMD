# PROJECT.md — DCMD (Dumb Command Prompt)

## 1. Overview

**DCMD (Dumb Command Prompt)** is a local Windows launcher inspired by the operational feel of a command-line terminal. Its purpose is to provide fast access to custom commands, simple automations, website shortcuts, application launching, configurable web searches, and controlled execution of local Python scripts.

The software will be developed in **Python**, run entirely locally, and will not use external APIs or external databases. The user should be able to activate DCMD at any time through a global hotkey, type a short command, and trigger a predefined action.

By default, the global hotkey will be:

```text
Ctrl + Shift + J
```

DCMD will run in the background after Windows starts. When the user presses the configured hotkey, the DCMD window should appear and receive focus automatically.

The interface will be a custom graphical window that simulates a modern terminal. It should not be a raw Python console. Visually, DCMD should use a dark theme with a black or near-black background, white text, and red accents. The visual direction should be closer to a modern developer terminal or tools such as Claude Code, rather than a direct copy of the traditional Windows CMD.

Unlike CMD, DCMD will not show the current folder path as the prompt. Instead, the main prompt will display:

```text
What command do you want to use?
```

The command input field will appear next to this prompt.

---

## 2. Goals

### 2.1 Main Goal

Build a lightweight local Windows launcher with a terminal-like graphical interface that can execute user-defined commands quickly, safely, and flexibly.

### 2.2 Specific Goals

- Allow DCMD to be opened or focused through a global hotkey.
- Keep the application running in the background.
- Create a custom graphical interface inspired by modern terminals.
- Use a black, white, and red visual identity.
- Allow commands to be configured through `.json` files.
- Allow websites to be opened through short commands.
- Allow installed Windows programs to be opened through configured commands.
- Allow configurable searches on websites such as YouTube, Google, GitHub, Reddit, and others.
- Allow Python scripts to be executed only when they are registered and stored inside the `scripts` folder.
- Provide command history navigation using the up and down arrow keys.
- Provide autocomplete for registered commands.
- Package the application as a `.exe` in the future.
- Allow the application to start automatically with Windows.

### 2.3 Example Usage

The user presses:

```text
Ctrl + Shift + J
```

DCMD appears and receives focus. The user types:

```text
yt
```

Expected result:

```text
Open YouTube in Opera GX.
```

Another example:

```text
search yt gameplays
```

Expected result:

```text
Open Opera GX, navigate to YouTube, and search for "gameplays".
```

Another example:

```text
exec script-1
```

Expected result:

```text
Find and execute the registered script named script-1.py inside the scripts folder.
```

---

## 3. Functional and Non-Functional Requirements

## 3.1 Functional Requirements

### FR01 — Global Hotkey

The system must allow the user to open or focus DCMD using a global hotkey.

- Default hotkey: `Ctrl + Shift + J`.
- The hotkey must be configurable through a settings file.
- The hotkey must work even when another application is focused.

### FR02 — Background Execution

DCMD must remain running in the background on Windows.

- When Windows starts, DCMD should be able to start automatically.
- While running in the background, DCMD must listen for the configured global hotkey.
- When the hotkey is triggered, the window must appear and receive focus.

### FR03 — Custom Graphical Interface

The system must provide its own graphical window that simulates a modern terminal.

- Black or near-black background.
- White main text.
- Red accent details.
- Minimal and elegant layout.
- Visual inspiration from modern terminal tools and Claude Code-like interfaces.
- Fixed prompt text: `What command do you want to use?`.

### FR04 — Window Focus Behavior

When the global hotkey is pressed, DCMD must focus the existing window.

- If the window is hidden, it should be shown.
- If the window is already open, it should receive focus.
- The system should avoid opening multiple unnecessary window instances.

### FR05 — Configurable Commands

The system must allow commands to be defined through `.json` configuration files.

Conceptual example:

```json
{
  "commands": {
    "yt": {
      "type": "open_url",
      "target": "https://www.youtube.com"
    },
    "opera": {
      "type": "open_program",
      "target": "C:/Users/<user>/AppData/Local/Programs/Opera GX/launcher.exe"
    },
    "script-1": {
      "type": "script",
      "target": "script-1.py"
    }
  }
}
```

### FR06 — Open Websites

The system must allow commands that open URLs in Opera GX.

Example command:

```text
yt
```

Expected result:

```text
Open https://www.youtube.com in Opera GX.
```

### FR07 — Open Programs

The system must allow commands that open installed Windows programs.

Example command:

```text
open vscode
```

Expected result:

```text
Open Visual Studio Code.
```

Programs must be registered in the local configuration file before they can be launched.

### FR08 — Configurable Searches

The system must support search commands with arguments.

Example command:

```text
search yt gameplays
```

Expected result:

```text
Open Opera GX and search YouTube for "gameplays".
```

The architecture must make it easy to add other search engines or searchable websites, such as:

```text
search google python decorators
search github python cli app
search reddit mechanical keyboard
```

Each search engine must be defined in `.json` using a URL template.

### FR09 — Execute Python Scripts

The system must allow registered Python scripts to be executed.

Example command:

```text
exec script-1
```

Rules:

- Only scripts inside the `scripts` folder may be executed.
- Only scripts registered in the `.json` configuration may be executed.
- The system must not execute arbitrary shell commands typed by the user.
- Scripts must be called through friendly identifiers, not necessarily by their full file names.

### FR10 — Command History

The system must keep command history during the current session.

- Up arrow: previous command.
- Down arrow: next command.
- Behavior should feel similar to CMD command navigation.

Persistent command logs are not required.

### FR11 — Autocomplete

The system must provide autocomplete for registered commands.

Desired behavior:

- The user starts typing a command.
- DCMD suggests compatible commands.
- The user can complete the command using `Tab`.
- Autocomplete should consider direct commands, search commands, open-program commands, and registered scripts.

### FR12 — Simple Error for Invalid Commands

When the user enters an unknown command, DCMD must display a simple error message.

Example:

```text
Unknown command.
```

### FR13 — Package as Executable

The system must support packaging as a `.exe`, preferably using PyInstaller.

The final goal is for the user to run DCMD without manually starting Python.

### FR14 — Start with Windows

The system must support starting DCMD automatically with Windows.

The recommended technical decision for the MVP is to use the Windows Startup folder because it is simple and easy to implement. Later, the Windows Task Scheduler can be evaluated if more control is needed.

### FR15 — Command Workflows

The system must allow one command to run multiple actions.

Example command:

    study mode

Expected result:

    1. Open Opera GX.
    2. Open YouTube.
    3. Open Visual Studio Code.
    4. Run the Python script study-setup.py.

Example configuration:

```json
{
  "commands": {
    "study mode": {
      "type": "workflow",
      "actions": [
        {
          "type": "open_program",
          "target": "Opera GX"
        },
        {
          "type": "open_url",
          "target": "https://www.youtube.com"
        },
        {
          "type": "open_program",
          "target": "Visual Studio Code"
        },
        {
          "type": "script",
          "target": "study-setup.py"
        }
      ]
    }
  }
}

---

## 3.2 Non-Functional Requirements

### NFR01 — Platform

DCMD will be developed exclusively for Windows.

### NFR02 — Language

The project will be developed in Python.

### NFR03 — Local Execution

The system must run locally and must not depend on external APIs or external databases.

### NFR04 — Simple Configuration

Configuration must be handled through clear and manually editable `.json` files.

### NFR05 — Security

The system must not directly execute arbitrary shell commands typed by the user.

Scripts can only be executed if they:

- are located inside the `scripts` folder;
- are Python files;
- are registered in the configuration file.

### NFR06 — Performance

DCMD must remain lightweight while running in the background.

- Low memory usage.
- Low CPU usage while waiting for the hotkey.
- Fast window activation after the hotkey is pressed.

### NFR07 — Maintainability

The project must be modular, separating UI, commands, configuration, script execution, autocomplete, history, and Windows integration.

### NFR08 — Extensibility

The architecture must allow new command types to be added in the future without rewriting the application core.

Possible future command types:

- open folder;
- run action sequences;
- copy text to clipboard;
- control windows;
- send keyboard shortcuts;
- open groups of programs;
- execute predefined automation flows.

---

## 4. Design

## 4.1 Visual Identity

DCMD should look like a modern, dark, minimal terminal-style launcher.

### Initial Palette

- Main background: black or near-black.
- Main text: white.
- Secondary text: light gray.
- Accents: red.
- Errors: red.
- Success messages: white or light gray, with red accents when appropriate.

### General Style

- Clean interface.
- Subtle borders.
- Floating launcher behavior.
- Inspired by modern CLI tools and Claude Code-like visual language.
- Avoid visual clutter.

## 4.2 Window

The window should behave like a floating launcher.

Desired characteristics:

- Open centered on the screen.
- Compact size, enough to show recent command history and the command input field.
- Automatically receive focus when called.
- Avoid creating multiple instances.
- Optionally support hiding after command execution in a future version.

## 4.3 Prompt

Unlike CMD, the prompt will not display the current directory path.

Desired prompt:

```text
What command do you want to use?  [user input]
```

Visual example:

```text
What command do you want to use? search yt gameplays
```

## 4.4 Visual History

The interface should display recent interactions from the current session.

Example:

```text
> yt
Opening YouTube in Opera GX...

> search yt gameplays
Searching YouTube for "gameplays"...

> unknown
Unknown command.
```

## 4.5 Autocomplete

Autocomplete should feel natural inside a terminal-like interface.

Recommended behavior:

- `Tab` completes the command when there is only one matching option.
- If multiple options are available, the system may list suggestions.
- Suggestions should be based on commands registered in `commands.json`.

---

## 5. Architecture

## 5.1 Architectural Overview

DCMD will be a local Python desktop application composed of independent modules.

The architecture will be organized into the following layers:

1. **Graphical interface**
2. **Global hotkey management**
3. **Command parser**
4. **Command executor**
5. **Configuration manager**
6. **Secure script runner**
7. **Windows integration**

## 5.2 Recommended Stack

### Language

- Python 3.11+

### Graphical Interface

Initial recommendation:

- `PySide6`

Reasons:

- Strong customization capabilities.
- Good support for desktop windows.
- Better fit for a modern interface than plain Tkinter.
- Solid foundation for building a custom terminal-like launcher.

### Global Hotkey

Possible libraries:

- `keyboard`
- `pynput`

The final decision should consider Windows compatibility and behavior after packaging the app as a `.exe`.

### Packaging

- `PyInstaller`

### Configuration

- `.json` files

---

## 5.3 Main Components

### App Bootstrap

Responsible for starting the application.

Responsibilities:

- load settings and command configuration;
- start the graphical application;
- register the global hotkey;
- guarantee a single running instance;
- keep the process running in the background.

### UI Layer

Responsible for the graphical interface.

Responsibilities:

- show the floating window;
- render the session history;
- display the fixed prompt;
- capture user input;
- implement command history navigation;
- implement autocomplete.

### Command Parser

Responsible for interpreting the text typed by the user.

Examples:

```text
yt
search yt gameplays
exec script-1
open vscode
```

Responsibilities:

- identify the command type;
- split arguments;
- validate syntax;
- return a standardized command structure for execution.

### Command Registry

Responsible for loading registered commands from JSON.

Responsibilities:

- read `commands.json`;
- validate available commands;
- provide command lists for autocomplete;
- map aliases to executable actions.

### Command Executor

Responsible for executing valid commands.

Initial command types:

- `open_url`;
- `open_program`;
- `search`;
- `script`.

### Script Runner

Responsible for executing authorized Python scripts.

Rules:

- block scripts outside the `scripts` folder;
- accept only registered scripts;
- accept only `.py` files;
- avoid direct execution of arbitrary shell commands.

### Windows Integration

Responsible for Windows-specific behavior.

Responsibilities:

- configure automatic startup;
- resolve program paths;
- launch executables;
- focus the window;
- guarantee a single DCMD instance.

---

## 5.4 Command Execution Flow

1. The user presses `Ctrl + Shift + J`.
2. DCMD shows or focuses the window.
3. The user types a command.
4. The UI sends the text to the parser.
5. The parser interprets the command.
6. The registry checks whether the command exists.
7. The executor runs the corresponding action.
8. The UI displays a simple success or error message.
9. The command is added to the session history.

---

## 5.5 Example JSON Configuration

Suggested file:

```text
config/commands.json
```

Example:

```json
{
  "browser": {
    "name": "Opera GX",
    "path": "C:/Users/<user>/AppData/Local/Programs/Opera GX/launcher.exe"
  },
  "hotkey": "ctrl+shift+j",
  "commands": {
    "yt": {
      "type": "open_url",
      "url": "https://www.youtube.com"
    },
    "vscode": {
      "type": "open_program",
      "path": "C:/Users/<user>/AppData/Local/Programs/Microsoft VS Code/Code.exe"
    }
  },
  "search_engines": {
    "yt": {
      "name": "YouTube",
      "url_template": "https://www.youtube.com/results?search_query={query}"
    },
    "google": {
      "name": "Google",
      "url_template": "https://www.google.com/search?q={query}"
    },
    "github": {
      "name": "GitHub",
      "url_template": "https://github.com/search?q={query}"
    },
    "reddit": {
      "name": "Reddit",
      "url_template": "https://www.reddit.com/search/?q={query}"
    }
  },
  "scripts": {
    "script-1": {
      "file": "script-1.py",
      "description": "Example script for testing script execution."
    }
  }
}
```

---

## 6. Folder Structure

Recommended initial structure:

```text
DCMD/
  README.md
  requirements.txt
  pyproject.toml
  .gitignore

  docs/
    PROJECT.md
    sprint-01.md
    sprint-02.md
    sprint-03.md
    sprint-04.md
    sprint-05.md

  config/
    commands.json
    settings.json

  scripts/
    script-1.py

  src/
    dcmd/
      __init__.py
      main.py
      app.py

      core/
        __init__.py
        command_parser.py
        command_registry.py
        command_executor.py
        autocomplete.py
        history.py

      ui/
        __init__.py
        main_window.py
        terminal_input.py
        theme.py

      integrations/
        __init__.py
        windows_startup.py
        global_hotkey.py
        process_launcher.py
        single_instance.py

      runners/
        __init__.py
        script_runner.py

      utils/
        __init__.py
        paths.py
        json_loader.py
        validators.py

  tests/
    test_command_parser.py
    test_command_registry.py
    test_autocomplete.py
    test_script_runner.py
```

## 6.1 Folder Descriptions

### `docs/`

Contains the project documentation.

Includes:

- `PROJECT.md`: main project overview and documentation.
- `sprint-01.md` to `sprint-05.md`: detailed documentation for each sprint.

### `config/`

Contains `.json` configuration files.

- `commands.json`: commands, scripts, programs, and search engines.
- `settings.json`: general preferences such as theme, global hotkey, and window behavior.

### `scripts/`

Contains Python scripts authorized for execution by DCMD.

Only scripts inside this folder may be executed.

### `src/dcmd/`

Contains the main application source code.

### `src/dcmd/core/`

Contains the core command logic.

### `src/dcmd/ui/`

Contains the graphical interface.

### `src/dcmd/integrations/`

Contains Windows integrations, global hotkeys, process launching, startup behavior, and single-instance handling.

### `src/dcmd/runners/`

Contains specialized runners, such as the secure script runner.

### `tests/`

Contains automated tests for the main logic.

---

## 7. Roadmap

Development will be divided into 5 sprints.

## Sprint 01 — Project Foundation and Command Parser

### Goal

Create the project foundation, folder structure, and initial command interpretation logic.

### Deliverables

- Create the initial repository structure.
- Create `PROJECT.md`.
- Create sprint documentation files.
- Create the initial `commands.json`.
- Implement JSON configuration loading.
- Implement the initial parser for commands such as:
  - `yt`
  - `search yt gameplays`
  - `exec script-1`
- Implement basic validations.
- Create initial parser tests.

### Expected Result

The project will have a clean foundation and will be able to interpret text commands, even before the final interface exists.

---

## Sprint 02 — Command Executor and Opera GX Integration

### Goal

Implement real execution for registered commands.

### Deliverables

- Implement URL opening in Opera GX.
- Implement opening of registered programs.
- Implement configurable search engines.
- Implement secure execution of Python scripts inside `scripts`.
- Block execution of unregistered scripts.
- Block paths outside the `scripts` folder.
- Create the test script `script-1.py`.

### Expected Result

DCMD will be able to open YouTube, perform searches, open configured programs, and execute authorized Python scripts.

---

## Sprint 03 — Graphical Launcher Interface

### Goal

Create the custom graphical window that simulates a modern terminal.

### Deliverables

- Create the window using PySide6.
- Apply the dark theme with red accents.
- Create the floating launcher layout.
- Add the fixed prompt:

```text
What command do you want to use?
```

- Add the command input field.
- Display visual session history.
- Show simple success and error messages.

### Expected Result

The user will be able to interact with DCMD through a custom graphical interface that feels like a modern terminal launcher.

---

## Sprint 04 — Global Hotkey, History, and Autocomplete

### Goal

Make DCMD usable as a real background launcher.

### Deliverables

- Implement configurable global hotkey.
- Set `Ctrl + Shift + J` as the default hotkey.
- Show or focus the window when the hotkey is pressed.
- Prevent multiple unnecessary window instances.
- Implement command history navigation with the up and down arrow keys.
- Implement autocomplete with `Tab`.
- Integrate autocomplete with commands registered in JSON.

### Expected Result

DCMD will be accessible at any time through the global hotkey and will behave similarly to CMD regarding command input history and navigation.

---

## Sprint 05 — Packaging, Windows Startup, and Polish

### Goal

Prepare DCMD for real Windows usage as an executable application.

### Deliverables

- Configure packaging with PyInstaller.
- Generate the `.exe` file.
- Implement optional startup with Windows.
- Evaluate the Startup folder as the initial solution.
- Improve window focus behavior.
- Improve simple error messages.
- Review documentation.
- Create installation and usage instructions.

### Expected Result

DCMD can be used as a local Windows application, start in the background with the system, and be called through the configured global hotkey.

---

## 8. Decisions

## 8.1 Confirmed Decisions

- The project will be developed only for Windows.
- The main language will be Python.
- The project name will be DCMD.
- The full name will be Dumb Command Prompt.
- The system will run locally.
- No external API will be used.
- No external database will be used.
- The interface will be a custom graphical window that simulates a terminal.
- The visual design will use a black background, white text, and red accents.
- The design will be inspired by modern terminals and Claude Code-like interfaces.
- The app will be activated through a global hotkey.
- The default hotkey will be `Ctrl + Shift + J`.
- The hotkey will be configurable.
- The window must receive focus when called.
- Commands will be configured in `.json` files.
- The primary browser will be Opera GX.
- Executable scripts will be stored in the `scripts` folder.
- Only registered scripts may be executed.
- Persistent command logs will not be required.
- Session command history must work with the up and down arrow keys.
- Autocomplete must be implemented.
- Invalid commands will show a simple error.
- The project must generate a `.exe` in the future.
- Sprint documentation will be stored in separate files inside `docs`.
- `PROJECT.md` will include a short summary of each sprint.
- DCMD must support automatically opening configured programs.

## 8.2 Recommended Technical Decisions

### Interface

Use `PySide6` to create a modern and highly customizable graphical interface.

### Startup with Windows

For the MVP, use the Windows Startup folder for simplicity.

Later, consider Windows Task Scheduler if more control is required.

### Packaging

Use `PyInstaller` to generate the `.exe` executable.

### Configuration

Split configuration into two files:

- `commands.json`: commands, searches, programs, and scripts.
- `settings.json`: hotkey, theme, window size, and general preferences.

### Script Execution

Use `subprocess` with strict path validation.

Important rules:

- resolve the absolute script path;
- verify that the script is inside the `scripts` folder;
- verify that the script is registered;
- verify the `.py` extension;
- execute it with the configured Python interpreter.

---

## 9. Documentation

## 9.1 Main Documents

Project documentation will be stored inside the `docs` folder.

Planned files:

```text
docs/
  PROJECT.md
  sprint-01.md
  sprint-02.md
  sprint-03.md
  sprint-04.md
  sprint-05.md
```

## 9.2 Expected Content for Each Sprint File

Each sprint file should contain:

- sprint goal;
- scope;
- tasks;
- acceptance criteria;
- deliverables;
- decisions made;
- pending items;
- final checklist.

## 9.3 Example Sprint Document Structure

```markdown
# Sprint 01 — Project Foundation and Command Parser

## Goal

Describe the sprint goal.

## Scope

List what is included and what is not included in the sprint.

## Tasks

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Acceptance Criteria

- Criterion 1
- Criterion 2

## Deliverables

- Deliverable 1
- Deliverable 2

## Decisions

- Decision 1

## Pending Items

- Pending item 1
```

---

## 10. Project Success Criteria

The project will be considered successful when:

- DCMD opens or focuses with `Ctrl + Shift + J`.
- The graphical interface is functional and visually aligned with the proposed design.
- The `yt` command opens YouTube in Opera GX.
- The `search yt gameplays` command searches for `gameplays` on YouTube using Opera GX.
- The `exec script-1` command executes an authorized Python script inside `scripts`.
- The system allows registered programs to be opened.
- Command history with arrow keys works correctly.
- Autocomplete works correctly.
- Invalid commands display a simple error message.
- The app can be packaged as a `.exe`.
- The app can start with Windows and run in the background.

---

## 11. Next Steps

1. Create the initial folder structure.
2. Create `commands.json` and `settings.json`.
3. Create the command parser.
4. Implement parser tests.
5. Implement Opera GX opening.
6. Implement secure script execution.
7. Create the initial graphical interface.
8. Implement the global hotkey.
9. Implement autocomplete and command history.
10. Package the app as `.exe`.
