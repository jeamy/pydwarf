"""
DWARF II WebSocket-Client
Kommunikation über WebSocket mit Protobuf
"""
import asyncio
import websockets
from typing import Callable, Optional, Dict, Any
import logging
from .proto import base_pb2

logger = logging.getLogger(__name__)


class DwarfWebSocketClient:
    """WebSocket-Client für DWARF II Teleskop"""
    
    def __init__(self, ip: str, port: int = 9900):
        self.ip = ip
        self.port = port
        self.url = f"ws://{ip}:{port}/"
        self.ws = None
        self.running = False
        self.message_handlers: Dict[tuple, Callable] = {}
        self.response_queue: asyncio.Queue = asyncio.Queue()
        
        # Protokoll-Version
        self.major_version = 2
        self.minor_version = 0
        self.device_id = 1  # 1: DWARF II, 2: MAGNI
    
    async def connect(self):
        """WebSocket-Verbindung herstellen"""
        try:
            self.ws = await websockets.connect(self.url)
            self.running = True
            
            # Background-Tasks starten
            asyncio.create_task(self._heartbeat())
            asyncio.create_task(self._receive_messages())
            
            logger.info(f"WebSocket verbunden: {self.url}")
        except Exception as e:
            logger.error(f"WebSocket-Verbindung fehlgeschlagen: {e}")
            raise
    
    async def disconnect(self):
        """WebSocket-Verbindung trennen"""
        self.running = False
        if self.ws:
            await self.ws.close()
            logger.info("WebSocket getrennt")
    
    async def _heartbeat(self):
        """Heartbeat senden (alle 30 Sekunden)"""
        while self.running:
            try:
                if self.ws:
                    await self.ws.send("ping")
                    logger.debug("Heartbeat gesendet")
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Heartbeat-Fehler: {e}")
                break
    
    async def _receive_messages(self):
        """Nachrichten empfangen"""
        while self.running:
            try:
                if not self.ws:
                    break
                
                data = await self.ws.recv()
                
                # Pong-Response ignorieren
                if isinstance(data, str) and data == "pong":
                    logger.debug("Pong empfangen")
                    continue
                
                # Protobuf-Paket parsen
                if isinstance(data, bytes):
                    await self._handle_protobuf_packet(data)
                    
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket-Verbindung geschlossen")
                break
            except Exception as e:
                logger.error(f"Fehler beim Empfangen: {e}")
                break
    
    async def _handle_protobuf_packet(self, data: bytes):
        """Protobuf-Paket verarbeiten"""
        try:
            # WsPacket parsen
            packet = base_pb2.WsPacket()
            packet.ParseFromString(data)
            
            logger.debug(
                f"Paket empfangen: Module {packet.module_id}, "
                f"CMD {packet.cmd}, Type {packet.type}"
            )
            
            # In Queue für wartende Requests
            await self.response_queue.put(packet)
            
            # Handler aufrufen, falls registriert
            key = (packet.module_id, packet.cmd)
            if key in self.message_handlers:
                await self.message_handlers[key](packet)
            
        except Exception as e:
            logger.error(f"Fehler beim Parsen des Protobuf-Pakets: {e}")
    
    def register_handler(
        self,
        module_id: int,
        cmd: int,
        handler: Callable
    ):
        """Handler für bestimmte Nachrichten registrieren"""
        key = (module_id, cmd)
        self.message_handlers[key] = handler
        logger.debug(f"Handler registriert: Module {module_id}, CMD {cmd}")
    
    async def send_command(
        self,
        module_id: int,
        cmd: int,
        data: bytes,
        wait_response: bool = False,
        timeout: float = 5.0
    ) -> Optional[Any]:
        """
        Befehl senden
        
        Args:
            module_id: Modul-ID
            cmd: Befehls-ID
            data: Serialisierte Protobuf-Message
            wait_response: Auf Response warten
            timeout: Timeout in Sekunden
        
        Returns:
            WsPacket (wenn wait_response=True)
        """
        if not self.ws or not self.running:
            raise ConnectionError("WebSocket nicht verbunden")
        
        try:
            # WsPacket erstellen
            packet = base_pb2.WsPacket()
            packet.major_version = self.major_version
            packet.minor_version = self.minor_version
            packet.device_id = self.device_id
            packet.module_id = module_id
            packet.cmd = cmd
            packet.type = 0  # Request
            packet.data = data
            
            # Senden
            await self.ws.send(packet.SerializeToString())
            logger.debug(f"Befehl gesendet: Module {module_id}, CMD {cmd}")
            
            # Auf Response warten
            if wait_response:
                try:
                    response = await asyncio.wait_for(
                        self.response_queue.get(),
                        timeout=timeout
                    )
                    return response
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout beim Warten auf Response")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Fehler beim Senden: {e}")
            raise
    
    async def send_command_simple(
        self,
        module_id: int,
        cmd: int
    ):
        """
        Einfachen Befehl ohne Daten senden
        (z.B. für Befehle ohne Parameter)
        """
        await self.send_command(module_id, cmd, b"")
    
    def is_connected(self) -> bool:
        """Prüfen ob verbunden"""
        return self.running and self.ws is not None
