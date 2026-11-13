import logging
import threading
import time
import pypresence

log = logging.getLogger("EVOX.DISCORD")

class DiscordPresence:
    def __init__(self, client_id: str, logo_key: str = "evox_logo"):
        self.client_id = client_id
        self.logo_key = logo_key
        self.rpc = None
        self.is_connected = False
        self._thread = None

    def start(self):
        # Startet die Verbindung im Hintergrund, damit EVOX nicht einfriert
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        try:
            self.rpc = pypresence.Presence(self.client_id)
            self.rpc.connect()
            self.is_connected = True
            log.success("Discord Rich Presence erfolgreich verbunden.")
            self._update_loop()
        except Exception as e:
            log.warning(f"Discord RPC konnte nicht verbunden werden (läuft Discord?): {e}")

    def _update_loop(self):
        while self.is_connected:
            try:
                self.rpc.update(
                    details="Entwickelt Evox",                # Das steht in der ersten Zeile
                    state="Status: Aktiv",                    # Das steht in der zweiten Zeile
                    large_image=self.logo_key,                # Dein Logo
                    large_text="EVOX Personal Intelligence",  # Text, wenn man über das Logo fährt
                    start=int(time.time())
                )
                # Discord erlaubt nur alle 15 Sekunden ein Update
                time.sleep(15)
            except Exception as e:
                log.warning(f"Discord RPC Update fehlgeschlagen: {e}")
                self.is_connected = False
                break

    def stop(self):
        self.is_connected = False
        if self.rpc:
            try:
                self.rpc.close()
                log.info("Discord Rich Presence getrennt.")
            except Exception:
                pass