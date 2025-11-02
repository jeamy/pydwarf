"""
Camera API Endpoints
Kamera-Steuerung (Tele & Wide)
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from ..services.dwarf_client import DwarfHTTPClient
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import camera_pb2, base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class CameraOpen(BaseModel):
    """Kamera öffnen"""
    binning: bool = False
    rtsp_encode_type: int = 0  # 0: 4K, 1: 1080p


class CameraParams(BaseModel):
    """Kamera-Parameter"""
    exp_mode: int = 0
    exp_index: int = 0
    gain_mode: int = 0
    gain_index: int = 0
    ircut_value: int = 0
    wb_mode: int = 0
    wb_index_type: int = 0
    wb_index: int = 0
    brightness: int = 128
    contrast: int = 128
    hue: int = 128
    saturation: int = 128
    sharpness: int = 50
    jpg_quality: int = 90


class TimelapseParams(BaseModel):
    """Zeitraffer-Parameter"""
    interval: int  # Sekunden
    count: int     # Anzahl Aufnahmen


class BurstParams(BaseModel):
    """Serienaufnahme-Parameter"""
    count: int = 10


# ============================================================================
# Teleobjektiv-Kamera
# ============================================================================

@router.post("/tele/open")
async def open_tele_camera(ip: str, params: CameraOpen):
    """Teleobjektiv-Kamera öffnen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqOpenCamera()
        req.binning = params.binning
        req.rtsp_encode_type = params.rtsp_encode_type
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_OPEN_CAMERA,
            req.SerializeToString(),
            wait_response=True,
            timeout=10.0
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


@router.post("/tele/close")
async def close_tele_camera(ip: str):
    """Teleobjektiv-Kamera schließen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_CLOSE_CAMERA,
            b"",
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


@router.post("/tele/photo")
async def take_photo(ip: str):
    """Foto aufnehmen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqPhoto()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_PHOTOGRAPH,
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


@router.post("/tele/burst/start")
async def start_burst(ip: str, params: BurstParams):
    """Serienaufnahme starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqBurst()
        req.count = params.count
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_BURST,
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


@router.post("/tele/burst/stop")
async def stop_burst(ip: str):
    """Serienaufnahme stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_STOP_BURST,
            b"",
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


@router.post("/tele/video/start")
async def start_video(ip: str):
    """Video-Aufnahme starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqStartRecord()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_START_RECORD,
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


@router.post("/tele/video/stop")
async def stop_video(ip: str):
    """Video-Aufnahme stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqStopRecord()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_STOP_RECORD,
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


@router.post("/tele/params/set")
async def set_camera_params(ip: str, params: CameraParams):
    """Kamera-Parameter setzen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqSetAllParams()
        req.exp_mode = params.exp_mode
        req.exp_index = params.exp_index
        req.gain_mode = params.gain_mode
        req.gain_index = params.gain_index
        req.ircut_value = params.ircut_value
        req.wb_mode = params.wb_mode
        req.wb_index_type = params.wb_index_type
        req.wb_index = params.wb_index
        req.brightness = params.brightness
        req.contrast = params.contrast
        req.hue = params.hue
        req.saturation = params.saturation
        req.sharpness = params.sharpness
        req.jpg_quality = params.jpg_quality
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_SET_ALL_PARAMS,
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


@router.get("/tele/params/get")
async def get_camera_params(ip: str):
    """Kamera-Parameter abrufen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqGetAllParams()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_TELE,
            CMD_CAMERA_TELE_GET_ALL_PARAMS,
            req.SerializeToString(),
            wait_response=True,
            timeout=5.0
        )
        
        if response:
            res = camera_pb2.ResGetAllParams()
            res.ParseFromString(response.data)
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "params": {
                    "exp_mode": res.exp_mode,
                    "exp_index": res.exp_index,
                    "gain_mode": res.gain_mode,
                    "gain_index": res.gain_index,
                    "ircut_value": res.ircut_value,
                    "wb_mode": res.wb_mode,
                    "wb_index_type": res.wb_index_type,
                    "wb_index": res.wb_index,
                    "brightness": res.brightness,
                    "contrast": res.contrast,
                    "hue": res.hue,
                    "saturation": res.saturation,
                    "sharpness": res.sharpness,
                    "jpg_quality": res.jpg_quality
                }
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Streams
# ============================================================================

@router.get("/stream/{camera_type}")
async def get_camera_stream(camera_type: str, ip: str):
    """
    JPG-Stream abrufen
    camera_type: 'tele' oder 'wide'
    """
    client = DwarfHTTPClient(ip)
    
    try:
        return StreamingResponse(
            client.get_jpg_stream(camera_type),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rtsp/{camera_type}")
async def get_rtsp_url(camera_type: str, ip: str):
    """
    RTSP-URL für Video-Stream
    camera_type: 'tele' oder 'wide'
    """
    client = DwarfHTTPClient(ip)
    url = client.get_rtsp_url(camera_type)
    
    return {
        "rtsp_url": url,
        "camera_type": camera_type
    }


# ============================================================================
# Weitwinkel-Kamera
# ============================================================================

@router.post("/wide/open")
async def open_wide_camera(ip: str, params: CameraOpen):
    """Weitwinkel-Kamera öffnen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqOpenCamera()
        req.binning = params.binning
        req.rtsp_encode_type = params.rtsp_encode_type
        
        response = await ws_client.send_command(
            MODULE_CAMERA_WIDE,
            CMD_CAMERA_WIDE_OPEN_CAMERA,
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


@router.post("/wide/close")
async def close_wide_camera(ip: str):
    """Weitwinkel-Kamera schließen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_WIDE,
            CMD_CAMERA_WIDE_CLOSE_CAMERA,
            b"",
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


@router.post("/wide/photo")
async def take_wide_photo(ip: str):
    """Weitwinkel-Foto aufnehmen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = camera_pb2.ReqPhoto()
        
        response = await ws_client.send_command(
            MODULE_CAMERA_WIDE,
            CMD_CAMERA_WIDE_PHOTOGRAPH,
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
