# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('venv_mp/lib/python3.11/site-packages/mediapipe/modules', 'mediapipe/modules')],
    hiddenimports=[
        'mediapipe',
        'cv2',
        'PIL',
        'numpy',
        'tkinter',
        'mido',
        'mido.backends',
        'mido.backends.rtmidi',
        'rtmidi',
        'threading',
        'json',
        'math',
        'time'
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
    [],
    exclude_binaries=True,
    name='Air MIDI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Air MIDI',
)

app = BUNDLE(
    coll,
    name='Air MIDI.app',
    icon=None,
    bundle_identifier='com.airmidi.handgesture',
    info_plist={
        'CFBundleName': 'Air MIDI',
        'CFBundleDisplayName': 'Air MIDI - Hand Gesture MIDI Controller',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.airmidi.handgesture',
        'NSCameraUsageDescription': 'Air MIDI uses your camera to detect hand gestures for MIDI control.',
        'NSMicrophoneUsageDescription': 'Air MIDI may access audio devices for MIDI output.',
        'LSMinimumSystemVersion': '10.13',
        'CFBundleExecutable': 'Air MIDI',
        'CFBundleIconFile': 'icon.icns',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,
    },
)