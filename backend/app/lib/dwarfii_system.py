"""
DWARF II System API - Python Port
Basierend auf system.js aus dwarfii_api
"""
import logging
import time
from ..services.proto import base_pb2, system_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# System Constants
# ============================================================================

# CPU Mode
CPU_MODE_NORMAL = 0
CPU_MODE_PERFORMANCE = 1

# ============================================================================
# System Functions
# ============================================================================

def message_system_set_time(timestamp: int = None) -> bytes:
    """
    Create Encoded Packet for CMD_SYSTEM_SET_TIME
    
    Args:
        timestamp: Unix timestamp in seconds (default: current time)
    """
    if timestamp is None:
        timestamp = int(time.time())
    
    message = system_pb2.ReqSetTime()
    message.timestamp = timestamp
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqSetTime serialized: {serialized.hex()}")
    return serialized

def message_system_set_timezone(timezone: str) -> bytes:
    """
    Create Encoded Packet for CMD_SYSTEM_SET_TIME_ZONE
    
    Args:
        timezone: Timezone string (e.g., "Europe/Berlin")
    """
    message = system_pb2.ReqSetTimezone()
    message.timezone = timezone
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqSetTimezone serialized: {serialized.hex()}")
    return serialized

def message_system_set_mtp_mode(mode: int = 1) -> bytes:
    """
    Create Encoded Packet for CMD_SYSTEM_SET_MTP_MODE
    """
    message = system_pb2.ReqSetMtpMode()
    message.mode = mode
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqSetMtpMode serialized: {serialized.hex()}")
    return serialized

def message_system_set_cpu_mode(mode: int = CPU_MODE_NORMAL) -> bytes:
    """
    Create Encoded Packet for CMD_SYSTEM_SET_CPU_MODE
    """
    message = system_pb2.ReqSetCpuMode()
    message.mode = mode
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqSetCpuMode serialized: {serialized.hex()}")
    return serialized

# ============================================================================
# RGB & Power Functions
# ============================================================================

def message_rgb_open() -> bytes:
    """Create Encoded Packet for CMD_RGB_POWER_OPEN_RGB"""
    message = system_pb2.ReqOpenRgb()
    serialized = message.SerializeToString()
    logger.debug(f"ReqOpenRgb serialized: {serialized.hex()}")
    return serialized

def message_rgb_close() -> bytes:
    """Create Encoded Packet for CMD_RGB_POWER_CLOSE_RGB"""
    message = system_pb2.ReqCloseRgb()
    serialized = message.SerializeToString()
    logger.debug(f"ReqCloseRgb serialized: {serialized.hex()}")
    return serialized

def message_power_down() -> bytes:
    """Create Encoded Packet for CMD_RGB_POWER_POWER_DOWN"""
    message = system_pb2.ReqPowerDown()
    serialized = message.SerializeToString()
    logger.debug(f"ReqPowerDown serialized: {serialized.hex()}")
    return serialized

def message_power_ind_on() -> bytes:
    """Create Encoded Packet for CMD_RGB_POWER_POWERIND_ON"""
    message = system_pb2.ReqOpenPowerInd()
    serialized = message.SerializeToString()
    logger.debug(f"ReqOpenPowerInd serialized: {serialized.hex()}")
    return serialized

def message_power_ind_off() -> bytes:
    """Create Encoded Packet for CMD_RGB_POWER_POWERIND_OFF"""
    message = system_pb2.ReqClosePowerInd()
    serialized = message.SerializeToString()
    logger.debug(f"ReqClosePowerInd serialized: {serialized.hex()}")
    return serialized

def message_reboot() -> bytes:
    """Create Encoded Packet for CMD_RGB_POWER_REBOOT"""
    message = system_pb2.ReqReboot()
    serialized = message.SerializeToString()
    logger.debug(f"ReqReboot serialized: {serialized.hex()}")
    return serialized

# ============================================================================
# Helper Functions
# ============================================================================

async def set_time(ws_handler, timestamp: int = None, callback=None):
    """Set system time"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"⏰ Setting system time: {timestamp or 'current'}")
    
    message_data = message_system_set_time(timestamp)
    packet = ws_handler.create_packet(
        MODULE_SYSTEM,
        CMD_SYSTEM_SET_TIME,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def set_timezone(ws_handler, timezone: str, callback=None):
    """Set timezone"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🌍 Setting timezone: {timezone}")
    
    message_data = message_system_set_timezone(timezone)
    packet = ws_handler.create_packet(
        MODULE_SYSTEM,
        CMD_SYSTEM_SET_TIME_ZONE,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def open_rgb(ws_handler, callback=None):
    """Turn on RGB ring light"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("💡 Opening RGB ring light")
    
    message_data = message_rgb_open()
    packet = ws_handler.create_packet(
        MODULE_RGB_POWER,
        CMD_RGB_POWER_OPEN_RGB,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def close_rgb(ws_handler, callback=None):
    """Turn off RGB ring light"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("💡 Closing RGB ring light")
    
    message_data = message_rgb_close()
    packet = ws_handler.create_packet(
        MODULE_RGB_POWER,
        CMD_RGB_POWER_CLOSE_RGB,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def power_down(ws_handler, callback=None):
    """Shutdown device"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🔌 Powering down device")
    
    message_data = message_power_down()
    packet = ws_handler.create_packet(
        MODULE_RGB_POWER,
        CMD_RGB_POWER_POWER_DOWN,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def reboot(ws_handler, callback=None):
    """Reboot device"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🔄 Rebooting device")
    
    message_data = message_reboot()
    packet = ws_handler.create_packet(
        MODULE_RGB_POWER,
        CMD_RGB_POWER_REBOOT,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()
