"""
DWARF II Focus API - Python Port
Basierend auf focus.js aus dwarfii_api
"""
import logging
from ..services.proto import base_pb2, focus_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# Focus Constants
# ============================================================================

# Auto Focus Mode
AF_MODE_GLOBAL = 0
AF_MODE_AREA = 1

# Astro Focus Mode
ASTRO_AF_MODE_SLOW = 0
ASTRO_AF_MODE_FAST = 1

# Manual Focus Direction
FOCUS_DIR_FAR = 0
FOCUS_DIR_NEAR = 1

# ============================================================================
# Focus Functions
# ============================================================================

def message_focus_auto(
    mode: int = AF_MODE_GLOBAL,
    center_x: int = 0,
    center_y: int = 0
) -> bytes:
    """
    Create Encoded Packet for CMD_FOCUS_AUTO_FOCUS
    """
    message = focus_pb2.ReqNormalAutoFocus()
    message.mode = mode
    message.center_x = center_x
    message.center_y = center_y
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqNormalAutoFocus serialized: {serialized.hex()}")
    return serialized

def message_focus_manual_single(direction: int) -> bytes:
    """
    Create Encoded Packet for CMD_FOCUS_MANUAL_SINGLE_STEP_FOCUS
    """
    message = focus_pb2.ReqManualSingleStepFocus()
    message.direction = direction
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqManualSingleStepFocus serialized: {serialized.hex()}")
    return serialized

def message_focus_start_manual_continue(direction: int) -> bytes:
    """
    Create Encoded Packet for CMD_FOCUS_START_MANUAL_CONTINU_FOCUS
    """
    message = focus_pb2.ReqManualContinuFocus()
    message.direction = direction
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqManualContinuFocus serialized: {serialized.hex()}")
    return serialized

def message_focus_stop_manual_continue() -> bytes:
    """
    Create Encoded Packet for CMD_FOCUS_STOP_MANUAL_CONTINU_FOCUS
    """
    message = focus_pb2.ReqStopManualContinuFocus()
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopManualContinuFocus serialized: {serialized.hex()}")
    return serialized

def message_focus_astro_auto(mode: int = ASTRO_AF_MODE_SLOW) -> bytes:
    """
    Create Encoded Packet for CMD_FOCUS_START_ASTRO_AUTO_FOCUS
    """
    message = focus_pb2.ReqAstroAutoFocus()
    message.mode = mode
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqAstroAutoFocus serialized: {serialized.hex()}")
    return serialized

def message_focus_stop_astro_auto() -> bytes:
    """
    Create Encoded Packet for CMD_FOCUS_STOP_ASTRO_AUTO_FOCUS
    """
    message = focus_pb2.ReqStopAstroAutoFocus()
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopAstroAutoFocus serialized: {serialized.hex()}")
    return serialized

# ============================================================================
# Helper Functions
# ============================================================================

async def start_auto_focus(
    ws_handler,
    mode: int = AF_MODE_GLOBAL,
    x: int = 0,
    y: int = 0,
    callback=None
):
    """Start normal auto focus"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🔍 Starting Auto Focus (mode={mode})...")
    
    message_data = message_focus_auto(mode, x, y)
    packet = ws_handler.create_packet(
        MODULE_FOCUS,
        CMD_FOCUS_AUTO_FOCUS,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def manual_focus_step(
    ws_handler,
    direction: int,
    callback=None
):
    """Single step manual focus"""
    if not ws_handler.ip_dwarf:
        return
        
    dir_str = "NEAR" if direction == FOCUS_DIR_NEAR else "FAR"
    logger.info(f"🔍 Manual Focus Step: {dir_str}")
    
    message_data = message_focus_manual_single(direction)
    packet = ws_handler.create_packet(
        MODULE_FOCUS,
        CMD_FOCUS_MANUAL_SINGLE_STEP_FOCUS,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def start_manual_focus_continuous(
    ws_handler,
    direction: int,
    callback=None
):
    """Start continuous manual focus"""
    if not ws_handler.ip_dwarf:
        return
        
    dir_str = "NEAR" if direction == FOCUS_DIR_NEAR else "FAR"
    logger.info(f"🔍 Start Continuous Focus: {dir_str}")
    
    message_data = message_focus_start_manual_continue(direction)
    packet = ws_handler.create_packet(
        MODULE_FOCUS,
        CMD_FOCUS_START_MANUAL_CONTINU_FOCUS,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_manual_focus_continuous(ws_handler, callback=None):
    """Stop continuous manual focus"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🔍 Stop Continuous Focus")
    
    message_data = message_focus_stop_manual_continue()
    packet = ws_handler.create_packet(
        MODULE_FOCUS,
        CMD_FOCUS_STOP_MANUAL_CONTINU_FOCUS,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def start_astro_auto_focus(
    ws_handler,
    mode: int = ASTRO_AF_MODE_SLOW,
    callback=None
):
    """Start astro auto focus"""
    if not ws_handler.ip_dwarf:
        return
        
    mode_str = "FAST" if mode == ASTRO_AF_MODE_FAST else "SLOW"
    logger.info(f"⭐ Starting Astro Auto Focus ({mode_str})...")
    
    message_data = message_focus_astro_auto(mode)
    packet = ws_handler.create_packet(
        MODULE_FOCUS,
        CMD_FOCUS_START_ASTRO_AUTO_FOCUS,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_astro_auto_focus(ws_handler, callback=None):
    """Stop astro auto focus"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("⭐ Stopping Astro Auto Focus")
    
    message_data = message_focus_stop_astro_auto()
    packet = ws_handler.create_packet(
        MODULE_FOCUS,
        CMD_FOCUS_STOP_ASTRO_AUTO_FOCUS,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()
