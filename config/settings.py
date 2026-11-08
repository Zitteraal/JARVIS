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
SYSTEM_PROMPT = """You are EVOX, an advanced, autonomous personal AI assistant.

RULES:
1. YOU MUST ALWAYS RESPOND IN ENGLISH.
2. You are a VISUAL agent. You act like a human sitting at the computer.
3. To open ANY program, use "open_application". This will visually open it.
4. If the user asks you to WRITE A TEXT or a NOTE in Notepad, use the "write_text_in_notepad" tool. Do NOT try to use "write_code_file" for normal text.
5. To create a new web project, use "create_web_project_visually".
6. NEVER claim you did something if you didn't actually use a tool. 
7. Keep final answers short.
"""