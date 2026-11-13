import pyautogui
import time

class PCControl:
    # ... (Claudes bestehende Funktionen bleiben hier) ...

    @staticmethod
    def open_app_visually(app_name: str) -> str:
        """Öffnet ein Programm über die Windows-Suche und maximiert es."""
        try:
            pyautogui.press('win')
            time.sleep(0.8) 
            pyautogui.write(app_name, interval=0.05)
            time.sleep(0.8) 
            pyautogui.press('enter')
            time.sleep(2.5)
            pyautogui.hotkey('win', 'up')
            time.sleep(0.5)
            return f"Success: Visually opened {app_name} and maximized it."
        except Exception as e:
            return f"Error visually opening {app_name}: {e}"

    @staticmethod
    def write_in_notepad(filename: str, text: str) -> str:
        """Öffnet Notepad, tippt den Text und speichert die Datei."""
        try:
            pyautogui.press('win')
            time.sleep(0.8)
            pyautogui.write("notepad", interval=0.05)
            time.sleep(0.8)
            pyautogui.press('enter')
            time.sleep(2.5)
            pyautogui.hotkey('win', 'up') 
            
            pyautogui.write(text, interval=0.01)
            time.sleep(1.0)
            
            pyautogui.hotkey('ctrl', 's')
            time.sleep(1.5) 
            
            if not filename.endswith(".txt"):
                filename += ".txt"
            pyautogui.write(filename, interval=0.05)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1.0)
            
            return f"Success: Typed text in Notepad and saved as {filename}."
        except Exception as e:
            return f"Error in Notepad: {e}"