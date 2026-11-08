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
            {"type": "function", "function": {"name": "open_application", "description": "Opens any program visibly on the screen.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            
            # NEUES TOOL: Notepad Text schreiben
            {"type": "function", "function": {"name": "write_text_in_notepad", "description": "Opens Notepad, types text into it, and saves the file. Use this when the user asks to write a text file or a note.", "parameters": {"type": "object", "properties": {"filename": {"type": "string"}, "text": {"type": "string"}}, "required": ["filename", "text"]}}},
            
            {"type": "function", "function": {"name": "create_web_project_visually", "description": "Creates a full web project and opens it in VS Code.", "parameters": {"type": "object", "properties": {"project_name": {"type": "string"}}, "required": ["project_name"]}}},
            {"type": "function", "function": {"name": "write_code_file", "description": "Writes code directly to a file and opens it in VS Code.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}, "code_content": {"type": "string"}}, "required": ["file_path", "code_content"]}}},
            {"type": "function", "function": {"name": "uninstall_with_revo_visually", "description": "Opens Revo Uninstaller visibly.", "parameters": {"type": "object", "properties": {"program_name": {"type": "string"}}, "required": ["program_name"]}}},
            {"type": "function", "function": {"name": "list_directory", "description": "Lists files in a directory.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
            {"type": "function", "function": {"name": "read_text_file", "description": "Reads the content of a file.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}}},
            {"type": "function", "function": {"name": "web_search", "description": "Searches the internet.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
            {"type": "function", "function": {"name": "analyze_disk", "description": "Analyzes hard drives.", "parameters": {"type": "object", "properties": {}, "required": []}}}
        ]

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name == "open_application":
            app = arguments.get("app_name", "").lower().strip()
            return PCControl.open_app_visually(app)
            
        elif tool_name == "write_text_in_notepad":
            filename = arguments.get("filename", "note.txt")
            text = arguments.get("text", "")
            return PCControl.write_in_notepad(filename, text)

        elif tool_name == "create_web_project_visually":
            project_name = arguments.get("project_name", "NewProject")
            result = ProjectGenerator.create_web_project(project_name)
            desktop = os.path.join(os.path.expanduser("~"), "Desktop", "EVOX_Projects", project_name)
            subprocess.Popen(f'explorer "{desktop}"', shell=True)
            time.sleep(1.5)
            PCControl.open_app_visually("Visual Studio Code")
            time.sleep(2.0)
            return f"Success: Project {project_name} created and opened visually."

        elif tool_name == "write_code_file":
            file_path = arguments.get("file_path", "").replace("/", "\\")
            code = arguments.get("code_content", "")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                subprocess.Popen(f'code -r "{file_path}"', shell=True)
                time.sleep(1.5)
                UIAutomation.center_window("Visual Studio Code")
                UIAutomation.focus_window("Visual Studio Code")
                return f"Success: Wrote {file_path} and opened it in VS Code."
            except Exception as e:
                return f"Error writing code file: {str(e)}"

        elif tool_name == "uninstall_with_revo_visually":
            prog_name = arguments.get("program_name", "")
            
            # 1. Revo starten (kein UAC mehr!)
            AdminTools.launch_revo_admin()
            
            # 2. Warten, bis Revo geladen ist
            time.sleep(5.0) # Auf 5 Sekunden reduziert
            
            # 3. Fenster zentrieren und fokussieren
            UIAutomation.center_window("Revo Uninstaller")
            UIAutomation.focus_window("Revo Uninstaller")
            time.sleep(1.0)
            
            # 4. Programmnamen tippen
            pyautogui.write(prog_name, interval=0.05)
            time.sleep(1.0)
            
            return f"Success: Started Revo and typed '{prog_name}'."

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
            
        return f"Error: Tool '{tool_name}' is unknown."