# -*- mode: python -*-
block_cipher = None

a = Analysis(['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('templates', 'templates'), 
        ('static', 'static'),
        ('.env', '.'),
        ('icon.png', '.'),
    ],
    hiddenimports=[
        'pystray', 
        'PIL', 
        'plyer',
        'webview',
        'flask',
        'flask_cors',
        'binance',
        'binance.client',
        'sqlite3',
        'pandas',
        'numpy',
        'requests',
        'dotenv',
        'csv',
        'json',
        'threading',
        'urllib.request',
        'urllib.error'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Trading Bot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico')

coll = COLLECT(exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Trading Bot')