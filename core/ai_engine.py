import json
import threading
import httpx
from PySide6.QtCore import QObject, Signal
from config import settings

class ChatWorker(QObject):
    chunk = Signal(str)
    finished = Signal(str)
    failed = Signal(str)
    confirmRequired = Signal(str, str)
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
                        
                        for tool_call in tool_calls:
                            function = tool_call.get("function", {})
                            tool_name = function.get("name")
                            arguments = function.get("arguments", {})
                            
                            # --- ROBUSTE JSON VERARBEITUNG ---
                            if isinstance(arguments, str):
                                try:
                                    arguments = json.loads(arguments)
                                except Exception as e:
                                    print(f"JSON PARSE ERROR: {e}")
                                    print(f"RAW ARGUMENTS: {arguments}")
                                    arguments = {}
                            # ---------------------------------

                            if tool_name in ["uninstall_with_revo", "execute_admin_command", "uninstall_program", "delete_project"]:
                                prog_name = arguments.get("program_name", arguments.get("command", arguments.get("project_name", "Unknown Action")))
                                self._confirm_event.clear()
                                self._is_confirmed = False
                                
                                self.confirmRequired.emit(tool_name, prog_name)
                                self._confirm_event.wait() 
                                
                                if not self._is_confirmed:
                                    result = "Action cancelled by user."
                                    self._messages.append({"role": "tool", "content": result})
                                    self.systemMessage.emit(result)
                                    continue

                            from core.tool_manager import ToolManager
                            tm = ToolManager()
                            result = tm.execute_tool(tool_name, arguments)
                            
                            self._messages.append({
                                "role": "tool",
                                "content": result
                            })
                            self.systemMessage.emit(result)
                        
                        continue 
                    else:
                        full = content
                        break
                        
            if not full.strip():
                if tool_executed:
                    full = "Action completed successfully, Sir."
                else:
                    full = "I am ready for your next command, Sir."
                    
            self.chunk.emit(full)
            self.finished.emit(full)
            
        except Exception as exc:
            self.failed.emit(f"Fehler: {exc}")