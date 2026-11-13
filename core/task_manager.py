import logging
from memory.database import Database

log = logging.getLogger("EVOX.TASKS")

class TaskManager:
    def __init__(self, db: Database):
        self._db = db

    def create_task(self, title: str, description: str = "") -> str:
        try:
            task_id = self._db.insert_returning_id(
                "INSERT INTO tasks (title, description, status, progress) VALUES (?, ?, 'planned', 0)",
                (title, description)
            )
            log.success(f"Neue Aufgabe erstellt: '{title}' (ID: {task_id})")
            return f"Task '{title}' created successfully with ID {task_id}."
        except Exception as e:
            log.error(f"Fehler beim Erstellen der Aufgabe: {e}")
            return f"Error creating task: {e}"

    def update_task(self, task_id: int, status: str, progress: int = None) -> str:
        try:
            if progress is not None:
                self._db.execute(
                    "UPDATE tasks SET status = ?, progress = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, progress, task_id)
                )
            else:
                self._db.execute(
                    "UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (status, task_id)
                )
            log.info(f"Aufgabe {task_id} aktualisiert: Status={status}, Fortschritt={progress}%")
            return f"Task {task_id} updated to {status}."
        except Exception as e:
            log.error(f"Fehler beim Aktualisieren der Aufgabe: {e}")
            return f"Error updating task: {e}"

    def list_all_tasks(self) -> str:
        rows = self._db.query("SELECT id, title, status, progress FROM tasks ORDER BY created_at DESC")
        if not rows:
            return "No tasks found."
        
        result = "All Tasks:\n"
        for r in rows:
            result += f"[{r['id']}] {r['title']} - Status: {r['status']} ({r['progress']}%)\n"
        return result
        
    def get_active_tasks(self) -> list:
        """Gibt eine Liste von Dicts für die UI zurück."""
        rows = self._db.query(
            "SELECT id, title, status, progress FROM tasks WHERE status NOT IN ('completed', 'cancelled', 'failed') ORDER BY created_at DESC"
        )
        return [dict(r) for r in rows]