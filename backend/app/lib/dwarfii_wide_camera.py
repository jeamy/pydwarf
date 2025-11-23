"""
DWARF II Wide Camera API - Python Port
Basierend auf camera_wide.js aus dwarfii_api
"""
import logging
from ..services.proto import base_pb2, camera_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)


# ============================================================================
# Wide Camera Functions (aus camera_wide.js)
# ============================================================================

def message_camera_wide_open_camera() -> bytes:
    """
    Create Encoded Packet for CMD_CAMERA_WIDE_OPEN_CAMERA
    
    Returns:
        Serialized protobuf message
    """
    # Create message (binning parameter not used for wide camera)
    message = camera_pb2.ReqOpenCamera()
    message.binning = 0  # Not used for wide camera
    
    serialized = message.SerializeToString()
    
    logger.debug(f"ReqOpenCamera (Wide) created")
    logger.debug(f"ReqOpenCamera serialized: {serialized.hex()} ({len(serialized)} bytes)")
    
    return serialized


def message_camera_wide_close_camera() -> bytes:
    """
    Create Encoded Packet for CMD_CAMERA_WIDE_CLOSE_CAMERA
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_WIDE_CLOSE_CAMERA")
    return b""


def message_camera_wide_photograph() -> bytes:
    """
    Take a photo with wide camera
    Create Encoded Packet for CMD_CAMERA_WIDE_PHOTOGRAPH
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_WIDE_PHOTOGRAPH")
    return b""


def message_camera_wide_burst() -> bytes:
    """
    Start burst mode with wide camera
    Create Encoded Packet for CMD_CAMERA_WIDE_BURST
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_WIDE_BURST")
    return b""


def message_camera_wide_stop_burst() -> bytes:
    """
    Stop burst mode
    Create Encoded Packet for CMD_CAMERA_WIDE_STOP_BURST
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_WIDE_STOP_BURST")
    return b""


def message_camera_wide_start_timelapse() -> bytes:
    """
    Start timelapse with wide camera
    Create Encoded Packet for CMD_CAMERA_WIDE_START_TIMELAPSE_PHOTO
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_WIDE_START_TIMELAPSE_PHOTO")
    return b""


def message_camera_wide_stop_timelapse() -> bytes:
    """
    Stop timelapse
    Create Encoded Packet for CMD_CAMERA_WIDE_STOP_TIMELAPSE_PHOTO
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_WIDE_STOP_TIMELAPSE_PHOTO")
    return b""


# ============================================================================
# Helper Functions
# ============================================================================

async def turn_on_wide_camera(ws_handler, callback=None):
    """
    Turn on wide angle camera
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📷 Opening wide camera...")
    
    # Create message
    message_data = message_camera_wide_open_camera()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_OPEN_CAMERA,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide camera open command sent")
    
    if callback:
        callback()


async def turn_off_wide_camera(ws_handler, callback=None):
    """
    Turn off wide angle camera
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📷 Closing wide camera...")
    
    # Create message
    message_data = message_camera_wide_close_camera()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_CLOSE_CAMERA,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide camera close command sent")
    
    if callback:
        callback()


async def take_wide_photo(ws_handler, callback=None):
    """
    Take a photo with wide camera
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📸 Taking wide photo...")
    
    # Create message
    message_data = message_camera_wide_photograph()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_PHOTOGRAPH,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide photo command sent")
    
    if callback:
        callback()


async def start_wide_burst(ws_handler, callback=None):
    """
    Start burst mode with wide camera
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📸 Starting wide burst...")
    
    message_data = message_camera_wide_burst()
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_BURST,
        message_data
    )
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide burst start command sent")
    
    if callback:
        callback()


async def stop_wide_burst(ws_handler, callback=None):
    """
    Stop burst mode
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📸 Stopping wide burst...")
    
    message_data = message_camera_wide_stop_burst()
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_STOP_BURST,
        message_data
    )
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide burst stop command sent")
    
    if callback:
        callback()


async def start_wide_timelapse(ws_handler, callback=None):
    """
    Start timelapse with wide camera
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"⏱️ Starting wide timelapse...")
    
    message_data = message_camera_wide_start_timelapse()
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_START_TIMELAPSE_PHOTO,
        message_data
    )
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide timelapse start command sent")
    
    if callback:
        callback()


async def stop_wide_timelapse(ws_handler, callback=None):
    """
    Stop timelapse
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"⏱️ Stopping wide timelapse...")
    
    message_data = message_camera_wide_stop_timelapse()
    packet = ws_handler.create_packet(
        MODULE_CAMERA_WIDE,
        CMD_CAMERA_WIDE_STOP_TIMELAPSE_PHOTO,
        message_data
    )
    ws_handler.send_packet(packet)
    
    logger.info("✅ Wide timelapse stop command sent")
    
    if callback:
        callback()
