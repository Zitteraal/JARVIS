import pythoncom
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