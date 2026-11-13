import subprocess
import os
import ctypes
import logging

log = logging.getLogger("EVOX.ADMIN")

class AdminTools:
    @staticmethod
    def execute_as_admin(command: str) -> str:
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", command, None, None, 1)
            return f"Admin command executed: {command}"
        except Exception as e:
            log.error(f"Fehler beim Admin-Befehl: {e}")
            return f"Error executing admin command: {e}"

    @staticmethod
    def launch_revo_admin() -> str:
        revo_paths = [
            r"C:\Program Files\VS Revo Group\Revo Uninstaller\RevoUnin.exe",
            r"C:\Program Files (x86)\VS Revo Group\Revo Uninstaller\RevoUnin.exe",
            r"C:\Program Files\VS Revo Group\Revo Uninstaller Pro\RevoUninPro.exe",
            r"C:\Program Files (x86)\VS Revo Group\Revo Uninstaller Pro\RevoUninPro.exe"
        ]
        
        revo_exe = None
        for p in revo_paths:
            if os.path.exists(p):
                revo_exe = p
                break
                
        if not revo_exe:
            log.error("Revo Uninstaller nicht gefunden.")
            return "Error: Revo Uninstaller not found."
            
        try:
            # Fordert UAC-Prompt an (nur für Revo)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", revo_exe, None, None, 1)
            log.info("UAC-Prompt für Revo Uninstaller angefordert.")
            return "Success: Requested Admin privileges for Revo Uninstaller."
        except Exception as e:
            log.error(f"Fehler beim Starten von Revo: {e}")
            return f"Error launching Revo: {e}"

    @staticmethod
    def check_command(command: str) -> str | None:
        return None