import subprocess
import os
import threading
import re
import unicodedata
from pathlib import Path
import pygame

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "assets" / "en_US-lessac-high.onnx"

class TextToSpeech:
    def __init__(self):
        self._lock = threading.Lock()
        self._pygame_init = False

    def speak(self, text: str):
        if not text.strip():
            return
        
        clean_text = self._clean_text(text)
        if not clean_text:
            return
            
        print(f"\n[TTS an Piper]: {clean_text}\n")
            
        threading.Thread(target=self._speak_worker, args=(clean_text,), daemon=True).start()

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`.*?`', '', text)
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        text = re.sub(r'[*_#~>|<\[\]{}()]', '', text)
        text = re.sub(r'(?i)\b(tilde|atilde|asterisk|backslash|slash|hash|underscore|absatz)\b', '', text)
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('utf-8')
        erlaubte_zeichen = r'a-zA-Z0-9äöüÄÖÜß\s.,!?;:\'"-'
        text = re.sub(f'[^{erlaubte_zeichen}]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _speak_worker(self, text: str):
        with self._lock:
            try:
                temp_wav = BASE_DIR / "data" / "tts_output.wav"
                cmd = ["piper", "--model", str(MODEL_PATH), "--output_file", str(temp_wav)]
                process = subprocess.run(cmd, input=text.encode('utf-8'), capture_output=True)
                
                if process.returncode != 0:
                    print(f"Piper Fehler: {process.stderr.decode('utf-8')}")
                    return

                if not self._pygame_init:
                    pygame.mixer.init()
                    self._pygame_init = True
                
                pygame.mixer.music.load(str(temp_wav))
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                    
                pygame.mixer.music.unload()
                
                if temp_wav.exists():
                    os.remove(temp_wav)
                    
            except Exception as e:
                print(f"TTS Fehler: {e}")