import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5 

class PCControl:
    @staticmethod
    def move_mouse(x: int, y: int) -> str:
        try:
            pyautogui.moveTo(x, y, duration=0.5)
            return f"Mouse moved to {x}, {y}."
        except Exception as e:
            return f"Error moving mouse: {e}"

    @staticmethod
    def click_mouse(button: str = "left") -> str:
        try:
            pyautogui.click(button=button)
            return f"Mouse clicked ({button})."
        except Exception as e:
            return f"Error clicking mouse: {e}"

    @staticmethod
    def type_text(text: str) -> str:
        try:
            time.sleep(0.5)
            pyautogui.write(text, interval=0.01) 
            return "Text typed successfully."
        except Exception as e:
            return f"Error typing text: {e}"

    @staticmethod
    def press_hotkey(keys: list) -> str:
        try:
            pyautogui.hotkey(*keys)
            return f"Hotkey pressed: {'+'.join(keys)}."
        except Exception as e:
            return f"Error pressing hotkey: {e}"

    @staticmethod
    def press_key(key: str) -> str:
        try:
            pyautogui.press(key)
            return f"Key pressed: {key}."
        except Exception as e:
            return f"Error pressing key: {e}"

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
            return f"Visually opened {app_name} and maximized it."
        except Exception as e:
            return f"Error visually opening {app_name}: {e}"

    @staticmethod
    def write_in_notepad(filename: str, text: str) -> str:
        """Öffnet Notepad, tippt den Text und speichert die Datei."""
        try:
            # 1. Notepad öffnen
            pyautogui.press('win')
            time.sleep(0.8)
            pyautogui.write("notepad", interval=0.05)
            time.sleep(0.8)
            pyautogui.press('enter')
            time.sleep(2.5)
            pyautogui.hotkey('win', 'up') # Maximieren
            
            # 2. Text tippen
            pyautogui.write(text, interval=0.01)
            time.sleep(1.0)
            
            # 3. Speichern (Strg + S)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(1.5) # Warten bis der Speichern-Dialog offen ist
            
            # 4. Dateinamen eingeben (z.B. "trees.txt")
            if not filename.endswith(".txt"):
                filename += ".txt"
            pyautogui.write(filename, interval=0.05)
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1.0)
            
            return f"Success: Typed text in Notepad and saved as {filename}."
        except Exception as e:
            return f"Error in Notepad: {e}"