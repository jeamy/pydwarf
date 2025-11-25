"""
DWARF II Astro API - Python Port
Basierend auf astro.js aus dwarfii_api
"""
import logging
from ..services.proto import base_pb2, astro_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# Astro Constants
# ============================================================================

# Solar System Targets
SOLAR_MERCURY = 1
SOLAR_VENUS = 2
SOLAR_MARS = 3
SOLAR_JUPITER = 4
SOLAR_SATURN = 5
SOLAR_URANUS = 6
SOLAR_NEPTUNE = 7
SOLAR_MOON = 8
SOLAR_SUN = 9

# ============================================================================
# Astro Functions
# ============================================================================

def message_astro_calibration_start() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_CALIBRATION
    """
    message = astro_pb2.ReqStartCalibration()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStartCalibration serialized: {serialized.hex()}")
    return serialized

def message_astro_calibration_stop() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_CALIBRATION
    """
    message = astro_pb2.ReqStopCalibration()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopCalibration serialized: {serialized.hex()}")
    return serialized

def message_astro_goto_dso(
    ra: float,
    dec: float,
    target_name: str = ""
) -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_GOTO_DSO
    """
    message = astro_pb2.ReqGotoDSO()
    message.ra = ra
    message.dec = dec
    message.target_name = target_name
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqGotoDSO serialized: {serialized.hex()}")
    return serialized

def message_astro_goto_solar(
    index: int,
    lat: float,
    lon: float,
    target_name: str = ""
) -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_GOTO_SOLAR_SYSTEM
    Note: lat/lon are user's coordinates
    """
    message = astro_pb2.ReqGotoSolarSystem()
    message.index = index
    message.lat = lat
    message.lon = lon
    message.target_name = target_name
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqGotoSolarSystem serialized: {serialized.hex()}")
    return serialized

def message_astro_goto_stop() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_GOTO
    """
    message = astro_pb2.ReqStopGoto()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopGoto serialized: {serialized.hex()}")
    return serialized

def message_astro_stacking_start() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_CAPTURE_RAW_LIVE_STACKING
    """
    message = astro_pb2.ReqCaptureRawLiveStacking()
    serialized = message.SerializeToString()
    logger.debug(f"ReqCaptureRawLiveStacking serialized: {serialized.hex()}")
    return serialized

def message_astro_stacking_stop() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_CAPTURE_RAW_LIVE_STACKING
    """
    message = astro_pb2.ReqStopCaptureRawLiveStacking()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopCaptureRawLiveStacking serialized: {serialized.hex()}")
    return serialized

def message_astro_dark_start(reshoot: int = 0) -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_CAPTURE_RAW_DARK
    """
    message = astro_pb2.ReqCaptureDarkFrame()
    message.reshoot = reshoot
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqCaptureDarkFrame serialized: {serialized.hex()}")
    return serialized

def message_astro_dark_stop() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_CAPTURE_RAW_DARK
    """
    message = astro_pb2.ReqStopCaptureDarkFrame()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopCaptureDarkFrame serialized: {serialized.hex()}")
    return serialized

def message_astro_go_live() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_GO_LIVE
    """
    message = astro_pb2.ReqGoLive()
    serialized = message.SerializeToString()
    logger.debug(f"ReqGoLive serialized: {serialized.hex()}")
    return serialized

def message_astro_track_special_target(index: int, lat: float, lon: float) -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_TRACK_SPECIAL_TARGET
    Track Sun (0) or Moon (1)
    """
    message = astro_pb2.ReqTrackSpecialTarget()
    message.index = index
    message.lat = lat
    message.lon = lon
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqTrackSpecialTarget serialized: {serialized.hex()}")
    return serialized

def message_astro_stop_track_special_target() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_TRACK_SPECIAL_TARGET
    """
    message = astro_pb2.ReqStopTrackSpecialTarget()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopTrackSpecialTarget serialized: {serialized.hex()}")
    return serialized

def message_astro_one_click_goto_dso(ra: float, dec: float, target_name: str = "") -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_ONE_CLICK_GOTO_DSO
    """
    message = astro_pb2.ReqOneClickGotoDSO()
    message.ra = ra
    message.dec = dec
    message.target_name = target_name
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqOneClickGotoDSO serialized: {serialized.hex()}")
    return serialized

def message_astro_one_click_goto_solar(index: int, lat: float, lon: float, target_name: str = "") -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_ONE_CLICK_GOTO_SOLAR_SYSTEM
    """
    message = astro_pb2.ReqOneClickGotoSolarSystem()
    message.index = index
    message.lat = lat
    message.lon = lon
    message.target_name = target_name
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqOneClickGotoSolarSystem serialized: {serialized.hex()}")
    return serialized

