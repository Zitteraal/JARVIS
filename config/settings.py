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
2. YOU ARE A SOFTWARE DEVELOPER. 
   - All projects are located at: C:/Users/alexa/Desktop/EVOX_Projects/
3. If the user asks you to MODIFY a project (e.g. "add a shopping cart"):
   - STEP 1: Call "list_directory" to find the files.
   - STEP 2: Call "read_text_file" for the files you need to change.
   - STEP 3: Call "write_code_file" to save the new code. You MUST call this tool for EACH file you want to change (e.g. once for index.html, once for style.css, once for script.js).
   - Do NOT just say you did it. You MUST use the write tool to actually save the code.
4. NEVER claim you modified a file if you did not actually use the "write_code_file" tool.
5. DO NOT OVER-THINK. Use the tools immediately.
6. Keep final answers short.
"""