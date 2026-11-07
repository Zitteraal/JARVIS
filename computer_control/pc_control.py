import pyautogui
import time

# Sicherheitsfeature von PyAutoGUI: Wenn die Maus in die obere linke Ecke (0,0) gezogen wird, bricht es ab.
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5 # Kurze Pause zwischen Aktionen

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
            pyautogui.write(text, interval=0.05)
            return "Text typed successfully."
        except Exception as e:
            return f"Error typing text: {e}"

    @staticmethod
    def press_hotkey(keys: list) -> str:
        try:
            # keys könnte z.B. ["ctrl", "c"] sein
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