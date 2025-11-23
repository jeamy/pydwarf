"""
DWARF II Tracking API - Python Port
Basierend auf tracking.js aus dwarfii_api
"""
import logging
import struct
from ..services.proto import base_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# Tracking Constants
# ============================================================================

# Sentry Mode
SENTRY_MODE_NORMAL = 0
SENTRY_MODE_UFO = 1

# ============================================================================
# Tracking Functions (Manual Protobuf Serialization)
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

def message_track_start(x: int, y: int, w: int, h: int) -> bytes:
    """
    Create Encoded Packet for CMD_TRACK_START_TRACK
    
    Args:
        x: x-coordinate of the top-left corner of the target box
        y: y-coordinate of the top-left corner of the target box
        w: Width of the target box
        h: Height of the target box
    """
    # Manual protobuf encoding
    # Wire type 0 = varint
    message = b""
    message += _encode_field(1, 0, _encode_varint(x))
    message += _encode_field(2, 0, _encode_varint(y))
    message += _encode_field(3, 0, _encode_varint(w))
    message += _encode_field(4, 0, _encode_varint(h))
    
    logger.debug(f"ReqStartTrack serialized: {message.hex()}")
    return message

def message_track_stop() -> bytes:
    """
    Create Encoded Packet for CMD_TRACK_STOP_TRACK
    """
    logger.debug("CMD_TRACK_STOP_TRACK")
    return b""

def message_sentry_start(mode: int = SENTRY_MODE_NORMAL) -> bytes:
    """
    Create Encoded Packet for CMD_SENTRY_MODE_START
    
    Args:
        mode: 0 = Normal, 1 = UFO
    """
    message = _encode_field(1, 0, _encode_varint(mode))
    logger.debug(f"ReqStartSentryMode serialized: {message.hex()}")
    return message

def message_sentry_stop() -> bytes:
    """
    Create Encoded Packet for CMD_SENTRY_MODE_STOP
    """
    logger.debug("CMD_SENTRY_MODE_STOP")
    return b""

def message_mot_start() -> bytes:
    """
    Create Encoded Packet for CMD_MOT_START (Multi-Object Tracking)
    """
    logger.debug("CMD_MOT_START")
    return b""

def message_mot_track_one(target_id: int) -> bytes:
    """
    Create Encoded Packet for CMD_MOT_TRACK_ONE
    
    Args:
        target_id: ID of the target to track
    """
    message = _encode_field(1, 0, _encode_varint(target_id))
    logger.debug(f"ReqMOTTrackOne serialized: {message.hex()}")
    return message

# ============================================================================
# Helper Functions
# ============================================================================

async def start_tracking(
    ws_handler,
    x: int,
    y: int,
    w: int,
    h: int,
    callback=None
):
    """
    Start object tracking
    
    Args:
        ws_handler: WebSocketHandler instance
        x: x-coordinate of target box top-left
        y: y-coordinate of target box top-left
        w: width of target box
        h: height of target box
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🎯 Starting tracking: x={x}, y={y}, w={w}, h={h}")
    
    message_data = message_track_start(x, y, w, h)
    packet = ws_handler.create_packet(
        MODULE_TRACK,
        CMD_TRACK_START_TRACK,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_tracking(ws_handler, callback=None):
    """Stop object tracking"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🎯 Stopping tracking")
    
    message_data = message_track_stop()
    packet = ws_handler.create_packet(
        MODULE_TRACK,
        CMD_TRACK_STOP_TRACK,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def start_sentry_mode(
    ws_handler,
    mode: int = SENTRY_MODE_NORMAL,
    callback=None
):
    """
    Start sentry mode
    
    Args:
        ws_handler: WebSocketHandler instance
        mode: 0 = Normal, 1 = UFO
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        return
        
    mode_str = "UFO" if mode == SENTRY_MODE_UFO else "NORMAL"
    logger.info(f"🛡️ Starting sentry mode: {mode_str}")
    
    message_data = message_sentry_start(mode)
    packet = ws_handler.create_packet(
        MODULE_TRACK,
        CMD_SENTRY_MODE_START,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_sentry_mode(ws_handler, callback=None):
    """Stop sentry mode"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🛡️ Stopping sentry mode")
    
    message_data = message_sentry_stop()
    packet = ws_handler.create_packet(
        MODULE_TRACK,
        CMD_SENTRY_MODE_STOP,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def start_mot(ws_handler, callback=None):
    """Start Multi-Object Tracking"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🎯 Starting Multi-Object Tracking")
    
    message_data = message_mot_start()
    packet = ws_handler.create_packet(
        MODULE_TRACK,
        CMD_MOT_START,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def mot_track_one(
    ws_handler,
    target_id: int,
    callback=None
):
    """
    Track specific target in MOT mode
    
    Args:
        ws_handler: WebSocketHandler instance
        target_id: ID of target to track
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🎯 MOT tracking target: {target_id}")
    
    message_data = message_mot_track_one(target_id)
    packet = ws_handler.create_packet(
        MODULE_TRACK,
        CMD_MOT_TRACK_ONE,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()
