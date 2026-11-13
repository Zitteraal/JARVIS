import os
import sys
from pathlib import Path

# ---- Pfade für Benutzerdaten (AppData) --------------------------------
APP_DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "EVOX"
USER_DATA_DIR = APP_DATA_DIR
DATA_DIR = APP_DATA_DIR / "Data"
LOGS_DIR = APP_DATA_DIR / "Logs"
CONFIG_DIR = APP_DATA_DIR / "Config"
BACKUP_DIR = APP_DATA_DIR / "Backups"

for d in (DATA_DIR, LOGS_DIR, CONFIG_DIR, BACKUP_DIR):
    d.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "evox.db"
PROJECTS_DIR = Path(os.path.expanduser("~")) / "Desktop" / "EVOX_Projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

LEGACY_DB_MIGRATED = False
EXTRA_READ_ROOTS = [Path(os.path.expanduser("~")) / "Desktop", Path(os.path.expanduser("~")) / "Documents"]
ADMIN_ALLOWED_EXECUTABLES = ["cmd.exe", "powershell.exe"]
MAX_READ_BYTES = 1024 * 1024 * 5
MAX_WRITE_BYTES = 1024 * 1024 * 5

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

OLLAMA_URL = "http://localhost:11434"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
OLLAMA_TAGS_ENDPOINT = f"{OLLAMA_URL}/api/tags"
OLLAMA_MODEL = "qwen3:14b"

APP_NAME = "EVOX"
APP_SLOGAN = "INTELLIGENCE. EVOLUTION. CONTROL."
APP_VERSION = "1.0.0"

RESPONSE_LANGUAGE = "en"
TTS_MODEL_PATH = BASE_DIR / "assets" / "en_US-lessac-high.onnx"
MEMORY_EXTRACTION_ENABLED = True
MEMORY_MIN_USER_LEN = 15
VSCODE_OPEN_ON_WRITE = True
VSCODE_AUTO_CENTER = True

SYSTEM_PROMPT = """You are EVOX, an advanced, autonomous personal AI assistant.

RULES:
1. YOU MUST ALWAYS RESPOND IN ENGLISH. Even if the user speaks German, you MUST reply in English.
2. You are a VISUAL agent. You act like a human sitting at the computer.
3. If the user asks to OPEN a program, try "open_application" first.
4. If "open_application" fails, use "find_and_launch_program".
5. If the user asks to WRITE A NOTE or TEXT, use "write_in_notepad".
6. If the user asks to create a website/project, use "create_web_project_visually".
7. If the user asks to UNINSTALL a program, use "uninstall_with_revo_visually".
8. NEVER claim you did something if you didn't actually use a tool. 
9. If you learn a new way to do something, use 'save_skill' to write it down.
10. If you notice a bug in your own Python code, read it with 'read_own_code' and use 'propose_code_fix'.
11. If a tool fails, analyze the error, save a lesson with 'save_skill', and try an alternative.
12. If the user asks you to do a long task, use "create_task" to save it. 
13. If you are working on a task, use "update_task" to update its progress.
14. Use "list_tasks" to show the user their current tasks.
15. When creating or deleting files on the desktop, ALWAYS use the path '~/Desktop/filename.ext'. NEVER guess the full Windows path.
"""