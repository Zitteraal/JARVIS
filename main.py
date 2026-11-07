"""
J.A.R.V.I.S. – Persönlicher KI-Assistent
Einstiegspunkt. Startet die Qt/QML-Anwendung und verbindet
das Python-Backend mit der QML-Oberfläche.
"""
import sys
import os
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

from interface.backend import Backend


def main() -> int:
    # QtQuick Controls im "Basic"-Stil (stylebar, plattformunabhängig)
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

    app = QGuiApplication(sys.argv)
    app.setApplicationName("J.A.R.V.I.S.")
    app.setOrganizationName("JARVIS")
    app.setApplicationVersion("0.1.0")

    backend = Backend()

    engine = QQmlApplicationEngine()

    # QML-Importpfade
    qml_dir = Path(__file__).parent / "interface" / "qml"
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