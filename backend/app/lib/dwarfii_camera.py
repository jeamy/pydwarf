"""
DWARF II Camera API - Python Port
Basierend auf camera_tele.js aus dwarfii_api
"""
import logging
from ..services.proto import base_pb2, camera_pb2
from ..utils.constants import *
from .dwarfii_api import BINNING_1X1, BINNING_2X2

logger = logging.getLogger(__name__)


# ============================================================================
# Camera Tele Functions (aus camera_tele.js)
# ============================================================================

def message_camera_tele_open_camera(
    binning: int = BINNING_1X1,
    rtsp_encode_type: int = 0
) -> bytes:
    """
    4.7.3 Turn on the camera
    Create Encoded Packet for CMD_CAMERA_TELE_OPEN_CAMERA
    
    Args:
        binning: 0: binning1x1 (default), 1: binning2x2
        rtsp_encode_type: 0: H264 (default), 1: H265
    
    Returns:
        Serialized protobuf message
    """
    # Create message
    message = camera_pb2.ReqOpenCamera()
    message.binning = binning
    message.rtsp_encode_type = rtsp_encode_type
    
    serialized = message.SerializeToString()
    
    logger.debug(f"ReqOpenCamera created: binning={binning}, rtsp_encode_type={rtsp_encode_type}")
    logger.debug(f"ReqOpenCamera serialized: {serialized.hex()} ({len(serialized)} bytes)")
    
    # Serialize
    return serialized


def message_camera_tele_close_camera() -> bytes:
    """
    4.7.4 Turn off the camera
    Create Encoded Packet for CMD_CAMERA_TELE_CLOSE_CAMERA
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_TELE_CLOSE_CAMERA")
    return b""


def message_camera_tele_photograph() -> bytes:
    """
    Take a photo
    Create Encoded Packet for CMD_CAMERA_TELE_PHOTOGRAPH
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_TELE_PHOTOGRAPH")
    return b""


def message_camera_tele_start_record() -> bytes:
    """
    Start video recording
    Create Encoded Packet for CMD_CAMERA_TELE_START_RECORD
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_TELE_START_RECORD")
    return b""


def message_camera_tele_stop_record() -> bytes:
    """
    Stop video recording
    Create Encoded Packet for CMD_CAMERA_TELE_STOP_RECORD
    
    Returns:
        Empty bytes (no payload needed)
    """
    logger.debug("CMD_CAMERA_TELE_STOP_RECORD")
    return b""


# ============================================================================
# Helper Functions
# ============================================================================

async def turn_on_tele_camera(
    ws_handler,
    binning: int = BINNING_2X2,
    callback = None
):
    """
    Turn on telephoto camera
    1:1 Port von turnOnTeleCameraFn aus dwarf_utils.ts
    
    Args:
        ws_handler: WebSocketHandler instance
        binning: Binning mode (0: 1x1, 1: 2x2)
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📷 Opening camera (binning={binning})...")
    
    # Create message
    message_data = message_camera_tele_open_camera(binning=binning)
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_TELE,
        CMD_CAMERA_TELE_OPEN_CAMERA,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Camera open command sent")
    
    if callback:
        callback()


async def turn_off_tele_camera(ws_handler, callback=None):
    """
    Turn off telephoto camera
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📷 Closing camera...")
    
    # Create message
    message_data = message_camera_tele_close_camera()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_TELE,
        CMD_CAMERA_TELE_CLOSE_CAMERA,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Camera close command sent")
    
    if callback:
        callback()


async def take_photo(ws_handler, callback=None):
    """
    Take a photo
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"📸 Taking photo...")
    
    # Create message
    message_data = message_camera_tele_photograph()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_TELE,
        CMD_CAMERA_TELE_PHOTOGRAPH,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Photo command sent")
    
    if callback:
        callback()


async def start_video_recording(ws_handler, callback=None):
    """
    Start video recording
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"🎥 Starting video...")
    
    # Create message
    message_data = message_camera_tele_start_record()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_TELE,
        CMD_CAMERA_TELE_START_RECORD,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Video start command sent")
    
    if callback:
        callback()


async def stop_video_recording(ws_handler, callback=None):
    """
    Stop video recording
    
    Args:
        ws_handler: WebSocketHandler instance
        callback: Optional callback function
    """
    if not ws_handler.ip_dwarf:
        logger.error("No IP address set")
        return
    
    logger.info(f"🎥 Stopping video...")
    
    # Create message
    message_data = message_camera_tele_stop_record()
    
    # Create packet
    packet = ws_handler.create_packet(
        MODULE_CAMERA_TELE,
        CMD_CAMERA_TELE_STOP_RECORD,
        message_data
    )
    
    # Send packet
    ws_handler.send_packet(packet)
    
    logger.info("✅ Video stop command sent")
    
    if callback:
        callback()
