"""
Tracking API Endpoints
Objekt-Verfolgung, Sentry-Modus, Multi-Object Tracking
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class StartTrackingRequest(BaseModel):
    """Objekt-Tracking starten"""
    x: int  # x-Koordinate der Box (oben links)
    y: int  # y-Koordinate der Box (oben links)
    w: int  # Breite der Box
    h: int  # Höhe der Box


class StartSentryRequest(BaseModel):
    """Sentry-Modus starten"""
    mode: int = 0  # 0: Normal, 1: UFO


class MOTTrackOneRequest(BaseModel):
    """MOT: Spezifisches Objekt tracken"""
    target_id: int


# ============================================================================
# Manual Protobuf Encoding (da tracking_pb2 fehlt)
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


def _create_req_start_track(x: int, y: int, w: int, h: int) -> bytes:
    """Create ReqStartTrack message"""
    message = b""
    message += _encode_field(1, 0, _encode_varint(x))
    message += _encode_field(2, 0, _encode_varint(y))
    message += _encode_field(3, 0, _encode_varint(w))
    message += _encode_field(4, 0, _encode_varint(h))
    return message


def _create_req_start_sentry(mode: int) -> bytes:
    """Create ReqStartSentryMode message"""
    return _encode_field(1, 0, _encode_varint(mode))


def _create_req_mot_track_one(target_id: int) -> bytes:
    """Create ReqMOTTrackOne message"""
    return _encode_field(1, 0, _encode_varint(target_id))


# ============================================================================
# Standard Tracking
# ============================================================================

@router.post("/start")
async def start_tracking(ip: str, request: StartTrackingRequest):
    """Objekt-Tracking starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_req_start_track(
            request.x, request.y, request.w, request.h
        )
        
        response = await ws_client.send_command(
            MODULE_TRACK,
            CMD_TRACK_START_TRACK,
            req_data,
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "box": {"x": request.x, "y": request.y, "w": request.w, "h": request.h}
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/stop")
async def stop_tracking(ip: str):
    """Objekt-Tracking stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        # Empty message
        req_data = b""
        
        response = await ws_client.send_command(
            MODULE_TRACK,
            CMD_TRACK_STOP_TRACK,
            req_data,
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
# Sentry Mode
# ============================================================================

@router.post("/sentry/start")
async def start_sentry_mode(ip: str, request: StartSentryRequest):
    """Sentry-Modus starten (Wächter-Modus)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_req_start_sentry(request.mode)
        
        response = await ws_client.send_command(
            MODULE_TRACK,
            CMD_SENTRY_MODE_START,
            req_data,
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            mode_str = "UFO" if request.mode == 1 else "Normal"
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": mode_str
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/sentry/stop")
async def stop_sentry_mode(ip: str):
    """Sentry-Modus stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        # Empty message
        req_data = b""
        
        response = await ws_client.send_command(
            MODULE_TRACK,
            CMD_SENTRY_MODE_STOP,
            req_data,
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
# Multi-Object Tracking (MOT)
# ============================================================================

@router.post("/mot/start")
async def start_mot(ip: str):
    """Multi-Object Tracking starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        # Empty message
        req_data = b""
        
        response = await ws_client.send_command(
            MODULE_TRACK,
            CMD_MOT_START,
            req_data,
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


@router.post("/mot/track-one")
async def mot_track_one(ip: str, request: MOTTrackOneRequest):
    """MOT: Spezifisches Objekt tracken"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_req_mot_track_one(request.target_id)
        
        response = await ws_client.send_command(
            MODULE_TRACK,
            CMD_MOT_TRACK_ONE,
            req_data,
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "target_id": request.target_id
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()
