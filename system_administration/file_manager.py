import os
import win32com.client
from pathlib import Path

class FileManager:
    @staticmethod
    def create_text_file(file_path: str, content: str) -> str:
        try:
            if "desktop" in file_path.lower() or "schreibtisch" in file_path.lower():
                shell = win32com.client.Dispatch("WScript.Shell")
                desktop_path = shell.SpecialFolders("Desktop")
                filename = os.path.basename(file_path)
                file_path = os.path.join(desktop_path, filename)
            else:
                file_path = os.path.expanduser(file_path)
            
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            return f"Success: File created successfully at {file_path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"

    @staticmethod
    def list_directory(path: str) -> list:
        """Listet den Inhalt eines Ordners auf."""
        if not path or path == "~":
            path = os.path.expanduser("~")
        
        items = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    try:
                        is_dir = entry.is_dir()
                        size = entry.stat().st_size if not is_dir else 0
                        items.append({
                            "name": entry.name,
                            "path": entry.path.replace("\\", "/"),
                            "is_dir": is_dir,
                            "size": size
                        })
                    except Exception:
                        pass
        except Exception as e:
            return []
            
        # Ordner nach oben, dann alphabetisch sortieren
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return items