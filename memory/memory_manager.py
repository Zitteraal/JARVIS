"""
Verwaltet Einträge im Langzeitgedächtnis.
Kategorien: personal, preference, project, task, instruction.
"""
from memory.database import Database


VALID_CATEGORIES = ("personal", "preference", "project", "task", "instruction")


class MemoryManager:
    def __init__(self, db: Database):
        self._db = db

    def list_all(self, category: str | None = None) -> list[dict]:
        if category and category in VALID_CATEGORIES:
            rows = self._db.query(
                "SELECT id, category, content, source, created_at FROM memories "
                "WHERE category = ? ORDER BY category ASC, created_at DESC",
                (category,),
            )
        else:
            rows = self._db.query(
                "SELECT id, category, content, source, created_at FROM memories "
                "ORDER BY category ASC, created_at DESC"
            )
        return [self._fmt(r) for r in rows]

    def add(self, category: str, content: str, source: str = "auto") -> int | None:
        if category not in VALID_CATEGORIES:
            return None
        content = content.strip()
        if not content or len(content) > 500:
            return None
        dup = self._db.query(
            "SELECT id FROM memories WHERE category = ? AND LOWER(content) = LOWER(?)",
            (category, content),
        )
        if dup:
            return None
        return self._db.insert_returning_id(
            "INSERT INTO memories (category, content, source) VALUES (?, ?, ?)",
            (category, content, source),
        )

    def update(self, mem_id: int, content: str) -> bool:
        content = content.strip()
        if not content or len(content) > 500:
            return False
        return self._db.execute(
            "UPDATE memories SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (content, mem_id),
        ) > 0

    def delete(self, mem_id: int) -> bool:
        return self._db.execute("DELETE FROM memories WHERE id = ?", (mem_id,)) > 0

    def all_contents(self) -> list[str]:
        rows = self._db.query(
            "SELECT content FROM memories ORDER BY category ASC, created_at DESC"
        )
        return [r["content"] for r in rows]

    @staticmethod
    def _fmt(row) -> dict:
        d = dict(row)
        created = str(d.get("created_at", ""))
        d["created_at"] = created[:16]
        return d