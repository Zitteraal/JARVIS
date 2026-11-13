import os
import subprocess
import logging
from pathlib import Path
from datetime import datetime

log = logging.getLogger("EVOX.EVOLUTION")
BASE_DIR = Path(__file__).resolve().parent.parent

class SelfEvolver:
    @staticmethod
    def read_own_code(filename: str) -> str:
        """EVOX liest seinen eigenen Quellcode."""
        file_path = BASE_DIR / filename
        if file_path.exists() and file_path.suffix == ".py":
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading code: {e}"
        return f"Error: File '{filename}' not found or not a Python file."

    @staticmethod
    def propose_code_fix(filename: str, new_code: str) -> str:
        """Bereitet eine Code-Änderung in einem sicheren Git-Branch vor."""
        file_path = BASE_DIR / filename
        if not file_path.exists():
            return "Error: File does not exist."
            
        try:
            # 1. Aktuellen Branch merken
            current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=BASE_DIR, text=True).strip()
            
            # 2. Neuen Branch erstellen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            branch_name = f"evox_evolution_{timestamp}"
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=BASE_DIR, check=True, capture_output=True)
            log.info(f"Evolution-Branch erstellt: {branch_name}")
            
            # 3. Code schreiben
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_code)
                
            # 4. Commit
            subprocess.run(["git", "add", filename], cwd=BASE_DIR, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", f"EVOX Self-Evolution: Fix {filename}"], cwd=BASE_DIR, check=True, capture_output=True)
            log.success(f"Codeänderung in Branch '{branch_name}' committet.")
            
            # 5. Zurück zum Hauptbranch (Sicherheit)
            subprocess.run(["git", "checkout", current_branch], cwd=BASE_DIR, check=True, capture_output=True)
            
            return f"Success: Code fix prepared in Git branch '{branch_name}'. The main branch remains unchanged. Please review the changes manually."
            
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode('utf-8') if isinstance(e.stderr, bytes) else str(e.stderr)
            log.error(f"Git Error: {err}")
            return f"Git Error: {err}"
        except Exception as e:
            log.error(f"Error during self-evolution: {e}")
            return f"Error: {str(e)}"