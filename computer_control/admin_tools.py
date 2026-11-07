import ctypes
import subprocess
import os
from pathlib import Path

class AdminTools:
    @staticmethod
    def execute_as_admin(command: str) -> str:
        """Führt einen Befehl mit Administratorrechten (UAC) aus."""
        try:
            # 1 = SW_SHOWNORMAL, "runas" triggert den UAC Prompt
            ctypes.windll.shell32.ShellExecuteW(None, "runas", command, None, None, 1)
            return f"Admin command executed: {command}"
        except Exception as e:
            return f"Error executing admin command: {e}"

    @staticmethod
    def uninstall_with_revo(program_name: str) -> str:
        """Sucht Revo Uninstaller und startet die Deinstallation."""
        # Mögliche Standard-Pfade für Revo Uninstaller
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
            return "Error: Revo Uninstaller not found. Please install it or use the standard uninstaller."
            
        try:
            # Revo unterstützt den Parameter /uninstall "Programmname"
            cmd = f'"{revo_exe}" /uninstall "{program_name}"'
            subprocess.Popen(cmd, shell=True)
            return f"Revo Uninstaller launched for '{program_name}'. Please follow the Revo dialogs."
        except Exception as e:
            return f"Error launching Revo: {e}"