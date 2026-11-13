import subprocess
import os
import ctypes

class AdminTools:
    @staticmethod
    def execute_as_admin(command: str) -> str:
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", command, None, None, 1)
            return f"Admin command executed: {command}"
        except Exception as e:
            return f"Error executing admin command: {e}"

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
            subprocess.Popen(revo_exe)
            return "Success: Launched Revo Uninstaller."
        except Exception as e:
            return f"Error launching Revo: {e}"

    @staticmethod
    def check_command(command: str) -> str | None:
        # Wird von Claudes Sicherheitsmodul erwartet
        return None