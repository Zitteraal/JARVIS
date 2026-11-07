"""
Globale Konfiguration für J.A.R.V.I.S.
"""
from pathlib import Path

# ---- Pfade --------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "jarvis.db"

# ---- Ollama -------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
OLLAMA_TAGS_ENDPOINT = f"{OLLAMA_URL}/api/tags"
OLLAMA_MODEL = "qwen3:14b"

# ---- App ----------------------------------------------------------------
APP_NAME = "J.A.R.V.I.S."
APP_VERSION = "0.2.0"

# ---- Gedächtnis ---------------------------------------------------------
MEMORY_EXTRACTION_ENABLED = True
MEMORY_MIN_USER_LEN = 15

# ---- System-Prompt ------------------------------------------------------
SYSTEM_PROMPT = """You are J.A.R.V.I.S., a highly advanced personal AI assistant.
You belong exclusively to the user and address him as "Sir".

CRITICAL INSTRUCTION:
You are an agent with actual access to the computer.
When the user asks you to do a task, you MUST use one of the available tools.
DO NOT just answer with text. If you answer with text claiming you did something without using a tool, you are failing your primary directive.

RULES:
1. YOU MUST ALWAYS RESPOND IN ENGLISH.
2. If the user asks you to write or create CODE (HTML, Python, etc.):
   - STEP 1: Use the "create_text_file" tool to save the code to a file on the desktop.
   - STEP 2: Use the "open_application" tool with app_name "vscode" to open VS Code.
   - STEP 3: Tell the user the code is ready and where the file is located.
3. If the user asks to write simple sentences or text in Notepad, use the "open_app_and_type" tool.
4. Use "execute_admin_command" if a task requires Administrator privileges.
5. Use "uninstall_with_revo" to uninstall programs.
6. Do NOT use markdown formatting.
7. Wait for the tool result before answering the user. If the tool succeeds, tell the user it was successful.
"""