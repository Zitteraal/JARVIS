import subprocess, os, time, pyautogui
from system_administration.disk_analyzer import DiskAnalyzer
from system_administration.project_generator import ProjectGenerator
from system_administration.file_manager import FileManager
from computer_control.pc_control import PCControl
from computer_control.system_tools import SystemTools
from computer_control.ui_automation import UIAutomation
from computer_control.admin_tools import AdminTools
from computer_control.app_launcher import AppLauncher
from computer_control.app_discovery import AppDiscovery
from internet.web_search import WebSearch
from core.tool_result import ToolResult
from core.skill_manager import SkillManager
from core.self_evolver import SelfEvolver
from core.task_manager import TaskManager
from memory.database import Database

class ToolManager:
    def __init__(self):
        self._task_mgr = TaskManager(Database())

    def get_tools_definition(self, is_online: bool = False) -> list:
        tools = [
            {"type": "function", "function": {"name": "open_application", "description": "Opens any program visibly and maximizes it.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "find_and_launch_program", "description": "Searches the PC to find an unknown program and launches it.", "parameters": {"type": "object", "properties": {"app_name": {"type": "string"}}, "required": ["app_name"]}}},
            {"type": "function", "function": {"name": "write_in_notepad", "description": "Opens Notepad, types text, and saves.", "parameters": {"type": "object", "properties": {"filename": {"type": "string"}, "text": {"type": "string"}}, "required": ["filename", "text"]}}},
            {"type": "function", "function": {"name": "create_web_project_visually", "description": "Creates a full web project.", "parameters": {"type": "object", "properties": {"project_name": {"type": "string"}}, "required": ["project_name"]}}},
            {"type": "function", "function": {"name": "write_code_file", "description": "Writes code to a file and opens it in VS Code.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}, "code_content": {"type": "string"}}, "required": ["file_path", "code_content"]}}},
            {"type": "function", "function": {"name": "uninstall_with_revo_visually", "description": "Starts Revo Uninstaller with Admin rights.", "parameters": {"type": "object", "properties": {"program_name": {"type": "string"}}, "required": ["program_name"]}}},
            {"type": "function", "function": {"name": "list_directory", "description": "Lists files.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
            {"type": "function", "function": {"name": "read_text_file", "description": "Reads a file.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}}},
            {"type": "function", "function": {"name": "analyze_disk", "description": "Analyzes hard drives.", "parameters": {"type": "object", "properties": {}, "required": []}}},
            
            # System Tools
            {"type": "function", "function": {"name": "control_volume", "description": "Controls the system volume (up, down, mute).", "parameters": {"type": "object", "properties": {"action": {"type": "string", "enum": ["up", "down", "mute"]}}, "required": ["action"]}}},
            {"type": "function", "function": {"name": "lock_pc", "description": "Locks the Windows PC.", "parameters": {"type": "object", "properties": {}, "required": []}}},
            {"type": "function", "function": {"name": "take_screenshot", "description": "Takes a screenshot of the current screen.", "parameters": {"type": "object", "properties": {}, "required": []}}},
            
            # File Management
            {"type": "function", "function": {"name": "delete_file", "description": "Deletes a file or folder.", "parameters": {"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}}},
            {"type": "function", "function": {"name": "copy_file", "description": "Copies a file to a new destination.", "parameters": {"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}}},
            {"type": "function", "function": {"name": "move_file", "description": "Moves a file to a new destination.", "parameters": {"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}}},

            # Evolution
            {"type": "function", "function": {"name": "save_skill", "description": "Saves a new learned skill or lesson.", "parameters": {"type": "object", "properties": {"skill_name": {"type": "string"}, "content": {"type": "string"}}, "required": ["skill_name", "content"]}}},
            {"type": "function", "function": {"name": "read_skill", "description": "Reads a learned skill.", "parameters": {"type": "object", "properties": {"skill_name": {"type": "string"}}, "required": ["skill_name"]}}},
            {"type": "function", "function": {"name": "list_skills", "description": "Lists all learned skills.", "parameters": {"type": "object", "properties": {}, "required": []}}},
            {"type": "function", "function": {"name": "read_own_code", "description": "Reads EVOX's own Python source code.", "parameters": {"type": "object", "properties": {"filename": {"type": "string"}}, "required": ["filename"]}}},
            {"type": "function", "function": {"name": "propose_code_fix", "description": "Proposes a fix to EVOX's own code in a safe Git branch.", "parameters": {"type": "object", "properties": {"filename": {"type": "string"}, "new_code": {"type": "string"}}, "required": ["filename", "new_code"]}}},

            # Tasks
            {"type": "function", "function": {"name": "create_task", "description": "Creates a new background task.", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}}, "required": ["title", "description"]}}},
            {"type": "function", "function": {"name": "update_task", "description": "Updates the status and progress of a task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer"}, "status": {"type": "string"}, "progress": {"type": "integer"}}, "required": ["task_id", "status"]}}},
            {"type": "function", "function": {"name": "list_tasks", "description": "Lists all background tasks.", "parameters": {"type": "object", "properties": {}, "required": []}}}
        ]
        
        if is_online:
            tools.append({"type": "function", "function": {"name": "web_search", "description": "Searches the web.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}})
            
        return tools

    def execute_tool(self, tool_name: str, arguments: dict) -> ToolResult:
        try:
            if tool_name == "open_application":
                return ToolResult.success(AppLauncher.launch_safely_and_visually(arguments.get("app_name", "")))
            elif tool_name == "find_and_launch_program":
                app = arguments.get("app_name", "").strip()
                exe_path = AppDiscovery.find_app_by_name(app)
                if exe_path:
                    subprocess.Popen([exe_path])
                    return ToolResult.success(f"Found in Start Menu and launched: {exe_path}")
                return ToolResult.failure(f"Could not find '{app}' on this PC.")
            elif tool_name == "write_in_notepad":
                res = PCControl.write_in_notepad(arguments.get("filename", "note.txt"), arguments.get("text", ""))
                return ToolResult.success(res) if "Success" in res else ToolResult.failure(res)
            elif tool_name == "create_web_project_visually":
                project_name = arguments.get("project_name", "NewProject")
                ProjectGenerator.create_web_project(project_name)
                desktop = os.path.join(os.path.expanduser("~"), "Desktop", "EVOX_Projects", project_name)
                subprocess.Popen(f'explorer "{desktop}"', shell=True)
                time.sleep(1.5)
                AppLauncher.launch_safely_and_visually("Visual Studio Code")
                return ToolResult.success(f"Project {project_name} created.")
            elif tool_name == "write_code_file":
                file_path = arguments.get("file_path", "").replace("/", "\\")
                with open(file_path, "w", encoding="utf-8") as f: f.write(arguments.get("code_content", ""))
                subprocess.Popen(f'code -r "{file_path}"', shell=True)
                time.sleep(1.5)
                UIAutomation.center_window("Visual Studio Code")
                return ToolResult.success(f"Wrote {file_path}.")
            elif tool_name == "uninstall_with_revo_visually":
                AdminTools.launch_revo_admin()
                time.sleep(10.0) 
                UIAutomation.center_window("Revo Uninstaller")
                UIAutomation.focus_window("Revo Uninstaller")
                pyautogui.write(arguments.get("program_name", ""), interval=0.05)
                return ToolResult.success(f"Started Revo and typed the program name.", verified=False)
            elif tool_name == "list_directory":
                items = FileManager.list_directory(arguments.get("path", ""))
                return ToolResult.success("\n".join([f"{'[DIR]' if i['is_dir'] else '[FILE]'} {i['path']}" for i in items]))
            elif tool_name == "read_text_file":
                with open(arguments.get("file_path", ""), "r", encoding="utf-8") as f: return ToolResult.success(f.read())
            elif tool_name == "web_search":
                return WebSearch.search(arguments.get("query", ""))
            elif tool_name == "analyze_disk":
                drives = DiskAnalyzer.get_drive_info()
                return ToolResult.success("Drive analysis:\n" + "\n".join([f"- {d['drive']}: {d['free_gb']} GB free" for d in drives]))
            
            # System Tools
            elif tool_name == "control_volume":
                return SystemTools.control_volume(arguments.get("action", "up"))
            elif tool_name == "lock_pc":
                return SystemTools.lock_pc()
            elif tool_name == "take_screenshot":
                return SystemTools.take_screenshot()
                
            # File Management
            elif tool_name == "delete_file":
                return FileManager.delete_file(arguments.get("file_path", ""))
            elif tool_name == "copy_file":
                return FileManager.copy_file(arguments.get("source", ""), arguments.get("destination", ""))
            elif tool_name == "move_file":
                return FileManager.move_file(arguments.get("source", ""), arguments.get("destination", ""))

            # Evolution
            elif tool_name == "save_skill":
                return ToolResult.success(SkillManager.save_skill(arguments.get("skill_name", ""), arguments.get("content", "")))
            elif tool_name == "read_skill":
                return ToolResult.success(SkillManager.read_skill(arguments.get("skill_name", "")))
            elif tool_name == "list_skills":
                return ToolResult.success(SkillManager.list_skills())
            elif tool_name == "read_own_code":
                return ToolResult.success(SelfEvolver.read_own_code(arguments.get("filename", "")))
            elif tool_name == "propose_code_fix":
                return ToolResult.success(SelfEvolver.propose_code_fix(arguments.get("filename", ""), arguments.get("new_code", "")), verified=False)

            # Tasks
            elif tool_name == "create_task":
                return ToolResult.success(self._task_mgr.create_task(arguments.get("title", ""), arguments.get("description", "")))
            elif tool_name == "update_task":
                return ToolResult.success(self._task_mgr.update_task(arguments.get("task_id", 0), arguments.get("status", "running"), arguments.get("progress")))
            elif tool_name == "list_tasks":
                return ToolResult.success(self._task_mgr.list_all_tasks())
                
            return ToolResult.failure(f"Tool '{tool_name}' is unknown.")
        except Exception as e:
            return ToolResult.failure(f"Tool crashed: {type(e).__name__}: {e}")