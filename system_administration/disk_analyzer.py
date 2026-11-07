import psutil
import os

class DiskAnalyzer:
    @staticmethod
    def get_drive_info() -> list:
        """Gibt eine Liste aller Laufwerke und deren Speicherplatz zurück."""
        drives = []
        for part in psutil.disk_partitions():
            if 'cdrom' in part.opts or part.fstype == '':
                continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
                drives.append({
                    "drive": part.device,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": usage.percent
                })
            except PermissionError:
                continue
        return drives

    @staticmethod
    def find_large_folders(path: str, limit: int = 5) -> list:
        """Findet die größten Ordner in einem Verzeichnis (z.B. C:\\Users\\Name)."""
        folders = []
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        size = DiskAnalyzer._get_dir_size(entry.path)
                        folders.append({"path": entry.path, "size_gb": round(size / (1024**3), 2)})
        except Exception:
            pass
        
        # Sortieren nach Größe (absteigend)
        folders.sort(key=lambda x: x["size_gb"], reverse=True)
        return folders[:limit]

    @staticmethod
    def _get_dir_size(start_path: str) -> int:
        """Berechnet die Ordnergröße (iterativ, um Rekursionsfehler zu vermeiden)."""
        total_size = 0
        try:
            for dirpath, _, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except Exception:
            pass
        return total_size