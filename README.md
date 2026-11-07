\# EVOX

\### PERSONAL INTELLIGENCE WORKSPACE



\*\*INTELLIGENCE. EVOLUTION. CONTROL.\*\*



EVOX ist ein hochmoderner, autonomer KI-Assistent für Windows. Im Gegensatz zu herkömmlichen Chatbots ist EVOX als zentrale Desktop-Umgebung (Workspace) konzipiert. Er kombiniert lokale KI-Modelle (via Ollama), Systemadministration, Sprachsteuerung und Werkzeuge zur Automatisierung des PCs.



\## Features

\- \*\*Lokales KI-Gehirn:\*\* Nutzt Ollama (Qwen 3) für Tool-Calling und natürliche Konversation.

\- \*\*Sprachsteuerung:\*\* Push-to-Talk Mikrofon-Integration mit Faster-Whisper (STT) und Piper (TTS).

\- \*\*Systemadministration:\*\* Echtzeit-Systemanalyse (CPU, RAM, GPU), Programmanalyse und -deinstallation.

\- \*\*Computer Control:\*\* Steuerung von Maus, Tastatur und Fenstern (via PyAutoGUI und pywinauto).

\- \*\*Workspace UI:\*\* Ein taktisches, minimalistisches Desktop-Interface, entwickelt mit PySide6 und QML.

\- \*\*Langzeitgedächtnis:\*\* Speichert Fakten über den Nutzer dauerhaft in einer SQLite-Datenbank.

\- \*\*Dateimanager:\*\* Integrierter File-Workspace zum Durchsuchen und Verwalten von Dateien.

\- \*\*Sicherheitsarchitektur:\*\* Kritischesystemeingriffe (Admin/Deinstallation) erfordern eine explizite UI-Bestätigung.



\## Voraussetzungen

\- \*\*Windows 10/11\*\*

\- \*\*Python 3.10+\*\*

\- \*\*Ollama\*\* (Lokal installiert und gestartet: `ollama serve`)

\- Das Modell muss heruntergeladen sein: `ollama pull qwen3:14b` (oder ein anderes kompatibles Modell)



\## Installation

1\. Repository klonen:

&#x20;  ```bash

&#x20;  git clone https://github.com/Zitteraal/JARVIS.git

&#x20;  cd JARVIS



2\. Virtuelle Umgebung erstellen und aktivieren:



python -m venv .venv

.venv\\Scripts\\activate



3\. Abhängigkeiten installieren:



pip install -r requirements.txt



4\. EVOX starten:



python main.py





Architektur

core/ – KI-Engine, Tool-Management und Kontextverwaltung.



computer\_control/ – Maus-, Tastatur- und Fenstersteuerung.



system\_administration/ – Systemanalyse, Registry, Dateiverwaltung.



voice/ – Spracherkennung (Whisper) und Sprachausgabe (TTS).



memory/ – SQLite-Datenbank und Langzeitgedächtnis.



interface/ – QML-basierte Benutzeroberfläche und Backend-Brücke.