def message_astro_stop_one_click_goto() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_ONE_CLICK_GOTO
    """
    message = astro_pb2.ReqStopOneClickGoto()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopOneClickGoto serialized: {serialized.hex()}")
    return serialized

def message_astro_start_eq_solving() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_START_EQ_SOLVING
    """
    message = astro_pb2.ReqStartEQSolving()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStartEQSolving serialized: {serialized.hex()}")
    return serialized

def message_astro_stop_eq_solving() -> bytes:
    """
    Create Encoded Packet for CMD_ASTRO_STOP_EQ_SOLVING
    """
    message = astro_pb2.ReqStopEQSolving()
    serialized = message.SerializeToString()
    logger.debug(f"ReqStopEQSolving serialized: {serialized.hex()}")
    return serialized

# ============================================================================
# Helper Functions
# ============================================================================

async def start_calibration(ws_handler, callback=None):
    """Start calibration"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("✨ Starting Calibration...")
    
    message_data = message_astro_calibration_start()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_CALIBRATION,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_calibration(ws_handler, callback=None):
    """Stop calibration"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("✨ Stopping Calibration")
    
    message_data = message_astro_calibration_stop()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_STOP_CALIBRATION,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def goto_dso(
    ws_handler,
    ra: float,
    dec: float,
    target_name: str = "",
    callback=None
):
    """Goto Deep Space Object"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🚀 Goto DSO: {target_name} (RA={ra}, DEC={dec})")
    
    message_data = message_astro_goto_dso(ra, dec, target_name)
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_GOTO_DSO,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def goto_solar(
    ws_handler,
    index: int,
    lat: float,
    lon: float,
    target_name: str = "",
    callback=None
):
    """Goto Solar System Object"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🚀 Goto Solar: {target_name} (Index={index})")
    
    message_data = message_astro_goto_solar(index, lat, lon, target_name)
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_GOTO_SOLAR_SYSTEM,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_goto(ws_handler, callback=None):
    """Stop Goto"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🛑 Stopping Goto")
    
    message_data = message_astro_goto_stop()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_STOP_GOTO,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def start_stacking(ws_handler, callback=None):
    """Start Live Stacking"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🌌 Starting Live Stacking...")
    
    message_data = message_astro_stacking_start()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_CAPTURE_RAW_LIVE_STACKING,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_stacking(ws_handler, callback=None):
    """Stop Live Stacking"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🌌 Stopping Live Stacking")
    
    message_data = message_astro_stacking_stop()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_STOP_CAPTURE_RAW_LIVE_STACKING,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def go_live(ws_handler, callback=None):
    """Go Live (Stop Stacking/Goto and return to live view)"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("📺 Go Live")
    
    message_data = message_astro_go_live()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_GO_LIVE,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def track_special_target(
    ws_handler,
    index: int,
    lat: float,
    lon: float,
    callback=None
):
    """Track Sun (0) or Moon (1)"""
    if not ws_handler.ip_dwarf:
        return
        
    target_name = "Sun" if index == 0 else "Moon"
    logger.info(f"🌞 Tracking {target_name}")
    
    message_data = message_astro_track_special_target(index, lat, lon)
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_TRACK_SPECIAL_TARGET,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_track_special_target(ws_handler, callback=None):
    """Stop tracking Sun/Moon"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🌞 Stop tracking special target")
    
    message_data = message_astro_stop_track_special_target()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_STOP_TRACK_SPECIAL_TARGET,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def one_click_goto_dso(
    ws_handler,
    ra: float,
    dec: float,
    target_name: str = "",
    callback=None
):
    """One-Click GoTo DSO (includes calibration, focus, goto)"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🚀 One-Click GoTo DSO: {target_name} (RA={ra}, DEC={dec})")
    
    message_data = message_astro_one_click_goto_dso(ra, dec, target_name)
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_ONE_CLICK_GOTO_DSO,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def one_click_goto_solar(
    ws_handler,
    index: int,
    lat: float,
    lon: float,
    target_name: str = "",
    callback=None
):
    """One-Click GoTo Solar System Object"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"🚀 One-Click GoTo Solar: {target_name} (Index={index})")
    
    message_data = message_astro_one_click_goto_solar(index, lat, lon, target_name)
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_ONE_CLICK_GOTO_SOLAR_SYSTEM,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_one_click_goto(ws_handler, callback=None):
    """Stop One-Click GoTo"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🛑 Stopping One-Click GoTo")
    
    message_data = message_astro_stop_one_click_goto()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_STOP_ONE_CLICK_GOTO,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def start_eq_solving(ws_handler, callback=None):
    """Start EQ Solving (Equatorial Mount Plate Solving)"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🔭 Starting EQ Solving")
    
    message_data = message_astro_start_eq_solving()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_START_EQ_SOLVING,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_eq_solving(ws_handler, callback=None):
    """Stop EQ Solving"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info("🔭 Stopping EQ Solving")
    
    message_data = message_astro_stop_eq_solving()
    packet = ws_handler.create_packet(
        MODULE_ASTRO,
        CMD_ASTRO_STOP_EQ_SOLVING,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()
