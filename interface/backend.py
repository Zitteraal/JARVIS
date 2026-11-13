import logging
import threading
import os
from datetime import datetime
import httpx, psutil, pynvml
from PySide6.QtCore import QObject, Property, QTimer, Signal, Slot

from config import settings
from core import ai_engine
from core.context_manager import ContextManager
from memory.database import Database
from memory.memory_manager import MemoryManager
from memory.extractor import MemoryExtractor
from core.task_manager import TaskManager
from voice.text_to_speech import TextToSpeech
from voice.speech_to_text import VoiceAssistant
from system_administration.file_manager import FileManager

log = logging.getLogger("EVOX.BACKEND")

class Backend(QObject):
    responseChunk = Signal(str)
    responseFinished = Signal(str)
    responseError = Signal(str)
    historyChanged = Signal()
    historyReloaded = Signal()
    stateChanged = Signal()
    ollamaStatusChanged = Signal()
    systemStatsChanged = Signal()
    timeChanged = Signal()
    memoryChanged = Signal()
    memoryAdded = Signal(str)
    confirmRequested = Signal(str)
    confirmCancelled = Signal()
    systemMessageAdded = Signal(str)
    textRecognized = Signal(str)
    onlineModeChanged = Signal(bool)
    tasksChanged = Signal()

    def __init__(self):
        super().__init__()
        log.info("Backend initialisiert.")
        self._db = Database()
        self._mm = MemoryManager(self._db)
        self._cm = ContextManager(self._mm)
        self._tm = TaskManager(self._db)
        self._tts = TextToSpeech()
        self._voice = VoiceAssistant()
        self._voice.transcriptionReady.connect(self.textRecognized.emit) 
        self._voice.listeningChanged.connect(self._on_listening_changed)
        self._is_listening = False
        self._is_online = False 

        self._conversation_id = self._ensure_active_conversation()
        self._history = self._load_history()
        self._state = "idle"
        self._ollama_ok = False
        self._ollama_message = "Prüfe Verbindung..."
        self._cpu = self._ram = self._gpu = 0.0
        self._thread = None
        self._worker = None
        
        try:
            pynvml.nvmlInit()
            self._nvml_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self._has_gpu = True
        except Exception: 
            self._has_gpu = False

        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._tick)
        self._stats_timer.start(1000)

        self._ollama_timer = QTimer(self)
        self._ollama_timer.timeout.connect(self._check_ollama_async)
        self._ollama_timer.start(30000)
        self._check_ollama_async()

    def _ensure_active_conversation(self):
        existing = self._db.get_setting("current_conversation_id")
        if existing:
            row = self._db.query_one("SELECT id FROM conversations WHERE id = ?", (int(existing),))
            if row: return int(existing)
        new_id = self._db.insert_returning_id("INSERT INTO conversations DEFAULT VALUES")
        self._db.set_setting("current_conversation_id", str(new_id))
        return new_id

    def _load_history(self):
        rows = self._db.query("SELECT role, content FROM messages WHERE conversation_id = ? AND role IN ('user', 'assistant') ORDER BY id ASC", (self._conversation_id,))
        return [{"role": r["role"], "content": r["content"]} for r in rows]

    def _tick(self):
        try:
            self._cpu = psutil.cpu_percent(interval=None)
            self._ram = psutil.virtual_memory().percent
            if self._has_gpu:
                try: self._gpu = float(pynvml.nvmlDeviceGetUtilizationRates(self._nvml_handle).gpu)
                except: self._gpu = 0.0
        except: pass
        self.systemStatsChanged.emit()
        self.timeChanged.emit()

    def _set_state(self, new_state):
        if new_state != self._state:
            self._state = new_state
            self.stateChanged.emit()

    def _check_ollama_async(self):
        threading.Thread(target=self._check_ollama_worker, daemon=True).start()

    def _check_ollama_worker(self):
        try:
            r = httpx.get(settings.OLLAMA_TAGS_ENDPOINT, timeout=2.0)
            if r.status_code == 200:
                if any(settings.OLLAMA_MODEL.split(":")[0] in m.get("name", "") for m in r.json().get("models", [])):
                    self._ollama_ok, self._ollama_message = True, f"Verbunden · {settings.OLLAMA_MODEL} bereit"
                    log.success(f"Ollama verbunden. Modell '{settings.OLLAMA_MODEL}' ist bereit.")
                else:
                    self._ollama_ok, self._ollama_message = True, "Verbunden · Modell fehlt"
            else:
                self._ollama_ok, self._ollama_message = False, f"HTTP {r.status_code}"
        except: 
            self._ollama_ok, self._ollama_message = False, "Offline"
        self.ollamaStatusChanged.emit()

    @Slot()
    def refreshOllamaStatus(self): self._check_ollama_async()

    @Slot()
    def toggleOnlineMode(self):
        self._is_online = not self._is_online
        self.onlineModeChanged.emit(self._is_online)
        status = "ONLINE" if self._is_online else "OFFLINE"
        self.systemMessageAdded.emit(f"System mode switched to {status}.")
        log.info(f"Online-Modus geändert: {status}")

    @Slot(str)
    def sendMessage(self, text):
        text = text.strip()
        if not text or self._thread is not None: return
        
        log.info(f"Neue Benutzereingabe empfangen: '{text}'")
        
        self._db.insert_returning_id("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'user', ?)", (self._conversation_id, text))
        self._history.append({"role": "user", "content": text})
        self.historyChanged.emit()
        self._set_state("thinking")
        
        from core.tool_manager import ToolManager
        tm = ToolManager()
        tools = tm.get_tools_definition(is_online=self._is_online)
        
        worker = ai_engine.ChatWorker(self._cm.build_messages(self._history), settings.OLLAMA_MODEL, tools=tools, is_online=self._is_online)
        self._worker = worker
        
        worker.chunk.connect(self.responseChunk)
        worker.finished.connect(self._on_worker_finished)
        worker.failed.connect(self._on_worker_failed)
        worker.confirmRequired.connect(self._on_confirm_required)
        worker.confirmCancelled.connect(self.confirmCancelled.emit)
        worker.systemMessage.connect(self.systemMessageAdded.emit)

        self._thread = threading.Thread(target=worker.run, daemon=True)
        self._thread.start()

    @Slot()
    def startListening(self): self._voice.start_recording()
    @Slot()
    def stopListening(self): self._voice.stop_recording()

    def _on_listening_changed(self, is_listening):
        self._is_listening = is_listening
        self.systemStatsChanged.emit()

    @Slot(bool)
    def respondToConfirmation(self, confirmed):
        if self._worker: self._worker.set_confirmation(confirmed)

    def _on_confirm_required(self, tool_name: str, arg: str) -> None:
        log.warning(f"Kritische Aktion angefordert: {tool_name} ({arg}). Warte auf Bestätigung...")
        self.confirmRequested.emit(arg)

    @Slot()
    def clearHistory(self):
        new_id = self._db.insert_returning_id("INSERT INTO conversations DEFAULT VALUES")
        self._db.set_setting("current_conversation_id", str(new_id))
        self._conversation_id = new_id
        self._history = []
        self.historyChanged.emit()
        self.historyReloaded.emit()
        log.info("Chat-Verlauf geleert.")

    @Slot(result="QVariantList")
    def getCurrentMessages(self):
        rows = self._db.query("SELECT role, content, created_at FROM messages WHERE conversation_id = ? AND role IN ('user', 'assistant') ORDER BY id ASC", (self._conversation_id,))
        return [{"role": r["role"], "content": r["content"], "time": str(r["created_at"])[11:16]} for r in rows]

    def _on_worker_finished(self, full):
        log.success("KI-Antwort vollständig generiert.")
        self._history.append({"role": "assistant", "content": full})
        self._db.insert_returning_id("INSERT INTO messages (conversation_id, role, content) VALUES (?, 'assistant', ?)", (self._conversation_id, full))
        self.historyChanged.emit()
        self._set_state("idle")
        self.responseFinished.emit(full)
        self._thread = None
        self._worker = None
        if full.strip(): 
            self._tts.speak(full)
        self.tasksChanged.emit() # UI-Update triggern, falls Task geändert
        self._maybe_extract_memories()

    def _on_worker_failed(self, error):
        log.error(f"KI-Worker Fehler: {error}")
        self._set_state("error")
        self.responseError.emit(error)
        self._thread = None
        self._worker = None
        QTimer.singleShot(4000, lambda: self._set_state("idle"))

    def _maybe_extract_memories(self):
        if not settings.MEMORY_EXTRACTION_ENABLED or len(self._history) < 2: return
        u, a = self._history[-2], self._history[-1]
        if u["role"] != "user" or a["role"] != "assistant" or len(u["content"]) < settings.MEMORY_MIN_USER_LEN: return
        
        extractor = MemoryExtractor(f"Nutzer: {u['content']}\nAssistent: {a['content'][:800]}", self._mm.all_contents(), settings.OLLAMA_MODEL)
        extractor.extracted.connect(self._on_memories_extracted)
        threading.Thread(target=extractor.run, daemon=True).start()

    def _on_memories_extracted(self, items):
        added = False
        for item in items:
            if self._mm.add(item["category"], item["content"], source="auto"):
                added = True
                self.memoryAdded.emit(item["content"])
        if added: self.memoryChanged.emit()

    @Slot(int, str)
    def updateMemory(self, mem_id, content):
        if self._mm.update(mem_id, content): self.memoryChanged.emit()
    @Slot(int)
    def deleteMemory(self, mem_id):
        if self._mm.delete(mem_id): self.memoryChanged.emit()
    
    @Slot(result=str)
    def getHomeDirectory(self): 
        import os
        return os.path.expanduser("~").replace("\\", "/")
    @Slot(str, result="QVariantList")
    def listDirectory(self, path): return FileManager.list_directory(path)

    @Property(str, notify=stateChanged)
    def state(self): return self._state
    @Property(bool, notify=ollamaStatusChanged)
    def ollamaOk(self): return self._ollama_ok
    @Property(str, notify=ollamaStatusChanged)
    def ollamaMessage(self): return self._ollama_message
    @Property(float, notify=systemStatsChanged)
    def cpuPercent(self): return self._cpu
    @Property(float, notify=systemStatsChanged)
    def ramPercent(self): return self._ram
    @Property(float, notify=systemStatsChanged)
    def gpuPercent(self): return self._gpu
    @Property(bool, notify=systemStatsChanged)
    def isListening(self): return self._is_listening
    @Property(bool, notify=onlineModeChanged)
    def isOnline(self): return self._is_online
    @Property(str, notify=timeChanged)
    def currentTime(self): return datetime.now().strftime("%H:%M:%S")
    @Property(str, notify=timeChanged)
    def currentDate(self): return datetime.now().strftime("%A · %d.%m.%Y")
    @Property(str, constant=True)
    def modelName(self): return settings.OLLAMA_MODEL
    @Property("QVariantList", notify=memoryChanged)
    def memories(self): return self._mm.list_all()
    @Property(int, notify=memoryChanged)
    def memoryCount(self): return len(self._mm.list_all())
    
    @Property("QVariantList", notify=tasksChanged)
    def activeTasks(self): return self._tm.get_active_tasks()   