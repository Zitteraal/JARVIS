import json
import threading
import httpx
from PySide6.QtCore import QObject, Signal
from config import settings
from core.tool_result import ToolResult

class ChatWorker(QObject):
    chunk = Signal(str)
    finished = Signal(str)
    failed = Signal(str)
    confirmRequired = Signal(str, str)
    confirmCancelled = Signal()
    systemMessage = Signal(str)

    def __init__(self, messages: list[dict], model: str, tools: list | None = None):
        super().__init__()
        self._messages = messages
        self._model = model
        self._tools = tools or []
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
                    payload = {
                        "model": self._model,
                        "messages": self._messages,
                        "stream": False
                    }
                    if self._tools:
                        payload["tools"] = self._tools

                    resp = client.post(settings.OLLAMA_CHAT_ENDPOINT, json=payload)
                    
                    if resp.status_code != 200:
                        self.failed.emit(f"Ollama Fehler: HTTP {resp.status_code}")
                        return
                        
                    data = resp.json()
                    message = data.get("message", {})
                    tool_calls = message.get("tool_calls", [])
                    content = message.get("content", "")
                    
                    if tool_calls:
                        tool_executed = True
                        self._messages.append(message)
                        cancelled = False # NEU: Variable für Abbruch
                        
                        for tool_call in tool_calls:
                            function = tool_call.get("function", {})
                            tool_name = function.get("name")
                            arguments = function.get("arguments", {})
                            
                            if isinstance(arguments, str):
                                try:
                                    arguments = json.loads(arguments)
                                except:
                                    arguments = {}

                            if tool_name in ["uninstall_with_revo_visually", "execute_admin_command", "delete_project", "propose_code_fix"]:
                                prog_name = arguments.get("program_name", arguments.get("command", arguments.get("project_name", arguments.get("filename", "Unknown Action"))))
                                self._confirm_event.clear()
                                self._is_confirmed = False
                                
                                self.confirmRequired.emit(tool_name, prog_name)
                                
                                confirmed = self._confirm_event.wait(timeout=120.0)
                                if not confirmed or not self._is_confirmed:
                                    self.confirmCancelled.emit()
                                    result = ToolResult.failure("Action cancelled by user or timeout.")
                                    self._messages.append({"role": "tool", "content": result.to_llm_string()})
                                    self.systemMessage.emit(result.message)
                                    tool_results.append(result)
                                    cancelled = True
                                    break # Bricht die for-Schleife für die Tools ab

                            try:
                                from core.tool_manager import ToolManager
                                result = ToolManager().execute_tool(tool_name, arguments)
                            except Exception as e:
                                result = ToolResult.failure(f"Tool crashed: {type(e).__name__}: {e}")
                            
                            tool_results.append(result)
                            self._messages.append({"role": "tool", "content": result.to_llm_string()})
                            self.systemMessage.emit(result.message)
                        
                        if cancelled:
                            break # Bricht die äußere Iterations-Schleife ab
                        
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
            self.failed.emit(f"Fehler: {exc}")