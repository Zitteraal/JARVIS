"""
Extrahiert nach jeder Antwort Fakten über den Nutzer aus dem Dialog.
Läuft in eigenem Thread, blockiert die UI nicht.
"""
import json
import re

import httpx
from PySide6.QtCore import QObject, Signal

from config import settings


EXTRACTION_PROMPT = """Du bist ein Gedächtnis-Extraktor für einen KI-Assistenten. \
Analysiere den Dialog-Ausschnitt und extrahiere NUR Fakten über den Nutzer, \
die langfristig relevant sind.

Kategorien:
- "personal": Name, Beruf, Wohnort, Familie, Alter, wichtige persönliche Daten
- "preference": Vorlieben, Abneigungen, bevorzugte Tools/Sprachen/Zeiten/Arbeitsweise
- "project": Aktuelle Projekte, Ziele, Deadlines
- "task": Wiederkehrende Aufgaben, Gewohnheiten, Routinen
- "instruction": Explizite Anweisungen des Nutzers ("Nenne mich X", "Antworte immer formell")

Regeln:
- Speichere KEINE Passwörter, API-Keys, Kreditkartennummern oder andere Secrets.
- Speichere KEINE temporären Infos (Uhrzeit, Wetter, einmalige Fragen).
- Speichere KEINE allgemeinen Fakten (Hauptstadt von Frankreich) — nur Fakten ÜBER DEN NUTZER.
- Speichere NUR, was der Nutzer aktiv über sich preisgegeben hat.
- Formuliere jeden Eintrag als kurzen, eigenständigen Satz in der Ich-Perspektive des Nutzers.
  Beispiel: "Mein Name ist Max."
- Ignoriere bereits bekannte Fakten.

Dialog-Ausschnitt:
{exchange}

Bekannte Fakten (nicht erneut extrahieren):
{known}

Antworte ausschließlich mit einem JSON-Objekt:
{{"memories": [{{"category": "...", "content": "..."}}]}}
Wenn nichts Relevantes vorhanden ist: {{"memories": []}}"""


class MemoryExtractor(QObject):
    extracted = Signal(list)  # list[dict] mit {"category", "content"}
    failed = Signal(str)

    def __init__(self, exchange: str, known: list[str], model: str):
        super().__init__()
        self._exchange = exchange
        self._known = known
        self._model = model

    def run(self) -> None:
        known_str = "\n".join(f"- {k}" for k in self._known) if self._known else "(keine)"
        prompt = EXTRACTION_PROMPT.format(exchange=self._exchange, known=known_str)
        try:
            with httpx.Client(timeout=90) as client:
                r = client.post(
                    settings.OLLAMA_CHAT_ENDPOINT,
                    json={
                        "model": self._model,
                        "messages": [{"role": "user", "content": prompt}],
                        "stream": False,
                        "format": "json",
                        "options": {"temperature": 0.1},
                    },
                )
                if r.status_code != 200:
                    self.failed.emit(f"HTTP {r.status_code}")
                    return
                content = r.json().get("message", {}).get("content", "")
                items = self._parse(content)
                if items:
                    self.extracted.emit(items)
        except Exception as exc:
            self.failed.emit(str(exc))

    @staticmethod
    def _parse(text: str) -> list[dict]:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if not m:
                return []
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                return []
        if not isinstance(data, dict):
            return []
        arr = data.get("memories", [])
        if not isinstance(arr, list):
            return []
        valid = {"personal", "preference", "project", "task", "instruction"}
        out = []
        for item in arr:
            if not isinstance(item, dict):
                continue
            cat = str(item.get("category", "")).lower().strip()
            content = str(item.get("content", "")).strip()
            if cat in valid and 3 <= len(content) <= 500:
                out.append({"category": cat, "content": content})
        return out