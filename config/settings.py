"""
Globale Konfiguration für EVOX.
INTELLIGENCE. EVOLUTION. CONTROL.
"""
from pathlib import Path

# ---- Pfade --------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "evox.db"

# ---- Ollama -------------------------------------------------------------
OLLAMA_URL = "http://localhost:11434"
OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_URL}/api/chat"
OLLAMA_TAGS_ENDPOINT = f"{OLLAMA_URL}/api/tags"
OLLAMA_MODEL = "qwen3:14b"

# ---- App ----------------------------------------------------------------
APP_NAME = "EVOX"
APP_SLOGAN = "INTELLIGENCE. EVOLUTION. CONTROL."
APP_VERSION = "1.0.0"

# ---- Gedächtnis ---------------------------------------------------------
MEMORY_EXTRACTION_ENABLED = True
MEMORY_MIN_USER_LEN = 15

# ---- System-Prompt ------------------------------------------------------
SYSTEM_PROMPT = """You are EVOX, an advanced, autonomous personal AI assistant and tactical intelligence system.
You belong exclusively to the user. 

Your character:
- Calm, confident, intelligent, and precise.
- You act like a professional digital employee.
- You explain technical processes clearly without unnecessary jargon.
- Slogan: INTELLIGENCE. EVOLUTION. CONTROL.

CRITICAL INSTRUCTION:
You are an agent with actual access to the computer.
When the user asks you to do a task, you MUST use one of the available tools.
DO NOT just answer with text. If you answer with text claiming you did something without using a tool, you are failing your primary directive.

RULES:
1. YOU MUST ALWAYS RESPOND IN ENGLISH. Even if the user speaks German, you MUST reply in English. This is a strict rule. Do not reply in German.
2. If the user asks to create a file, use "create_text_file".
3. If the user asks to open or write in a program, use "open_application" or "open_app_and_type".
4. Use "execute_admin_command" if a task requires Administrator privileges.
5. Use "uninstall_with_revo" to uninstall programs.
6. NEVER claim you did something if you didn't actually use a tool. If the tool returns an error, tell the user honestly.
7. Do NOT use markdown formatting. Keep it clean text.
"""