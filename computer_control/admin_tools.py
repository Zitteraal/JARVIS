import subprocess
import os

class AdminTools:
    @staticmethod
    def execute_as_admin(command: str) -> str:
        try:
            # Da EVOX bereits Admin ist, können wir Befehle direkt ausführen
            subprocess.Popen(command, shell=True)
            return f"Command executed: {command}"
        except Exception as e:
            return f"Error executing command: {e}"

    @staticmethod
    def launch_revo_admin() -> str:
        """Startet Revo Uninstaller. Da EVOX Admin ist, gibt es keinen UAC-Prompt mehr."""
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
            return "Error: Revo Uninstaller not found."
            
        try:
            # Startet Revo. Da EVOX schon Admin ist, ploppt KEIN UAC auf.
            subprocess.Popen(revo_exe)
            return "Success: Launched Revo Uninstaller with inherited Admin rights."
        except Exception as e:
            return f"Error launching Revo: {e}"