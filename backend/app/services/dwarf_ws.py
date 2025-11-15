"""
Dummy DwarfWebSocketClient für Kompatibilität
TODO: Alle Funktionen auf dwarfii_api portieren
"""
import logging

logger = logging.getLogger(__name__)


class DwarfWebSocketClient:
    """Dummy-Klasse für Kompatibilität"""
    
    def __init__(self, ip: str, port: int = 9900):
        self.ip = ip
        self.port = port
        logger.warning(f"DwarfWebSocketClient ist deprecated. Bitte auf dwarfii_api portieren!")
    
    async def connect(self):
        raise NotImplementedError("Bitte auf dwarfii_api portieren")
    
    async def disconnect(self):
        pass
    
    async def send_command(self, *args, **kwargs):
        raise NotImplementedError("Bitte auf dwarfii_api portieren")
