"""
EVOX – Personal Intelligence Workspace
Einstiegspunkt. Startet die Qt/QML-Anwendung.
"""
import sys
import os
import ctypes
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

from interface.backend import Backend

def main() -> int:
    # 1. WINDOWS APP ID (Verhindert das Python-Logo in der Taskleiste)
    try:
        myappid = "EVOX.PersonalIntelligenceWorkspace"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        print(f"AppUserModelID konnte nicht gesetzt werden: {e}")

    # QtQuick Controls im "Basic"-Stil
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

    app = QGuiApplication(sys.argv)
    app.setApplicationName("EVOX")
    app.setOrganizationName("EVOX Systems")
    app.setApplicationVersion("1.0.0")

    # 2. DAS EVOX ICON LADEN
    base_dir = Path(__file__).parent
    icon_path = base_dir / "assets" / "evox_app_icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    else:
        print(f"Warnung: EVOX Icon nicht gefunden unter {icon_path}")

    backend = Backend()

    engine = QQmlApplicationEngine()

    # QML-Importpfade
    qml_dir = base_dir / "interface" / "qml"
    engine.addImportPath(str(qml_dir))

    # Backend als globales Objekt in QML verfügbar machen
    engine.rootContext().setContextProperty("backend", backend)

    # Hauptfenster laden
    engine.load(QUrl.fromLocalFile(str(qml_dir / "main.qml")))

    if not engine.rootObjects():
        print("FEHLER: QML konnte nicht geladen werden.", file=sys.stderr)
        return -1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())