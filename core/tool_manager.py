import subprocess
import os
import time
from system_administration.disk_analyzer import DiskAnalyzer
from system_administration.program_manager import ProgramManager
from system_administration.report_generator import ReportGenerator
from system_administration.file_manager import FileManager
from computer_control.pc_control import PCControl
from computer_control.ui_automation import UIAutomation
from computer_control.admin_tools import AdminTools

class ToolManager:
    def __init__(self):
        pass

    def get_tools_definition(self) -> list:
        return [
            # --- SYSTEM ADMINISTRATION ---
            {
                "type": "function",
                "function": {
                    "name": "open_application",
                    "description": "Opens any program or game.",
                    "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}
                }
            },

            {
                "type": "function",
                "function": {
                    "name": "get_system_stats",
                    "description": "Returns real-time CPU, RAM, and GPU usage percentages.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "close_application",
                    "description": "Closes a running program.",
                    "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_text_file",
                    "description": "Creates a new text file and writes content to it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string"},
                            "content": {"type": "string"}
                        },
                        "required": ["file_path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "uninstall_with_revo",
                    "description": "Uninstalls a program using Revo Uninstaller.",
                    "parameters": {"type": "object", "properties": {"program_name": {"type": "string"}}, "required": ["program_name"]}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_admin_command",
                    "description": "Executes a command with Administrator privileges (UAC).",
                    "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_disk",
                    "description": "Analyzes hard drives and free space.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            },
            
            # --- PC CONTROL ---
            {
                "type": "function",
                "function": {
                    "name": "open_app_and_type",
                    "description": "Opens a program and immediately types text into it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "app_name": {"type": "string"},
                            "text": {"type": "string"}
                        },
                        "required": ["app_name", "text"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "move_mouse",
                    "description": "Moves the mouse to specific screen coordinates (X, Y).",
                    "parameters": {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}}, "required": ["x", "y"]}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "mouse_click",
                    "description": "Clicks the mouse.",
                    "parameters": {"type": "object", "properties": {"button": {"type": "string", "enum": ["left", "right", "double"]}}, "required": ["button"]}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "type_text",
                    "description": "Types text using the keyboard into the currently focused window.",
                    "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}
                }
            },
            
            # --- UI AUTOMATION ---
            {
                "type": "function",
                "function": {
                    "name": "focus_window",
                    "description": "Brings a specific window to the foreground.",
                    "parameters": {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_open_windows",
                    "description": "Lists all currently open windows.",
                    "parameters": {"type": "object", "properties": {}, "required": []}
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        app_name = arguments.get("app_name", "").lower().strip()
        
        # Hier ist das fehlende Komma behoben:
        open_apps = {
            "steam": "start steam://open/main", 
            "cs": "start steam://rungameid/730",
            "cs2": "start steam://rungameid/730", 
            "chrome": "start chrome",
            "browser": "start chrome", 
            "edge": "start msedge",
            "rechner": "calc", 
            "calculator": "calc", 
            "notepad": "notepad",
            "explorer": "explorer", 
            "files": "explorer", 
            "cmd": "start cmd",
            "terminal": "start powershell",
            "vscode": "start code",
            "code": "start code"
        }
        
        close_apps = {
            "steam": "steam.exe", 
            "cs": "cs2.exe", 
            "cs2": "cs2.exe",
            "chrome": "chrome.exe", 
            "browser": "chrome.exe", 
            "edge": "msedge.exe",
            "rechner": "CalculatorApp.exe", 
            "calculator": "CalculatorApp.exe",
            "notepad": "notepad.exe", 
            "explorer": "explorer.exe", 
            "cmd": "cmd.exe",
            "vscode": "Code.exe"
        }

        if tool_name == "open_application":
            cmd = open_apps.get(app_name, f"start {app_name}")
            subprocess.Popen(cmd, shell=True)
            time.sleep(1.5)
            return f"Success: {app_name.capitalize()} launched."
                
        elif tool_name == "close_application":
            process_name = close_apps.get(app_name, f"{app_name}.exe")
            subprocess.run(["taskkill", "/F", "/T", "/IM", process_name], capture_output=True)
            return f"Success: {app_name.capitalize()} closed."

        elif tool_name == "create_text_file":
            return FileManager.create_text_file(arguments.get("file_path", ""), arguments.get("content", ""))

        elif tool_name == "analyze_disk":
            drives = DiskAnalyzer.get_drive_info()
            return "Drive analysis:\n" + "\n".join([f"- {d['drive']}: {d['free_gb']} GB free out of {d['total_gb']} GB" for d in drives])

        elif tool_name == "uninstall_with_revo":
            return AdminTools.uninstall_with_revo(arguments.get("program_name", ""))

        elif tool_name == "get_system_stats":
            import psutil
            import pynvml
            
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            gpu = 0.0
            
            try:
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            except:
                pass
                
            return f"Live System Stats:\nCPU: {cpu}%\nRAM: {ram}%\nGPU: {gpu}%\n"
            
        elif tool_name == "execute_admin_command":
            return AdminTools.execute_as_admin(arguments.get("command", ""))

        # --- PC CONTROL ---
        elif tool_name == "open_app_and_type":
            app = arguments.get("app_name", "").lower().strip()
            text = arguments.get("text", "")
            cmd = open_apps.get(app, f"start {app}")
            try:
                subprocess.Popen(cmd, shell=True)
                time.sleep(2.5)
                from computer_control.ui_automation import UIAutomation
                UIAutomation.focus_window(app)
                from computer_control.pc_control import PCControl
                PCControl.type_text(text)
                return f"Success: Opened {app} and typed the text."
            except Exception as e:
                return f"Error: {str(e)}"

        elif tool_name == "move_mouse":
            return PCControl.move_mouse(arguments.get("x", 0), arguments.get("y", 0))
        elif tool_name == "mouse_click":
            btn = arguments.get("button", "left")
            if btn == "double":
                return PCControl.click_mouse() + " " + PCControl.click_mouse()
            return PCControl.click_mouse(btn)
        elif tool_name == "type_text":
            return PCControl.type_text(arguments.get("text", ""))

        # --- UI AUTOMATION ---
        elif tool_name == "list_open_windows":
            return UIAutomation.list_open_windows()
        elif tool_name == "focus_window":
            return UIAutomation.focus_window(arguments.get("title", ""))
        
        return f"Error: Tool '{tool_name}' is unknown."