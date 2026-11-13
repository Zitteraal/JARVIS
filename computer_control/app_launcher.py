import subprocess
import time
import pyautogui
from pywinauto import Desktop

class AppLauncher:
    @staticmethod
    def launch_safely_and_visually(app_name: str) -> str:
        app_map = {
            "notepad": "notepad.exe", "chrome": "chrome.exe",
            "vscode": "code.cmd", "code": "code.cmd",
            "explorer": "explorer.exe", "rechner": "calc.exe", "calculator": "calc.exe"
        }
        exe = app_map.get(app_name.lower(), f"{app_name}.exe")

        try:
            subprocess.Popen([exe])
        except FileNotFoundError:
            return f"FAILED: Das Programm '{app_name}' wurde nicht gefunden."
        except Exception as e:
            return f"FAILED: Fehler beim Starten von {app_name}: {e}"

        time.sleep(3.0) # Warten bis das Fenster geladen ist

        try:
            # Sucht das Fenster anhand des Namens (funktioniert besser als PID)
            desktop = Desktop(backend="uia")
            # Sucht ein Fenster, das den App-Namen im Titel hat (z.B. "Unbenannt - Notepad")
            win = desktop.window(title_re=f"(?i).*{app_name}.*")
            
            if win.exists():
                win.set_focus()
                time.sleep(0.5)
                win.maximize()
                time.sleep(0.5)
                return f"SUCCESS (verified): {app_name} wurde geöffnet und maximiert."
            else:
                # Fallback falls der Fenstertitel nicht gefunden wird
                pyautogui.hotkey('win', 'up')
                return f"SUCCESS (unverified): {app_name} wurde gestartet (Maximierung via Tastatur)."
        except Exception as e:
            pyautogui.hotkey('win', 'up')
            return f"UNVERIFIED: {app_name} gestartet. Maximierung via Tastatur-Fallback."