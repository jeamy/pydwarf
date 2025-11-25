"""
Camera Parameters API Endpoints
Erweiterte Kamera-Einstellungen: Exposure, Gain, White Balance, IR Cut, Bildqualität
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class SetExposureModeRequest(BaseModel):
    """Belichtungsmodus setzen"""
    mode: int  # 0: Auto, 1: Manual
    camera: Literal["tele", "wide"] = "tele"


class SetExposureRequest(BaseModel):
    """Belichtungszeit setzen"""
    value: int  # Belichtungszeit in Mikrosekunden
    camera: Literal["tele", "wide"] = "tele"


class SetGainModeRequest(BaseModel):
    """Gain-Modus setzen"""
    mode: int  # 0: Auto, 1: Manual
    camera: Literal["tele", "wide"] = "tele"


class SetGainRequest(BaseModel):
    """Gain-Wert setzen"""
    value: int  # Gain-Wert (0-300 typisch)
    camera: Literal["tele", "wide"] = "tele"


class SetWBModeRequest(BaseModel):
    """Weißabgleich-Modus setzen"""
    mode: int  # 0: Auto, 1: Manual
    camera: Literal["tele", "wide"] = "tele"


class SetIRCutRequest(BaseModel):
    """IR-Filter setzen"""
    mode: int  # 0: IR Cut (normal), 1: IR Pass (astro)


class SetImageQualityRequest(BaseModel):
    """Bildqualität-Parameter setzen"""
    value: int  # 0-255
    camera: Literal["tele", "wide"] = "tele"


# ============================================================================
# Manual Protobuf Encoding
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


def _create_single_int_message(value: int) -> bytes:
    """Create message with single int field"""
    return _encode_field(1, 0, _encode_varint(value))


# ============================================================================
# Exposure
# ============================================================================

@router.post("/exposure/mode")
async def set_exposure_mode(ip: str, request: SetExposureModeRequest):
    """Belichtungsmodus setzen (Auto/Manual)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.mode)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_EXP_MODE if request.camera == "tele" else CMD_CAMERA_WIDE_SET_EXP_MODE
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            mode_str = "Auto" if request.mode == 0 else "Manual"
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": mode_str,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/exposure/value")
async def set_exposure(ip: str, request: SetExposureRequest):
    """Belichtungszeit setzen (in Mikrosekunden)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.value)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_EXP if request.camera == "tele" else CMD_CAMERA_WIDE_SET_EXP
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "value_us": request.value,
                "value_s": request.value / 1_000_000,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Gain
# ============================================================================

@router.post("/gain/mode")
async def set_gain_mode(ip: str, request: SetGainModeRequest):
    """Gain-Modus setzen (Auto/Manual)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.mode)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_GAIN_MODE if request.camera == "tele" else CMD_CAMERA_WIDE_SET_GAIN
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            mode_str = "Auto" if request.mode == 0 else "Manual"
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": mode_str,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/gain/value")
async def set_gain(ip: str, request: SetGainRequest):
    """Gain-Wert setzen (0-300 typisch)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.value)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_GAIN if request.camera == "tele" else CMD_CAMERA_WIDE_SET_GAIN
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "value": request.value,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# White Balance
# ============================================================================

@router.post("/wb/mode")
async def set_wb_mode(ip: str, request: SetWBModeRequest):
    """Weißabgleich-Modus setzen (Auto/Manual)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.mode)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_WB_MODE if request.camera == "tele" else CMD_CAMERA_WIDE_SET_WB_MODE
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            mode_str = "Auto" if request.mode == 0 else "Manual"
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": mode_str,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# IR Cut Filter (nur Tele)
# ============================================================================

@router.post("/ircut")
async def set_ircut(ip: str, request: SetIRCutRequest):
    """IR-Filter setzen (nur Tele-Kamera)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.mode)
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_SET_IRCUT,
            req_data,
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            mode_str = "Cut (Normal)" if request.mode == 0 else "Pass (Astro)"
            
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


# ============================================================================
# Image Quality
# ============================================================================

@router.post("/brightness")
async def set_brightness(ip: str, request: SetImageQualityRequest):
    """Helligkeit setzen (0-255)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.value)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_BRIGHTNESS if request.camera == "tele" else CMD_CAMERA_WIDE_SET_BRIGHTNESS
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "value": request.value,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/contrast")
async def set_contrast(ip: str, request: SetImageQualityRequest):
    """Kontrast setzen (0-255)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.value)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_CONTRAST if request.camera == "tele" else CMD_CAMERA_WIDE_SET_CONTRAST
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "value": request.value,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/saturation")
async def set_saturation(ip: str, request: SetImageQualityRequest):
    """Sättigung setzen (0-255)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.value)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_SATURATION if request.camera == "tele" else CMD_CAMERA_WIDE_SET_SATURATION
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "value": request.value,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/sharpness")
async def set_sharpness(ip: str, request: SetImageQualityRequest):
    """Schärfe setzen (0-255)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_single_int_message(request.value)
        
        module = MODULE_CAMERA_TELE if request.camera == "tele" else MODULE_CAMERA_WIDE
        cmd = CMD_CAMERA_TELE_SET_SHARPNESS if request.camera == "tele" else CMD_CAMERA_WIDE_SET_SHARPNESS
        
        response = await ws_client.send_command(
            module, cmd, req_data, wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "value": request.value,
                "camera": request.camera
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()
