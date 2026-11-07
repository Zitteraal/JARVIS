import os
import win32com.client

class FileManager:
    @staticmethod
    def create_text_file(file_path: str, content: str) -> str:
        try:
            # Wenn der Nutzer "desktop" sagt, fragen wir Windows nach dem echten Pfad
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