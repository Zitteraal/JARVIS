import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# 1. Custom SUCCESS Level erstellen (liegt zwischen INFO und WARNING)
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)

# Fügt die .success() Methode zu jedem Logger hinzu
logging.Logger.success = success

def setup_logging() -> Path:
    """Richtet das Logging ein und gibt den Pfad zur Logdatei zurück."""
    
    # Log-Verzeichnis im AppData-Ordner
    log_dir = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "EVOX" / "Logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "evox.log"

    # Format: [13:42:01] [INFO] [EVOX] Nachricht
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    date_format = "%H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # Root Logger konfigurieren
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG) 

    # Verhindere doppelte Handler bei mehrfachem Aufruf
    if root_logger.handlers:
        return log_file

    # 1. Console Handler (Live-Ausgabe im Terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 2. File Handler (Speichert in evox.log mit Rotation)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Externe Bibliotheken etwas ruhiger stellen
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("pywinauto").setLevel(logging.WARNING)

    return log_file