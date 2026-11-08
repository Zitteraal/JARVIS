import sys
import os
import ctypes
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QSharedMemory

from config import settings
from interface.backend import Backend

def is_admin():
    """Prüft, ob das Skript mit Administratorrechten läuft."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main() -> int:
    # 1. ADMIN CHECK & NEUSTART
    if not is_admin():
        print("Fordere Administratorrechte an...")
        # Startet die aktuelle Python-Datei mit 'runas' (UAC Prompt)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0) # Beendet den nicht-Admin Prozess

    # 2. WINDOWS APP ID (Eigenständige Taskleiste)
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("EVOX.PersonalIntelligenceWorkspace")
    except Exception as e:
        print(f"AppUserModelID Fehler: {e}")

    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

    app = QGuiApplication(sys.argv)
    app.setApplicationName("EVOX")
    app.setOrganizationName("EVOX Systems")
    app.setApplicationVersion("1.0.0")

    # 3. SINGLE INSTANCE CHECK
    shared_mem = QSharedMemory("EVOX_SingleInstance_Lock")
    if shared_mem.attach():
        print("EVOX läuft bereits. Beende diesen Startversuch.")
        return 0
    if not shared_mem.create(1):
        print("Konnte SharedMemory nicht erstellen.")
        return 1

    # 4. ICON LADEN
    icon_path = settings.BASE_DIR / "assets" / "evox_app_icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    backend = Backend()

    engine = QQmlApplicationEngine()

    qml_dir = settings.BASE_DIR / "interface" / "qml"
    engine.addImportPath(str(qml_dir))
    engine.rootContext().setContextProperty("backend", backend)

    engine.load(QUrl.fromLocalFile(str(qml_dir / "main.qml")))

    if not engine.rootObjects():
        print("FEHLER: QML konnte nicht geladen werden.", file=sys.stderr)
        return -1

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())