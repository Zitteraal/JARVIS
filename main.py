import sys
import os
import ctypes
import logging
import threading
from pathlib import Path

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QSharedMemory

from config import settings
from core.logging_setup import setup_logging

log = logging.getLogger("EVOX.MAIN")
_IS_SHUTTING_DOWN = False

def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    log.critical("EVOX ist unerwartet abgestürzt!", exc_info=(exc_type, exc_value, exc_traceback))

def handle_thread_exception(args):
    log.critical(
        f"Absturz im Hintergrund-Thread '{args.thread.name if args.thread else 'Unknown'}':",
        exc_info=(args.exc_type, args.exc_value, args.exc_traceback)
    )

sys.excepthook = handle_uncaught_exception
threading.excepthook = handle_thread_exception

def handle_qml_warnings(warnings):
    global _IS_SHUTTING_DOWN
    # Wenn EVOX gerade beendet wird, ignorieren wir die Abschalt-Warnungen von Qt
    if _IS_SHUTTING_DOWN:
        return
        
    for w in warnings:
        log.warning("QML: %s", w.toString())

def main() -> int:
    log_file = setup_logging()
    log.info("EVOX %s startet (Programm: %s)", settings.APP_VERSION, settings.BASE_DIR)

    # 1. SINGLE INSTANCE CHECK
    shared_mem = QSharedMemory("EVOX_SingleInstance_Lock")
    if shared_mem.attach():
        log.warning("EVOX läuft bereits. Beende diesen Startversuch.")
        return 0
    if not shared_mem.create(1):
        log.error("Konnte SharedMemory nicht erstellen.")
        return 1

    # 2. WINDOWS APP ID
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
    app.backend = backend

    # --- DISCORD RICH PRESENCE STARTEN ---
    from core.discord_presence import DiscordPresence
    discord = DiscordPresence(client_id="1570908710396633199", logo_key="evox_logo")
    discord.start()
    # --- ENDE DISCORD ---

    engine = QQmlApplicationEngine()
    engine.warnings.connect(handle_qml_warnings)

    qml_dir = base_dir / "interface" / "qml"
    engine.addImportPath(str(qml_dir))

    engine.rootContext().setContextProperty("backend", backend)
    engine.load(QUrl.fromLocalFile(str(qml_dir / "main.qml")))

    if not engine.rootObjects():
        log.critical("QML konnte nicht geladen werden.")
        return -1

    def on_quit():
        global _IS_SHUTTING_DOWN
        _IS_SHUTTING_DOWN = True
        log.info("EVOX wird vom Benutzer geschlossen...")
        log.info("EVOX-Prozess vollständig beendet.")
    
    app.aboutToQuit.connect(on_quit)

    # Die App läuft, bis sie geschlossen wird
    exit_code = app.exec()
    
    # Wir lassen Python das Aufräumen übernehmen.
    return exit_code

if __name__ == "__main__":
    sys.exit(main())