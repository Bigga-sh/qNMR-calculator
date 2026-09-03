# PyInstaller runtime hook — set Qt WebEngine paths before anything starts
import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    meipass = Path(getattr(sys, "_MEIPASS", str(Path(sys.executable).parent)))
    qt6 = meipass / "PyQt6" / "Qt6"

    # Tell Qt WebEngine where its subprocess executable lives
    we_exe = qt6 / "bin" / "QtWebEngineProcess.exe"
    if we_exe.exists():
        os.environ.setdefault("QTWEBENGINEPROCESS_PATH", str(we_exe))

    # Explicitly set resource and locale paths so the subprocess finds pak files
    we_res = qt6 / "resources"
    if we_res.exists():
        os.environ.setdefault("QTWEBENGINE_RESOURCES_PATH", str(we_res))

    we_loc = qt6 / "translations" / "qtwebengine_locales"
    if we_loc.exists():
        os.environ.setdefault("QTWEBENGINE_LOCALES_PATH", str(we_loc))

    # Disable GPU and sandbox (common crash sources in PyInstaller bundles).
    # --disable-logging suppresses Chromium stderr so no console window pops up
    # when QtWebEngineProcess.exe is spawned.
    os.environ.setdefault(
        "QTWEBENGINE_CHROMIUM_FLAGS",
        "--disable-gpu --disable-gpu-compositing --no-sandbox --disable-logging",
    )
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")

    # Ensure Qt can find its plugins (platform, imageformats, etc.)
    qt_plugins = qt6 / "plugins"
    if qt_plugins.exists():
        existing = os.environ.get("QT_PLUGIN_PATH", "")
        if str(qt_plugins) not in existing:
            os.environ["QT_PLUGIN_PATH"] = (
                str(qt_plugins) + (os.pathsep + existing if existing else "")
            )
