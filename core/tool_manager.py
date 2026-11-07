import subprocess
import os
import time
import pyautogui
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
            {"type": "function", "function": {"name": "open_application", "description": "Opens any program or game.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "close_application", "description": "Closes a running program.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "create_web_project", "description": "Creates a full web project on the desktop and opens it in VS Code.", "parameters": {"type": "object", "properties": {"project_name": {"type": "string"}}, "required": ["project_name"]}}},
            
            # Das neue (sichere) Schreib-Tool
            {"type": "function", "function": {"name": "write_code_file", "description": "Writes code directly to a file on the hard drive and opens it in VS Code. Use this for large files to prevent token limits.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}, "code_content": {"type": "string"}}, "required": ["file_path", "code_content"]}}},
            
            {"type": "function", "function": {"name": "list_directory", "description": "Lists the files in a directory.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
            {"type": "function", "function": {"name": "read_text_file", "description": "Reads the content of a file.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}}},
            {"type": "function", "function": {"name": "web_search", "description": "Searches the internet for current information.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
            {"type": "function", "function": {"name": "analyze_disk", "description": "Analyzes hard drives.", "parameters": {"type": "object", "properties": {}, "required": []}}},
            {"type": "function", "function": {"name": "execute_admin_command", "description": "Executes a command with Admin privileges.", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}}
        ]

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name == "open_application":
            app = arguments.get("app_name", "").lower().strip()
            apps = {"vscode": "start code", "code": "start code", "notepad": "notepad", "chrome": "start chrome"}
            subprocess.Popen(apps.get(app, f"start {app}"), shell=True)
            return f"Success: {app.capitalize()} launched."
            
        elif tool_name == "create_web_project":
            return ProjectGenerator.create_web_project(arguments.get("project_name", "NewProject"))

        elif tool_name == "write_code_file":
            file_path = arguments.get("file_path", "").replace("/", "\\")
            code = arguments.get("code_content", "")
            
            try:
                # 1. Datei direkt auf der Festplatte speichern (keine Token-Limits!)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                
                # 2. In VS Code öffnen (damit der Nutzer es sieht)
                subprocess.Popen(f'code -r "{file_path}"', shell=True)
                time.sleep(1.0)
                
                # 3. Fenster zentrieren
                UIAutomation.center_window("Visual Studio Code")
                UIAutomation.focus_window("Visual Studio Code")
                
                return f"Success: Wrote {file_path} directly to disk and opened it in VS Code."
            except Exception as e:
                return f"Error writing code file: {str(e)}"

        elif tool_name == "list_directory":
            items = FileManager.list_directory(arguments.get("path", ""))
            return "\n".join([f"{'[DIR]' if i['is_dir'] else '[FILE]'} {i['path']}" for i in items])
            
        elif tool_name == "read_text_file":
            try:
                with open(arguments.get("file_path", ""), "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                return f"Error reading file: {e}"

        elif tool_name == "web_search":
            return WebSearch.search(arguments.get("query", ""))
            
        elif tool_name == "analyze_disk":
            drives = DiskAnalyzer.get_drive_info()
            return "Drive analysis:\n" + "\n".join([f"- {d['drive']}: {d['free_gb']} GB free out of {d['total_gb']} GB" for d in drives])
            
        elif tool_name == "execute_admin_command":
            return AdminTools.execute_as_admin(arguments.get("command", ""))
            
        return f"Error: Tool '{tool_name}' is unknown."