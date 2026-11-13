import logging
import json
import threading
import httpx
from PySide6.QtCore import QObject, Signal
from config import settings
from core.tool_result import ToolResult

log = logging.getLogger("EVOX.AI")

class ChatWorker(QObject):
    chunk = Signal(str)
    finished = Signal(str)
    failed = Signal(str)
    confirmRequired = Signal(str, str)
    confirmCancelled = Signal()
    systemMessage = Signal(str)

    def __init__(self, messages: list[dict], model: str, tools: list | None = None, is_online: bool = False):
        super().__init__()
        self._messages = messages
        self._model = model
        self._tools = tools or []
        self._is_online = is_online
        self._confirm_event = threading.Event()
        self._is_confirmed = False

    def set_confirmation(self, confirmed: bool):
        self._is_confirmed = confirmed
        self._confirm_event.set()

    def run(self) -> None:
        full = ""
        tool_executed = False
        tool_results = []
        
        try:
            with httpx.Client(timeout=120) as client:
                for iteration in range(5):
                    log.debug(f"KI-Anfrage Iteration {iteration + 1} an Ollama...")
                    payload = {
                        "model": self._model,
                        "messages": self._messages,
                        "stream": False
                    }
                    if self._tools:
                        payload["tools"] = self._tools

                    resp = client.post(settings.OLLAMA_CHAT_ENDPOINT, json=payload)
                    
                    if resp.status_code != 200:
                        log.error(f"Ollama API Fehler: HTTP {resp.status_code}")
                        self.failed.emit(f"Ollama Fehler: HTTP {resp.status_code}")
                        return
                        
                    data = resp.json()
                    message = data.get("message", {})
                    tool_calls = message.get("tool_calls", [])
                    content = message.get("content", "")
                    
                    if content:
                        log.info(f"KI generiert Text: {content[:100]}...")

                    if tool_calls:
                        tool_executed = True
                        self._messages.append(message)
                        cancelled = False 
                        
                        for tool_call in tool_calls:
                            function = tool_call.get("function", {})
                            tool_name = function.get("name")
                            arguments = function.get("arguments", {})
                            
                            log.info(f"KI ruft Tool auf: {tool_name} mit Argumenten: {arguments}")
                            
                            if isinstance(arguments, str):
                                try:
                                    arguments = json.loads(arguments)
                                except:
                                    arguments = {}

                            if tool_name in ["uninstall_with_revo_visually", "execute_admin_command", "delete_project", "propose_code_fix", "delete_file"]:
                                self._confirm_event.clear()
                                self._is_confirmed = False
                                
                                # Der Fix, damit der richtige Name/das richtige Argument im Popup steht
                                prog_name = arguments.get("program_name") or arguments.get("file_path") or arguments.get("filename") or arguments.get("command") or arguments.get("project_name") or "Unknown Action"
                                
                                self.confirmRequired.emit(tool_name, prog_name)
                                
                                log.warning(f"Warte auf Bestätigung für {tool_name} ({prog_name})...")
                                confirmed = self._confirm_event.wait(timeout=120.0)
                                if not confirmed or not self._is_confirmed:
                                    log.error(f"Aktion abgebrochen durch Timeout oder Nutzer für {tool_name}.")
                                    self.confirmCancelled.emit()
                                    result = ToolResult.failure("Action cancelled by user or timeout.")
                                    self._messages.append({"role": "tool", "content": result.to_llm_string()})
                                    self.systemMessage.emit(result.message)
                                    tool_results.append(result)
                                    cancelled = True
                                    break

                            if tool_name == "web_search" and not self._is_online:
                                log.warning("Web-Suche blockiert: EVOX ist im Offline-Modus.")
                                result = ToolResult.failure("Web search is disabled while EVOX is in OFFLINE mode.")
                                tool_results.append(result)
                                self._messages.append({"role": "tool", "content": result.to_llm_string()})
                                self.systemMessage.emit(result.message)
                                continue

                            log.debug(f"Führe Tool '{tool_name}' aus...")
                            try:
                                from core.tool_manager import ToolManager
                                tm = ToolManager()
                                result = tm.execute_tool(tool_name, arguments)
                                if result.status == "success":
                                    log.success(f"Tool '{tool_name}' erfolgreich. Ergebnis: {result.message}")
                                elif result.status == "unverified":
                                    log.warning(f"Tool '{tool_name}' unverifiziert. Ergebnis: {result.message}")
                                else:
                                    log.error(f"Tool '{tool_name}' fehlgeschlagen. Fehler: {result.message}")
                            except Exception as e:
                                log.exception(f"Schwerwiegender Fehler bei Tool '{tool_name}':")
                                result = ToolResult.failure(f"Tool crashed: {type(e).__name__}: {e}")
                            
                            tool_results.append(result)
                            self._messages.append({"role": "tool", "content": result.to_llm_string()})
                            self.systemMessage.emit(result.message)
                        
                        if cancelled:
                            break 
                        
                        continue 
                    else:
                        full = content
                        break
                        
            if not full.strip():
                if tool_executed and tool_results:
                    successes = sum(1 for r in tool_results if r.status == "success")
                    unverified = sum(1 for r in tool_results if r.status == "unverified")
                    failures = sum(1 for r in tool_results if r.status == "failed")
                    summary = f"Summary: {successes} succeeded, {unverified} unverified, {failures} failed."
                    full = summary
                else:
                    full = "Action cancelled."
                    
            self.chunk.emit(full)
            self.finished.emit(full)
            
        except Exception as exc:
            log.exception("Unerwarteter Fehler im ChatWorker:")
            self.failed.emit(f"Fehler: {exc}")