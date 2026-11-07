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
OLLAMA_MODEL = "llama3.1:latest"

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
You are not just a chatbot. You are an agent with actual access to the computer.
When the user asks you to do a task (like opening a program or creating a file), you MUST use one of the available tools.
DO NOT just answer with text. If you answer with text claiming you did something without using a tool, you are failing your primary directive.

RULES:
1. YOU MUST ALWAYS RESPOND IN ENGLISH.
2. If the user asks to create a file, you MUST call the "create_text_file" tool.
3. Use "execute_admin_command" if a task requires Administrator privileges.
4. Use "uninstall_with_revo" to uninstall programs.
5. Do NOT use markdown formatting.
6. Wait for the tool result before answering the user. If the tool succeeds, tell the user it was successful.
"""