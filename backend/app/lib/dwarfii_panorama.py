"""
DWARF II Panorama API - Python Port
"""
import logging
from ..services.proto import base_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# Panorama Functions
# ============================================================================

def _encode_varint(value: int) -> bytes:
    """Encode integer as protobuf varint"""
    result = []
    while value > 0x7f:
        result.append((value & 0x7f) | 0x80)
        value >>= 7
    result.append(value & 0x7f)
    return bytes(result)

def _encode_field(field_number: int, wire_type: int, value: bytes) -> bytes:
    """Encode protobuf field"""
    tag = (field_number << 3) | wire_type
    return _encode_varint(tag) + value

def message_panorama_start(rows: int, cols: int) -> bytes:
    """
    Create Encoded Packet for CMD_PANORAMA_START_GRID
    
    Args:
        rows: Number of rows in panorama grid
        cols: Number of columns in panorama grid
    """
    message = b""
    message += _encode_field(1, 0, _encode_varint(rows))
    message += _encode_field(2, 0, _encode_varint(cols))
    
    logger.debug(f"ReqStartPanoramaByGrid serialized: {message.hex()}")
    return message

def message_panorama_stop() -> bytes:
    """
    Create Encoded Packet for CMD_PANORAMA_STOP
    """
    logger.debug("CMD_PANORAMA_STOP")
    return b""

# ============================================================================
# Helper Functions
# ============================================================================

async def start_panorama(
    ws_handler,
    rows: int,
    cols: int,
    callback=None
):
    """
    Start panorama capture
    
    Args:
        ws_handler: WebSocketHandler instance
        rows: Number of rows in panorama grid
        cols: Number of columns in panorama grid
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"📸 Starting panorama: {rows}x{cols}")
    
    message_data = message_panorama_start(rows, cols)
    packet = ws_handler.create_packet(
        MODULE_PANORAMA,
        CMD_PANORAMA_START_GRID,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_panorama(ws_handler, callback=None):
    """Stop panorama capture"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("📸 Stopping panorama")
    
    message_data = message_panorama_stop()
    packet = ws_handler.create_packet(
        MODULE_PANORAMA,
        CMD_PANORAMA_STOP,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()
