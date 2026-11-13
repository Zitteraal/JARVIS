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

    def __init__(self, messages, model, tools=None, is_online=False):
        super().__init__()
        self._messages = messages
        self._model = model
        self._tools = tools or []
        self._is_online = is_online
        self._confirm_event = threading.Event()
        self._is_confirmed = False

    def set_confirmation(self, confirmed):
        self._is_confirmed = confirmed
        self._confirm_event.set()

    def run(self):
        full = ""
        tool_executed = False
        tool_results = []
        
        try:
            with httpx.Client(timeout=120) as client:
                for iteration in range(5):
                    payload = {"model": self._model, "messages": self._messages, "stream": False}
                    if self._tools: payload["tools"] = self._tools

                    resp = client.post(settings.OLLAMA_CHAT_ENDPOINT, json=payload)
                    if resp.status_code != 200:
                        self.failed.emit(f"Ollama HTTP {resp.status_code}")
                        return
                        
                    data = resp.json()
                    message = data.get("message", {})
                    tool_calls = message.get("tool_calls", [])
                    content = message.get("content", "")

                    if tool_calls:
                        tool_executed = True
                        self._messages.append(message)
                        cancelled = False
                        
                        for tool_call in tool_calls:
                            func = tool_call.get("function", {})
                            tool_name = func.get("name")
                            args = func.get("arguments", {})
                            if isinstance(args, str):
                                try: args = json.loads(args)
                                except: args = {}

                            # SICHERHEITSSPERRE
                            if tool_name in ["uninstall_with_revo_visually", "execute_admin_command", "delete_project", "propose_code_fix"]:
                                self._confirm_event.clear()
                                self._is_confirmed = False
                                self.confirmRequired.emit(tool_name, args.get("program_name", args.get("filename", "Unknown")))
                                confirmed = self._confirm_event.wait(timeout=120.0)
                                if not confirmed or not self._is_confirmed:
                                    self.confirmCancelled.emit()
                                    result = ToolResult.failure("Action cancelled by user or timeout.")
                                    self._messages.append({"role": "tool", "content": result.to_llm_string()})
                                    self.systemMessage.emit(result.message)
                                    tool_results.append(result)
                                    cancelled = True
                                    break

                            # AUSFÜHREN
                            from core.tool_manager import ToolManager
                            result = ToolManager().execute_tool(tool_name, args)
                            
                            # REFLEXIONS-LOOP (Lernen aus Fehlern)
                            if result.status == "failed":
                                log.warning(f"Tool {tool_name} fehlgeschlagen. Starte Reflexion...")
                                reflexion_prompt = f"Deine letzte Aktion '{tool_name}' ist fehlgeschlagen. Fehler: {result.message}. Analysiere den Fehler, erstelle eine kurze Lektion und speichere sie mit 'save_skill' ab (Name: lesson_{tool_name}), bevor du weitermachst."
                                self._messages.append({"role": "system", "content": reflexion_prompt})
                            
                            tool_results.append(result)
                            self._messages.append({"role": "tool", "content": result.to_llm_string()})
                            self.systemMessage.emit(result.message)
                        
                        if cancelled: break
                        continue
                    else:
                        full = content
                        break
                        
            if not full.strip():
                if tool_executed and tool_results:
                    s = sum(1 for r in tool_results if r.status == "success")
                    u = sum(1 for r in tool_results if r.status == "unverified")
                    f = sum(1 for r in tool_results if r.status == "failed")
                    full = f"Summary: {s} succeeded, {u} unverified, {f} failed."
                else: full = "Action cancelled."
                    
            self.chunk.emit(full)
            self.finished.emit(full)
        except Exception as exc:
            self.failed.emit(f"Fehler: {exc}")