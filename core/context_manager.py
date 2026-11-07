"""
Baut den System-Prompt dynamisch aus dem Basis-Prompt + allen gespeicherten
Erinnerungen zusammen, und schneidet die History auf ein sinnvolles Maß.
"""
from config import settings
from memory.memory_manager import MemoryManager


class ContextManager:
    def __init__(self, memory_manager: MemoryManager):
        self._mm = memory_manager

    def build_system_prompt(self) -> str:
        base = settings.SYSTEM_PROMPT
        memories = self._mm.list_all()
        if not memories:
            return base

        labels = {
            "personal": "Persönliches",
            "preference": "Vorlieben & Arbeitsweise",
            "project": "Projekte",
            "task": "Gewohnheiten & wiederkehrende Aufgaben",
            "instruction": "Direkte Anweisungen",
        }
        by_cat: dict[str, list[str]] = {}
        for m in memories:
            by_cat.setdefault(m["category"], []).append(m["content"])

        parts = [base, "", "== Bekannte Fakten über den Nutzer =="]
        for cat in ("personal", "preference", "project", "task", "instruction"):
            if cat in by_cat:
                parts.append(f"\n{labels[cat]}:")
                for c in by_cat[cat]:
                    parts.append(f"- {c}")
        return "\n".join(parts)

    def build_messages(self, history: list[dict], max_messages: int = 40) -> list[dict]:
        trimmed = history[-max_messages:] if len(history) > max_messages else history
        return [{"role": "system", "content": self.build_system_prompt()}] + trimmed