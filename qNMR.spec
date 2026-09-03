# -*- mode: python ; coding: utf-8 -*-
import glob
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# RDKit data files (fingerprint tables, SMARTS, font maps, etc.)
rdkit_datas = collect_data_files('rdkit', excludes=['**/__pycache__/*', '**/*.py'])
rdkit_bins  = collect_dynamic_libs('rdkit')

# Conda puts RDKit C++ DLLs in Library\bin — PyInstaller can't auto-detect them
_conda_lib = r'C:\Users\acasagrande\AppData\Local\anaconda3\envs\chem\Library\bin'
_rdkit_dlls = glob.glob(rf'{_conda_lib}\RDKit*.dll')
_rdkit_dlls += glob.glob(rf'{_conda_lib}\boost_python*.dll')
_rdkit_dlls += glob.glob(rf'{_conda_lib}\boost_numpy*.dll')
# Pillow / imaging DLLs also conda-managed
_imaging_patterns = [
    'libwebp*.dll', 'lcms2.dll', 'jpeg*.dll', 'libjpeg*.dll',
    'libtiff*.dll', 'tiff.dll', 'openjp2.dll', 'zlib.dll',
    'libpng*.dll', 'freetype.dll',
]
for pat in _imaging_patterns:
    _rdkit_dlls += glob.glob(rf'{_conda_lib}\{pat}')
rdkit_bins += [(dll, '.') for dll in _rdkit_dlls]

a = Analysis(
    ['qNMR_gui.py'],
    pathex=[r'c:\Users\acasagrande\Desktop\projects\qNMR calculator'],
    binaries=rdkit_bins,
    datas=rdkit_datas + [
        (r'resources', 'resources'),
        (r'qNMRicon.ico', '.'),
    ],
    hiddenimports=[
        'qNMR',
        'rdkit',
        'rdkit.Chem',
        'rdkit.Chem.Draw',
        'rdkit.Chem.Descriptors',
        'PIL',
        'PIL.ImageQt',
        'openpyxl',
        'openpyxl.styles',
        'PyQt6.QtWebEngineCore',
        'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtSvg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyi_rth_webengine.py'],
    # Exclude heavy packages we don't need
    excludes=['matplotlib', 'scipy', 'pandas', 'tkinter', 'notebook',
              'IPython', 'jupyter', 'wx', 'PyQt5', 'PySide2', 'PySide6'],
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
    name='qNMR_Calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,          # Skip UPX — Qt DLLs don't compress well and it can break things
    console=False,      # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=r'qNMRicon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='qNMR_Calculator',
)
