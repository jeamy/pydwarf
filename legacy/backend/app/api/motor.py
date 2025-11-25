"""
Motor API Endpoints
Motor-Steuerung: Rotation, Pitch, Joystick
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import motor_pb2, base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class MotorRunRequest(BaseModel):
    """Motor bewegen"""
    motor_id: int  # 0: Rotation, 1: Pitch
    speed: float  # Geschwindigkeit
    direction: bool  # False: links/unten, True: rechts/oben
    speed_ramping: int = 500  # Beschleunigung (0-1000)
    resolution_level: int = 5  # Subdivision (0-8)


class MotorStopRequest(BaseModel):
    """Motor stoppen"""
    motor_id: int  # 0: Rotation, 1: Pitch


class JoystickRequest(BaseModel):
    """Joystick-Steuerung"""
    vector_angle: float  # Richtungs-Winkel (0-360°)
    vector_length: float  # Länge (0-1)
    speed: float  # Geschwindigkeit (0.1-30 °/s)


class JoystickFixedAngleRequest(BaseModel):
    """Joystick Fixed Angle"""
    vector_angle: float
    vector_length: float
    speed: float


class DualCameraLinkageRequest(BaseModel):
    """Dual-Kamera-Linkage"""
    x: int
    y: int


# ============================================================================
# Motor-Steuerung
# ============================================================================

@router.post("/run")
async def run_motor(ip: str, request: MotorRunRequest):
    """
    Motor bewegen
    motor_id: 0 = Rotation (Azimut), 1 = Pitch (Höhe)
    direction: False = links/unten, True = rechts/oben
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = motor_pb2.ReqMotorRun()
        req.id = request.motor_id
        req.speed = request.speed
        req.direction = request.direction
        req.speed_ramping = request.speed_ramping
        req.resolution_level = request.resolution_level
        
        response = await ws_client.send_command(
            MODULE_MOTOR,
            CMD_STEP_MOTOR_RUN,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            res = motor_pb2.ResMotor()
            res.ParseFromString(response.data)
            
            motor_name = "Rotation" if request.motor_id == 0 else "Pitch"
            direction_name = "rechts/oben" if request.direction else "links/unten"
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "motor": motor_name,
                "direction": direction_name,
                "speed": request.speed
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/stop")
async def stop_motor(ip: str, request: MotorStopRequest):
    """
    Motor stoppen
    motor_id: 0 = Rotation, 1 = Pitch
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = motor_pb2.ReqMotorStop()
        req.id = request.motor_id
        
        response = await ws_client.send_command(
            MODULE_MOTOR,
            CMD_STEP_MOTOR_STOP,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            res = motor_pb2.ResMotor()
            res.ParseFromString(response.data)
            
            motor_name = "Rotation" if request.motor_id == 0 else "Pitch"
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "motor": motor_name
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Joystick-Steuerung
# ============================================================================

@router.post("/joystick/start")
async def start_joystick(ip: str, request: JoystickRequest):
    """
    Joystick-Steuerung starten
    vector_angle: 0-360° (0=Norden, 90=Osten, 180=Süden, 270=Westen)
    vector_length: 0-1 (Intensität)
    speed: 0.1-30 °/s
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = motor_pb2.ReqMotorServiceJoystick()
        req.vector_angle = request.vector_angle
        req.vector_length = request.vector_length
        req.speed = request.speed
        
        response = await ws_client.send_command(
            MODULE_MOTOR,
            CMD_STEP_MOTOR_SERVICE_JOYSTICK,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "angle": request.vector_angle,
                "length": request.vector_length,
                "speed": request.speed
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/joystick/fixed-angle")
async def joystick_fixed_angle(ip: str, request: JoystickFixedAngleRequest):
    """
    Joystick Fixed Angle
    Bewegung in fester Richtung
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = motor_pb2.ReqMotorServiceJoystickFixedAngle()
        req.vector_angle = request.vector_angle
        req.vector_length = request.vector_length
        req.speed = request.speed
        
        response = await ws_client.send_command(
            MODULE_MOTOR,
            CMD_STEP_MOTOR_SERVICE_JOYSTICK_FIXED_ANGLE,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "angle": request.vector_angle
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/joystick/stop")
async def stop_joystick(ip: str):
    """Joystick-Steuerung stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = motor_pb2.ReqMotorServiceJoystickStop()
        
        response = await ws_client.send_command(
            MODULE_MOTOR,
            CMD_STEP_MOTOR_SERVICE_JOYSTICK_STOP,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Dual-Kamera-Linkage
# ============================================================================

@router.post("/dual-camera-linkage")
async def dual_camera_linkage(ip: str, request: DualCameraLinkageRequest):
    """
    Dual-Kamera-Linkage
    Synchronisierte Bewegung beider Kameras
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = motor_pb2.ReqDualCameraLinkage()
        req.x = request.x
        req.y = request.y
        
        response = await ws_client.send_command(
            MODULE_MOTOR,
            CMD_STEP_MOTOR_SERVICE_DUAL_CAMERA_LINKAGE,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "x": request.x,
                "y": request.y
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()
