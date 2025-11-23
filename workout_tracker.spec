# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Workout Tracker

block_cipher = None

a = Analysis(
    ['workout_tracker/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('workout_tracker/requirements.txt', 'workout_tracker'),
        ('workout_tracker.ico', '.'),
    ],
    hiddenimports=[
        'ttkbootstrap',
        'matplotlib',
        'pandas',
        'dateutil',
        'PIL',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WorkoutTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='workout_tracker.ico',  # Custom workout tracker icon
)
