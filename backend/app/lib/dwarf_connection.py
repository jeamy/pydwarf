"""
DWARF II Connection Manager
Verwaltet persistente WebSocket-Verbindungen
"""
import asyncio
import logging
from typing import Dict, Optional
from .dwarfii_api import WebSocketHandler

logger = logging.getLogger(__name__)


class DwarfConnectionManager:
    """
    Singleton Connection Manager für DWARF II
    Hält WebSocket-Verbindungen offen und wiederverwendet sie
    """
    
    _instance = None
    _connections: Dict[str, WebSocketHandler] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._connections = {}
            self._initialized = True
            logger.info("DwarfConnectionManager initialized")
    
    async def get_connection(self, ip: str) -> WebSocketHandler:
        """
        Hole oder erstelle WebSocket-Verbindung für IP
        Wiederverwendet bestehende Verbindungen
        """
        # Prüfe ob Verbindung existiert und noch offen ist
        if ip in self._connections:
            ws_handler = self._connections[ip]
            if ws_handler.is_connected():
                logger.info(f"♻️ Wiederverwendung bestehender Verbindung für {ip}")
                return ws_handler
            else:
                logger.info(f"🔄 Alte Verbindung geschlossen, erstelle neue für {ip}")
                del self._connections[ip]
        
        # Erstelle neue Verbindung
        logger.info(f"🆕 Erstelle neue Verbindung für {ip}")
        ws_handler = WebSocketHandler(ip)
        await ws_handler.open()
        
        if ws_handler.is_connected():
            self._connections[ip] = ws_handler
            logger.info(f"✅ Verbindung für {ip} erstellt und gespeichert")
        else:
            logger.error(f"❌ Verbindung für {ip} fehlgeschlagen")
        
        return ws_handler
    
    async def close_connection(self, ip: str):
        """Schließe Verbindung für IP"""
        if ip in self._connections:
            await self._connections[ip].close()
            del self._connections[ip]
            logger.info(f"🔌 Verbindung für {ip} geschlossen")
    
    async def close_all(self):
        """Schließe alle Verbindungen"""
        for ip in list(self._connections.keys()):
            await self.close_connection(ip)
        logger.info("🔌 Alle Verbindungen geschlossen")


# Globale Instanz
connection_manager = DwarfConnectionManager()
