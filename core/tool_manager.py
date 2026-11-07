import subprocess
import os
import time
from system_administration.disk_analyzer import DiskAnalyzer
from system_administration.program_manager import ProgramManager
from system_administration.report_generator import ReportGenerator
from system_administration.file_manager import FileManager
from system_administration.project_generator import ProjectGenerator
from computer_control.pc_control import PCControl
from computer_control.ui_automation import UIAutomation
from computer_control.admin_tools import AdminTools
from internet.web_search import WebSearch

class ToolManager:
    def __init__(self):
        pass

    def get_tools_definition(self) -> list:
        return [
            # --- SYSTEM & FILES ---
            {"type": "function", "function": {"name": "open_application", "description": "Opens any program or game.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "close_application", "description": "Closes a running program.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "create_text_file", "description": "Creates a new text file or OVERWRITES an existing one.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}, "content": {"type": "string"}}, "required": ["file_path", "content"]}}},
            {"type": "function", "function": {"name": "read_text_file", "description": "Reads the content of a file. Use this to see existing code.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}}},
            {"type": "function", "function": {"name": "list_directory", "description": "Lists the files in a directory. Use this to see the project structure.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
            
            # --- INTERNET & SOFTWARE ---
            {"type": "function", "function": {"name": "web_search", "description": "Searches the internet for current information.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
            {"type": "function", "function": {"name": "create_web_project", "description": "Creates a full web project on the desktop and opens it in VS Code.", "parameters": {"type": "object", "properties": {"project_name": {"type": "string"}}, "required": ["project_name"]}}},
            {"type": "function", "function": {"name": "delete_project", "description": "Deletes an existing web project folder. Requires user confirmation.", "parameters": {"type": "object", "properties": {"project_name": {"type": "string"}}, "required": ["project_name"]}}},

            # --- SYSTEM ADMIN ---
            {"type": "function", "function": {"name": "analyze_disk", "description": "Analyzes hard drives.", "parameters": {"type": "object", "properties": {}, "required": []}}},
            {"type": "function", "function": {"name": "execute_admin_command", "description": "Executes a command with Admin privileges.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
            {"type": "function", "function": {"name": "uninstall_with_revo", "description": "Uninstalls a program using Revo.", "parameters": {"type": "object", "properties": {"program_name": {"type": "string"}}, "required": ["program_name"]}}},
            
            # --- PC CONTROL ---
            {"type": "function", "function": {"name": "open_app_and_type", "description": "Opens a program and types text.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}, "text": {"type": "string"}}, "required": ["app_name", "text"]}}},
            {"type": "function", "function": {"name": "move_mouse", "description": "Moves the mouse.", "parameters": {"type": "object", "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}}, "required": ["x", "y"]}}},
            {"type": "function", "function": {"name": "mouse_click", "description": "Clicks the mouse.", "parameters": {"type": "object", "properties": {"button": {"type": "string", "enum": ["left", "right", "double"]}}, "required": ["button"]}}}
        ]

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        app_name = arguments.get("app_name", "").lower().strip()
        
        open_apps = {"steam": "start steam://open/main", "cs": "start steam://rungameid/730", "cs2": "start steam://rungameid/730", "chrome": "start chrome", "browser": "start chrome", "edge": "start msedge", "rechner": "calc", "calculator": "calc", "notepad": "notepad", "explorer": "explorer", "files": "explorer", "cmd": "start cmd", "terminal": "start powershell", "vscode": "start code", "code": "start code"}
        close_apps = {"steam": "steam.exe", "cs": "cs2.exe", "cs2": "cs2.exe", "chrome": "chrome.exe", "browser": "chrome.exe", "edge": "msedge.exe", "rechner": "CalculatorApp.exe", "calculator": "CalculatorApp.exe", "notepad": "notepad.exe", "explorer": "explorer.exe", "cmd": "cmd.exe", "vscode": "Code.exe"}

        if tool_name == "open_application":
            subprocess.Popen(open_apps.get(app_name, f"start {app_name}"), shell=True)
            time.sleep(1.5)
            return f"Success: {app_name.capitalize()} launched."
        elif tool_name == "close_application":
            subprocess.run(["taskkill", "/F", "/T", "/IM", close_apps.get(app_name, f"{app_name}.exe")], capture_output=True)
            return f"Success: {app_name.capitalize()} closed."
        elif tool_name == "create_text_file":
            return FileManager.create_text_file(arguments.get("file_path", ""), arguments.get("content", ""))
        elif tool_name == "read_text_file":
            try:
                with open(arguments.get("file_path", ""), "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {e}"
        elif tool_name == "list_directory":
            items = FileManager.list_directory(arguments.get("path", ""))
            return "\n".join([f"{'[DIR]' if i['is_dir'] else '[FILE]'} {i['path']}" for i in items])
            
        elif tool_name == "web_search":
            return WebSearch.search(arguments.get("query", ""))
        elif tool_name == "create_web_project":
            return ProjectGenerator.create_web_project(arguments.get("project_name", "NewProject"))
        elif tool_name == "delete_project":
            return FileManager.delete_project(arguments.get("project_name", ""))

        elif tool_name == "analyze_disk":
            drives = DiskAnalyzer.get_drive_info()
            return "Drive analysis:\n" + "\n".join([f"- {d['drive']}: {d['free_gb']} GB free out of {d['total_gb']} GB" for d in drives])
        elif tool_name == "execute_admin_command":
            return AdminTools.execute_as_admin(arguments.get("command", ""))
        elif tool_name == "uninstall_with_revo":
            return AdminTools.uninstall_with_revo(arguments.get("program_name", ""))

        elif tool_name == "open_app_and_type":
            app = arguments.get("app_name", "").lower().strip()
            text = arguments.get("text", "")
            cmd = open_apps.get(app, f"start {app}")
            try:
                subprocess.Popen(cmd, shell=True)
                time.sleep(2.5)
                UIAutomation.focus_window(app)
                PCControl.type_text(text)
                return f"Success: Opened {app} and typed the text."
            except Exception as e:
                return f"Error: {str(e)}"
        elif tool_name == "move_mouse":
            return PCControl.move_mouse(arguments.get("x", 0), arguments.get("y", 0))
        elif tool_name == "mouse_click":
            btn = arguments.get("button", "left")
            if btn == "double": return PCControl.click_mouse() + " " + PCControl.click_mouse()
            return PCControl.click_mouse(btn)
        
        return f"Error: Tool '{tool_name}' is unknown."