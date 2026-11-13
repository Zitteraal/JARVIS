import os
import glob
import win32com.client
from difflib import SequenceMatcher

class AppDiscovery:
    @staticmethod
    def _get_start_menu_paths():
        return [
            os.path.join(os.environ["ProgramData"], r"Microsoft\Windows\Start Menu\Programs"),
            os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs")
        ]

    @staticmethod
    def _resolve_shortcut(lnk_path):
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            return shell.CreateShortCut(lnk_path).Targetpath
        except Exception:
            return None

    @staticmethod
    def find_app_by_name(app_name: str) -> str:
        app_name = app_name.lower().strip()
        best_match = None
        highest_score = 0.0

        for base_path in AppDiscovery._get_start_menu_paths():
            for lnk_file in glob.glob(os.path.join(base_path, "**", "*.lnk"), recursive=True):
                filename = os.path.basename(lnk_file).replace(".lnk", "").lower()
                score = SequenceMatcher(None, app_name, filename).ratio()
                if app_name in filename: score += 0.5
                if score > highest_score:
                    highest_score = score
                    best_match = lnk_file

        if highest_score > 0.6 and best_match:
            target_exe = AppDiscovery._resolve_shortcut(best_match)
            if target_exe and os.path.exists(target_exe):
                return target_exe
        return None