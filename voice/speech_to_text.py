import os
os.environ["HF_HUB_OFFLINE"] = "1" # <--- Zwingt Whisper in den Offline-Modus
import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from PySide6.QtCore import QObject, Signal

class VoiceAssistant(QObject):
    transcriptionReady = Signal(str)
    listeningChanged = Signal(bool)

    def __init__(self):
        super().__init__()
        self._is_recording = False
        self._thread = None
        self._audio_buffer = []
        
        print("Lade Whisper (STT) Modell...")
        self.whisper = WhisperModel("base", device="cpu", compute_type="int8")
        
        self.samplerate = 16000
        self.chunk_size = 1280 
        self.device_index = 2 

    def start_recording(self):
        if self._is_recording: return
        self._is_recording = True
        self._audio_buffer = []
        self.listeningChanged.emit(True)
        
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def stop_recording(self):
        if not self._is_recording: return
        self._is_recording = False
        self.listeningChanged.emit(False)
        
        if self._thread:
            self._thread.join(timeout=2)
            
        if len(self._audio_buffer) > 0:
            full_audio = np.concatenate(self._audio_buffer)
            self._transcribe(full_audio)

    def _record_loop(self):
        try:
            # Versuch 1: Mono (1 Kanal)
            with sd.InputStream(device=self.device_index, samplerate=self.samplerate, channels=1, dtype='int16', blocksize=self.chunk_size) as stream:
                while self._is_recording:
                    audio_chunk, _ = stream.read(self.chunk_size)
                    self._audio_buffer.append(audio_chunk.flatten())
        except sd.PortAudioError:
            try:
                # Versuch 2: Stereo (2 Kanäle) und dann auf Mono reduzieren
                with sd.InputStream(device=self.device_index, samplerate=self.samplerate, channels=2, dtype='int16', blocksize=self.chunk_size) as stream:
                    while self._is_recording:
                        audio_chunk, _ = stream.read(self.chunk_size)
                        self._audio_buffer.append(audio_chunk[:, 0]) # Nur linken Kanal nehmen
            except Exception as e:
                print(f"Mikrofon-Fehler beim Aufnehmen: {e}")
                self._is_recording = False
                self.listeningChanged.emit(False)

    def _transcribe(self, audio_data):
        print("Transcribing...")
        audio_float = audio_data.astype(np.float32) / 32768.0
        segments, info = self.whisper.transcribe(audio_float, beam_size=5, language="de")
        text = " ".join([segment.text for segment in segments]).strip()
        
        if text:
            print(f"Erkannt: {text}")
            self.transcriptionReady.emit(text)