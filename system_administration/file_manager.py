import os
import shutil
import logging
from pathlib import Path
from core.tool_result import ToolResult

log = logging.getLogger("EVOX.FILES")

class FileManager:
    @staticmethod
    def list_directory(path: str) -> list:
        if not path or path == "~": path = os.path.expanduser("~")
        items = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    try:
                        is_dir = entry.is_dir()
                        size = entry.stat().st_size if not is_dir else 0
                        items.append({"name": entry.name, "path": entry.path.replace("\\", "/"), "is_dir": is_dir, "size": size})
                    except Exception: pass
        except Exception: return []
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return items

    @staticmethod
    def delete_file(file_path: str) -> ToolResult:
        try:
            if "desktop" in file_path.lower() or "schreibtisch" in file_path.lower():
                filename = os.path.basename(file_path)
                file_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
            else:
                file_path = os.path.expanduser(file_path)
                
            path = Path(file_path)
            if not path.exists(): return ToolResult.failure(f"File {file_path} not found.")
            if path.is_dir(): shutil.rmtree(path)
            else: path.unlink()
            return ToolResult.success(f"Deleted {file_path}.")
        except Exception as e:
            return ToolResult.failure(f"Error deleting file: {e}")

    @staticmethod
    def copy_file(source: str, destination: str) -> ToolResult:
        try:
            shutil.copy2(source, destination)
            return ToolResult.success(f"Copied {source} to {destination}.")
        except Exception as e:
            return ToolResult.failure(f"Error copying file: {e}")

    @staticmethod
    def move_file(source: str, destination: str) -> ToolResult:
        try:
            shutil.move(source, destination)
            return ToolResult.success(f"Moved {source} to {destination}.")
        except Exception as e:
            return ToolResult.failure(f"Error moving file: {e}")