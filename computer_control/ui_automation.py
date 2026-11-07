import sys
sys.coinit_flags = 2
import pythoncom
import pyautogui
from pywinauto import Desktop

class UIAutomation:
    @staticmethod
    def list_open_windows() -> str:
        pythoncom.CoInitialize()
        try:
            windows = Desktop(backend="uia").windows()
            titles = [w.window_text() for w in windows if w.window_text()]
            return "Open windows: " + ", ".join(titles)
        except Exception as e:
            return f"Error listing windows: {e}"
        finally:
            pythoncom.CoUninitialize()

    @staticmethod
    def focus_window(title: str) -> str:
        pythoncom.CoInitialize()
        try:
            app = Desktop(backend="uia").window(title_re=f".*{title}.*")
            app.set_focus()
            return f"Window '{title}' focused successfully."
        except Exception as e:
            return f"Error focusing window '{title}': {e}"
        finally:
            pythoncom.CoUninitialize()

    @staticmethod
    def center_window(title: str) -> str:
        """Zentriert das Fenster auf dem Bildschirm und setzt eine feste Größe."""
        pythoncom.CoInitialize()
        try:
            # Finde das Fenster (Regex, da der Titel sich ständig ändert)
            app = Desktop(backend="uia").window(title_re=f".*{title}.*")
            if not app.exists():
                return "Window not found."
                
            # Bildschirmauflösung holen
            screen_width, screen_height = pyautogui.size()
            
            # Fenstergröße festlegen (z.B. 1200x800)
            win_width = 1200
            win_height = 800
            
            # Position berechnen (Mittelpunkt)
            x = (screen_width - win_width) // 2
            y = (screen_height - win_height) // 2
            
            # Fenster verschieben und skalieren
            app.move_window(x, y, win_width, win_height)
            return f"Window '{title}' centered."
        except Exception as e:
            return f"Error centering window: {e}"
        finally:
            pythoncom.CoUninitialize()

    @staticmethod
    def click_element(window_title: str, element_name: str) -> str:
        pythoncom.CoInitialize()
        try:
            app = Desktop(backend="uia").window(title_re=f".*{window_title}.*")
            app.child_window(title=element_name).click_input()
            return f"Clicked '{element_name}' in window '{window_title}'."
        except Exception as e:
            return f"Error clicking element '{element_name}': {e}"
        finally:
            pythoncom.CoUninitialize()