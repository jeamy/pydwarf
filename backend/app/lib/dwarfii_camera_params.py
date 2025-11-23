"""
DWARF II Camera Parameters Extension
Erweiterte Kamera-Parameter (Exposure, Gain, White Balance, etc.)
"""
import logging
from ..services.proto import base_pb2, camera_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# Camera Parameter Constants
# ============================================================================

# Exposure Mode
EXP_MODE_AUTO = 0
EXP_MODE_MANUAL = 1

# Gain Mode
GAIN_MODE_AUTO = 0
GAIN_MODE_MANUAL = 1

# White Balance Mode
WB_MODE_AUTO = 0
WB_MODE_MANUAL = 1

# IR Cut Filter
IR_CUT = 0
IR_PASS = 1

# ============================================================================
# Helper Functions for Manual Protobuf Encoding
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

# ============================================================================
# Exposure Functions
# ============================================================================

def message_set_exp_mode(mode: int) -> bytes:
    """Set exposure mode (Auto/Manual)"""
    message = _encode_field(1, 0, _encode_varint(mode))
    logger.debug(f"SetExpMode serialized: {message.hex()}")
    return message

def message_set_exp(value: int) -> bytes:
    """Set exposure value (microseconds)"""
    message = _encode_field(1, 0, _encode_varint(value))
    logger.debug(f"SetExp serialized: {message.hex()}")
    return message

async def set_exposure_mode(ws_handler, mode: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set exposure mode"""
    if not ws_handler.ip_dwarf:
        return
    
    mode_str = "AUTO" if mode == EXP_MODE_AUTO else "MANUAL"
    logger.info(f"📷 Setting exposure mode: {mode_str}")
    
    message_data = message_set_exp_mode(mode)
    cmd = CMD_CAMERA_TELE_SET_EXP_MODE if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_EXP_MODE
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def set_exposure(ws_handler, value: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set exposure value in microseconds"""
    if not ws_handler.ip_dwarf:
        return
    
    logger.info(f"📷 Setting exposure: {value}µs")
    
    message_data = message_set_exp(value)
    cmd = CMD_CAMERA_TELE_SET_EXP if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_EXP
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

# ============================================================================
# Gain Functions
# ============================================================================

def message_set_gain_mode(mode: int) -> bytes:
    """Set gain mode (Auto/Manual)"""
    message = _encode_field(1, 0, _encode_varint(mode))
    logger.debug(f"SetGainMode serialized: {message.hex()}")
    return message

def message_set_gain(value: int) -> bytes:
    """Set gain value"""
    message = _encode_field(1, 0, _encode_varint(value))
    logger.debug(f"SetGain serialized: {message.hex()}")
    return message

async def set_gain_mode(ws_handler, mode: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set gain mode"""
    if not ws_handler.ip_dwarf:
        return
    
    mode_str = "AUTO" if mode == GAIN_MODE_AUTO else "MANUAL"
    logger.info(f"📷 Setting gain mode: {mode_str}")
    
    message_data = message_set_gain_mode(mode)
    cmd = CMD_CAMERA_TELE_SET_GAIN_MODE if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_GAIN
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def set_gain(ws_handler, value: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set gain value (0-300 typical range)"""
    if not ws_handler.ip_dwarf:
        return
    
    logger.info(f"📷 Setting gain: {value}")
    
    message_data = message_set_gain(value)
    cmd = CMD_CAMERA_TELE_SET_GAIN if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_GAIN
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

# ============================================================================
# White Balance Functions
# ============================================================================

def message_set_wb_mode(mode: int) -> bytes:
    """Set white balance mode"""
    message = _encode_field(1, 0, _encode_varint(mode))
    logger.debug(f"SetWBMode serialized: {message.hex()}")
    return message

async def set_wb_mode(ws_handler, mode: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set white balance mode"""
    if not ws_handler.ip_dwarf:
        return
    
    mode_str = "AUTO" if mode == WB_MODE_AUTO else "MANUAL"
    logger.info(f"📷 Setting WB mode: {mode_str}")
    
    message_data = message_set_wb_mode(mode)
    cmd = CMD_CAMERA_TELE_SET_WB_MODE if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_WB_MODE
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

# ============================================================================
# IR Cut Filter Functions
# ============================================================================

def message_set_ircut(mode: int) -> bytes:
    """Set IR cut filter"""
    message = _encode_field(1, 0, _encode_varint(mode))
    logger.debug(f"SetIRCut serialized: {message.hex()}")
    return message

async def set_ircut(ws_handler, mode: int, callback=None):
    """Set IR cut filter (Tele camera only)"""
    if not ws_handler.ip_dwarf:
        return
    
    mode_str = "CUT" if mode == IR_CUT else "PASS"
    logger.info(f"📷 Setting IR filter: {mode_str}")
    
    message_data = message_set_ircut(mode)
    packet = ws_handler.create_packet(MODULE_CAMERA_TELE, CMD_CAMERA_TELE_SET_IRCUT, message_data)
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

# ============================================================================
# Image Quality Parameters
# ============================================================================

def message_set_brightness(value: int) -> bytes:
    """Set brightness"""
    message = _encode_field(1, 0, _encode_varint(value))
    return message

def message_set_contrast(value: int) -> bytes:
    """Set contrast"""
    message = _encode_field(1, 0, _encode_varint(value))
    return message

def message_set_saturation(value: int) -> bytes:
    """Set saturation"""
    message = _encode_field(1, 0, _encode_varint(value))
    return message

def message_set_sharpness(value: int) -> bytes:
    """Set sharpness"""
    message = _encode_field(1, 0, _encode_varint(value))
    return message

async def set_brightness(ws_handler, value: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set brightness (0-255 typical)"""
    if not ws_handler.ip_dwarf:
        return
    
    logger.info(f"📷 Setting brightness: {value}")
    message_data = message_set_brightness(value)
    cmd = CMD_CAMERA_TELE_SET_BRIGHTNESS if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_BRIGHTNESS
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    if callback:
        callback()

async def set_contrast(ws_handler, value: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set contrast (0-255 typical)"""
    if not ws_handler.ip_dwarf:
        return
    
    logger.info(f"📷 Setting contrast: {value}")
    message_data = message_set_contrast(value)
    cmd = CMD_CAMERA_TELE_SET_CONTRAST if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_CONTRAST
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    if callback:
        callback()

async def set_saturation(ws_handler, value: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set saturation (0-255 typical)"""
    if not ws_handler.ip_dwarf:
        return
    
    logger.info(f"📷 Setting saturation: {value}")
    message_data = message_set_saturation(value)
    cmd = CMD_CAMERA_TELE_SET_SATURATION if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_SATURATION
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    if callback:
        callback()

async def set_sharpness(ws_handler, value: int, module: int = MODULE_CAMERA_TELE, callback=None):
    """Set sharpness (0-255 typical)"""
    if not ws_handler.ip_dwarf:
        return
    
    logger.info(f"📷 Setting sharpness: {value}")
    message_data = message_set_sharpness(value)
    cmd = CMD_CAMERA_TELE_SET_SHARPNESS if module == MODULE_CAMERA_TELE else CMD_CAMERA_WIDE_SET_SHARPNESS
    packet = ws_handler.create_packet(module, cmd, message_data)
    ws_handler.send_packet(packet)
    if callback:
        callback()
