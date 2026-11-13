import os
import sys
from pathlib import Path

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

RESPONSE_LANGUAGE = "en" # WICHTIG: Auf Englisch gestellt
TTS_MODEL_PATH = BASE_DIR / "assets" / "de_DE-thorsten-high.onnx"
MEMORY_EXTRACTION_ENABLED = True
MEMORY_MIN_USER_LEN = 15
VSCODE_OPEN_ON_WRITE = True
VSCODE_AUTO_CENTER = True

SYSTEM_PROMPT = """You are EVOX, an advanced, autonomous personal AI assistant.

RULES:
1. YOU MUST ALWAYS RESPOND IN ENGLISH.
2. You are a VISUAL agent. You act like a human sitting at the computer.
3. If the user asks to OPEN a program, try "open_application" first.
4. If "open_application" fails or you are not sure if the program is installed, use "find_and_launch_program".
5. If the user asks to WRITE A NOTE or TEXT, use "write_in_notepad".
6. If the user asks to SEARCH THE WEB, use "web_search".
7. If the user asks to create a website/project, use "create_web_project_visually".
8. If the user asks to UNINSTALL a program, you MUST use "uninstall_with_revo_visually".
9. NEVER claim you did something if you didn't actually use a tool. 
10. IMPORTANT: If a previous tool call was cancelled or timed out, and the user asks again, you MUST try to use the tool again. Do NOT just give manual instructions.
11. Keep final answers short.
"""