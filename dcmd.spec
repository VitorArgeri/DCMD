# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

pyside6_datas = collect_data_files("PySide6")

a = Analysis(
    ["src/dcmd/main.py"],
    pathex=["src"],
    binaries=[],
    datas=[
        ("config", "config"),
        ("scripts", "scripts"),
        *pyside6_datas,
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name="DCMD",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="DCMD",
    contents_directory=".",
)
