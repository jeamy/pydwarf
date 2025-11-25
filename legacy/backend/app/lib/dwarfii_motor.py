"""
DWARF II Motor API - Python Port
Basierend auf step_motor.js aus dwarfii_api
"""
import logging
from ..services.proto import base_pb2, motor_pb2
from ..utils.constants import *

logger = logging.getLogger(__name__)

# ============================================================================
# Motor Constants
# ============================================================================
AXIS_AZIMUTH = 0  # Rotation
AXIS_ALTITUDE = 1 # Pitch

# Direction
DIR_LEFT_DOWN = 0
DIR_RIGHT_UP = 1

# ============================================================================
# Motor Functions
# ============================================================================

def message_motor_run(
    axis: int,
    speed: float,
    direction: int,
    speed_ramping: int = 100,
    resolution_level: int = 0
) -> bytes:
    """
    Create Encoded Packet for CMD_STEP_MOTOR_RUN
    
    Args:
        axis: 0: Azimuth (Rotation), 1: Altitude (Pitch)
        speed: 0.1 - 30 degrees/s
        direction: 0: left/down, 1: right/up
        speed_ramping: 0-1000 (default 100)
        resolution_level: 0-8 (default 0)
    """
    message = motor_pb2.ReqMotorRun()
    message.id = axis
    message.speed = speed
    message.direction = bool(direction)
    message.speed_ramping = speed_ramping
    message.resolution_level = resolution_level
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqMotorRun serialized: {serialized.hex()}")
    return serialized

def message_motor_stop(axis: int) -> bytes:
    """
    Create Encoded Packet for CMD_STEP_MOTOR_STOP
    
    Args:
        axis: 0: Azimuth (Rotation), 1: Altitude (Pitch)
    """
    message = motor_pb2.ReqMotorStop()
    message.id = axis
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqMotorStop serialized: {serialized.hex()}")
    return serialized

def message_motor_joystick(
    vector_angle: float,
    vector_length: float,
    speed: float
) -> bytes:
    """
    Create Encoded Packet for CMD_STEP_MOTOR_SERVICE_JOYSTICK
    """
    message = motor_pb2.ReqMotorServiceJoystick()
    message.vector_angle = vector_angle
    message.vector_length = vector_length
    message.speed = speed
    
    serialized = message.SerializeToString()
    logger.debug(f"ReqMotorServiceJoystick serialized: {serialized.hex()}")
    return serialized

def message_motor_joystick_stop() -> bytes:
    """
    Create Encoded Packet for CMD_STEP_MOTOR_SERVICE_JOYSTICK_STOP
    """
    # Empty message
    message = motor_pb2.ReqMotorServiceJoystickStop()
    serialized = message.SerializeToString()
    logger.debug(f"ReqMotorServiceJoystickStop serialized: {serialized.hex()}")
    return serialized

# ============================================================================
# Helper Functions
# ============================================================================

async def start_motor(
    ws_handler,
    axis: int,
    speed: float,
    direction: int,
    callback=None
):
    """Start motor movement"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"⚙️ Starting motor: axis={axis}, speed={speed}, dir={direction}")
    
    message_data = message_motor_run(axis, speed, direction)
    packet = ws_handler.create_packet(
        MODULE_MOTOR,
        CMD_STEP_MOTOR_RUN,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def stop_motor(
    ws_handler,
    axis: int,
    callback=None
):
    """Stop motor movement"""
    if not ws_handler.ip_dwarf:
        return
        
    logger.info(f"⚙️ Stopping motor: axis={axis}")
    
    message_data = message_motor_stop(axis)
    packet = ws_handler.create_packet(
        MODULE_MOTOR,
        CMD_STEP_MOTOR_STOP,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def joystick_move(
    ws_handler,
    x: float,
    y: float,
    speed: float = 1.0,
    callback=None
):
    """
    Move using joystick vector (x, y)
    Calculates angle and length from x, y coordinates (-1 to 1)
    """
    import math
    
    # Calculate angle (0-360, 0 is positive x-axis, counter-clockwise)
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
        
    # Calculate length (0-1)
    length = min(math.sqrt(x*x + y*y), 1.0)
    
    logger.info(f"🕹️ Joystick: x={x}, y={y} -> angle={angle:.1f}, len={length:.2f}")
    
    message_data = message_motor_joystick(angle, length, speed)
    packet = ws_handler.create_packet(
        MODULE_MOTOR,
        CMD_STEP_MOTOR_SERVICE_JOYSTICK,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()

async def joystick_stop(ws_handler, callback=None):
    """Stop joystick movement"""
    logger.info("🕹️ Stopping joystick")
    
    message_data = message_motor_joystick_stop()
    packet = ws_handler.create_packet(
        MODULE_MOTOR,
        CMD_STEP_MOTOR_SERVICE_JOYSTICK_STOP,
        message_data
    )
    ws_handler.send_packet(packet)
    
    if callback:
        callback()
