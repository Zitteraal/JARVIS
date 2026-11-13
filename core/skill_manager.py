import os
import logging
from pathlib import Path
from datetime import datetime

log = logging.getLogger("EVOX.SKILLS")

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
BACKUP_DIR = SKILLS_DIR / "backups"

class SkillManager:
    @staticmethod
    def _ensure_dirs():
        SKILLS_DIR.mkdir(exist_ok=True)
        BACKUP_DIR.mkdir(exist_ok=True)

    @staticmethod
    def save_skill(skill_name: str, content: str) -> str:
        SkillManager._ensure_dirs()
        
        safe_name = "".join(c for c in skill_name if c.isalnum() or c in ('_', '-')).lower()
        if not safe_name:
            return "Error: Invalid skill name."
            
        file_path = SKILLS_DIR / f"{safe_name}.md"
        
        # Backup erstellen, falls der Skill bereits existiert
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = BACKUP_DIR / f"{safe_name}_backup_{timestamp}.md"
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    old_content = f.read()
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(old_content)
                log.info(f"Backup für Skill '{safe_name}' erstellt.")
            except Exception as e:
                log.error(f"Fehler beim Backup für {safe_name}: {e}")
                
        # Neuen Skill speichern
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            log.success(f"Skill '{safe_name}' erfolgreich gespeichert.")
            return f"Success: Skill '{safe_name}' has been learned and saved."
        except Exception as e:
            log.error(f"Fehler beim Speichern des Skills '{safe_name}': {e}")
            return f"Error saving skill: {e}"

    @staticmethod
    def read_skill(skill_name: str) -> str:
        safe_name = "".join(c for c in skill_name if c.isalnum() or c in ('_', '-')).lower()
        file_path = SKILLS_DIR / f"{safe_name}.md"
        
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading skill: {e}"
        return f"Skill '{safe_name}' not found."

    @staticmethod
    def list_skills() -> str:
        SkillManager._ensure_dirs()
        skills = [f.stem for f in SKILLS_DIR.glob("*.md")]
        if not skills:
            return "No skills learned yet."
        
        result = "Available Skills:\n"
        for s in skills:
            result += f"- {s}\n"
        return result