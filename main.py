import sys
import os
import ctypes
import logging
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QSharedMemory

from config import settings
from core.logging_setup import setup_logging

log = logging.getLogger("evox.main")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def handle_qml_warnings(warnings):
    for w in warnings:
        log.warning("QML: %s", w.toString())

def main() -> int:
    log_file = setup_logging()
    log.info("EVOX %s startet (Programm: %s)", settings.APP_VERSION, settings.BASE_DIR)

    # 1. SINGLE INSTANCE CHECK (Muss VOR dem Admin-Check passieren!)
    shared_mem = QSharedMemory("EVOX_SingleInstance_Lock")
    if shared_mem.attach():
        log.warning("EVOX läuft bereits. Beende diesen Startversuch.")
        return 0
    if not shared_mem.create(1):
        log.error("Konnte SharedMemory nicht erstellen.")
        return 1

    # 2. ADMIN CHECK
    if not is_admin():
        print("Fordere Administratorrechte an...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    try:
        myappid = "EVOX.PersonalIntelligenceWorkspace"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception as e:
        log.warning("AppUserModelID konnte nicht gesetzt werden: %s", e)

    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")

    app = QGuiApplication(sys.argv)
    app.setApplicationName(settings.APP_NAME)
    app.setOrganizationName("EVOX Systems")
    app.setApplicationVersion(settings.APP_VERSION)

    base_dir = settings.BASE_DIR
    icon_path = base_dir / "assets" / "evox_app_icon.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    from interface.backend import Backend
    backend = Backend()

    engine = QQmlApplicationEngine()
    engine.warnings.connect(handle_qml_warnings)

    qml_dir = base_dir / "interface" / "qml"
    engine.addImportPath(str(qml_dir))

    engine.rootContext().setContextProperty("backend", backend)
    engine.load(QUrl.fromLocalFile(str(qml_dir / "main.qml")))

    if not engine.rootObjects():
        log.critical("QML konnte nicht geladen werden.")
        return -1

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())