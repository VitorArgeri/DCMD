from pathlib import Path

from dcmd.integrations.windows_startup import (
    STARTUP_FILE_NAME,
    WATCHDOG_FILE_NAME,
    WindowsStartupManager,
    load_startup_enabled,
    startup_directory,
)


def test_startup_directory_uses_windows_roaming_path() -> None:
    appdata_path = Path("C:/Users/test/AppData/Roaming")
    result = startup_directory(appdata_path)
    assert result == (
        appdata_path
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
    )


def test_load_startup_enabled_defaults_to_false(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("{}", encoding="utf-8")
    assert load_startup_enabled(settings_path) is False


def test_load_startup_enabled_reads_true_flag(tmp_path: Path) -> None:
    settings_path = tmp_path / "settings.json"
    settings_path.write_text('{"startup": {"enabled": true}}', encoding="utf-8")
    assert load_startup_enabled(settings_path) is True


def test_enable_writes_startup_launcher_file(tmp_path: Path) -> None:
    manager = WindowsStartupManager(tmp_path)
    entry_path = manager.enable(("C:/DCMD/DCMD.exe",), Path("C:/DCMD"))
    assert entry_path == tmp_path / STARTUP_FILE_NAME
    assert entry_path.exists()
    contents = entry_path.read_text(encoding="utf-8")
    assert "powershell.exe" in contents
    assert WATCHDOG_FILE_NAME in contents


def test_enable_writes_watchdog_script(tmp_path: Path) -> None:
    manager = WindowsStartupManager(tmp_path)
    manager.enable(("C:/DCMD/DCMD.exe", "--background"), Path("C:/DCMD"))
    contents = manager.watchdog_path().read_text(encoding="utf-8")
    assert "$executable = 'C:/DCMD/DCMD.exe'" in contents
    assert "$arguments = @('--background')" in contents
    assert "$workingDirectory = 'C:\\DCMD'" in contents
    assert "watchdog.log" in contents
    assert "Write-WatchdogLog" in contents
    assert "while ($true)" in contents


def test_disable_removes_only_dcmd_launcher_file(tmp_path: Path) -> None:
    manager = WindowsStartupManager(tmp_path)
    other_file = tmp_path / "Other.cmd"
    other_file.write_text("echo other", encoding="utf-8")
    manager.enable(("C:/DCMD/DCMD.exe",), Path("C:/DCMD"))
    manager.disable()
    assert manager.entry_path().exists() is False
    assert manager.watchdog_path().exists() is False
    assert other_file.exists() is True
