"""
Camera API Endpoints
Kamera-Steuerung (Tele & Wide)
"""
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from ..services.dwarf_client import DwarfHTTPClient
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
    from ..lib.dwarfii_api import BINNING_1X1, BINNING_2X2
    from ..lib.dwarfii_camera import turn_on_tele_camera
    from ..lib.dwarf_connection import connection_manager
    
    # Response tracking
    response_data = {"status": "pending"}
    response_event = asyncio.Event()
    
    def message_callback(txt_info, result_data):
        """Callback für empfangene Nachrichten"""
        code = result_data.get("code")
        
        if code is not None:
            if code == 0:
                response_data["status"] = "success"
                response_data["code"] = 0
                response_data["message"] = "Kamera erfolgreich geöffnet"
                response_event.set()
            elif code == 374:
                response_data["status"] = "success"
                response_data["code"] = 374
                response_data["message"] = "Kamera bereits geöffnet"
                response_event.set()
            elif code in [27, 56, 57]:
                # Fehler - aber setze Event trotzdem
                response_data["status"] = "error"
                response_data["code"] = code
                response_data["message"] = f"Kamera-Fehler (Code {code})"
                response_event.set()
    
    try:
        # Hole persistente Verbindung
        ws_handler = await connection_manager.get_connection(ip)
        
        if not ws_handler.is_connected():
            return {"status": "error", "message": "Verbindung fehlgeschlagen"}
        
        # Callback registrieren
        ws_handler.register_message_callback("camera_open", message_callback)
        
        # Kamera öffnen
        binning = BINNING_2X2 if params.binning else BINNING_2X2
        await turn_on_tele_camera(ws_handler, binning=binning)
        
        # Warte auf Antwort (max 10 Sekunden - Notify braucht Zeit)
        try:
            await asyncio.wait_for(response_event.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            return {"status": "no_response", "message": "Keine Antwort nach 10s"}
        
        # Cleanup
        ws_handler.unregister_message_callback("camera_open")
        
        # Kurze Verzögerung, damit Notify vollständig verarbeitet wird
        await asyncio.sleep(0.5)
        
        # Verbindung NICHT schließen - wird wiederverwendet!
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tele/close")
async def close_tele_camera(ip: str):
    """Teleobjektiv-Kamera schließen"""
    # Verwende dwarfii_api Python Port
    from ..lib.dwarfii_api import WebSocketHandler
    from ..lib.dwarfii_camera import turn_off_tele_camera
    
    # Response tracking
    response_data = {"status": "pending"}
    response_event = asyncio.Event()
    
    def message_callback(txt_info, result_data):
        """Callback für empfangene Nachrichten"""
        code = result_data.get("code")
        
        if code is not None:
            if code == 0:
                response_data["status"] = "success"
                response_data["code"] = 0
                response_data["message"] = "Kamera erfolgreich geschlossen"
                response_event.set()
            else:
                # Andere Codes als Success behandeln (Kamera war schon zu)
                response_data["status"] = "success"
                response_data["code"] = code
                response_data["message"] = f"Kamera geschlossen (Code {code})"
                response_event.set()
    
    try:
        # WebSocketHandler erstellen
        ws_handler = WebSocketHandler(ip)
        
        # Callback registrieren
        ws_handler.register_message_callback("camera_close", message_callback)
        
        # Verbinden
        await ws_handler.open()
        
        if not ws_handler.is_connected():
            return {"status": "error", "message": "Verbindung fehlgeschlagen"}
        
        # Kamera schließen
        await turn_off_tele_camera(ws_handler)
        
        # Warte auf Antwort (max 5 Sekunden)
        try:
            await asyncio.wait_for(response_event.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            return {"status": "no_response", "message": "Keine Antwort nach 5s"}
        
        # Cleanup
        ws_handler.unregister_message_callback("camera_close")
        await ws_handler.close()
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tele/photo")
async def take_photo(ip: str):
    """Foto aufnehmen"""
    from ..lib.dwarfii_camera import take_photo as take_photo_cmd
    from ..lib.dwarf_connection import connection_manager
    
    response_data = {"status": "pending"}
    response_event = asyncio.Event()
    
    def message_callback(txt_info, result_data):
        if result_data.get("module_id") != MODULE_CAMERA_TELE:
            return
        if result_data.get("cmd") != CMD_CAMERA_TELE_PHOTOGRAPH:
            return
        code = result_data.get("code")
        if code is None:
            return
        if code == 0:
            response_data["status"] = "success"
            response_data["code"] = 0
            response_data["message"] = "Foto aufgenommen"
        elif code == 374:
            response_data["status"] = "success"
            response_data["code"] = 374
            response_data["message"] = "Kamera bereits ausgelöst"
        else:
            response_data["status"] = "error"
            response_data["code"] = code
            response_data["message"] = f"Fehler (Code {code})"
        response_event.set()
    
    try:
        ws_handler = await connection_manager.get_connection(ip)
        if not ws_handler.is_connected():
            return {"status": "error", "message": "Verbindung fehlgeschlagen"}
        
        ws_handler.register_message_callback("camera_photo", message_callback)
        
        await take_photo_cmd(ws_handler)
        
        try:
            await asyncio.wait_for(response_event.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            return {"status": "no_response", "message": "Keine Antwort nach 10s"}
        finally:
            ws_handler.unregister_message_callback("camera_photo")
        
        # Verbindung offen lassen (wird wiederverwendet)
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    from ..lib.dwarfii_api import WebSocketHandler
    from ..lib.dwarfii_camera import start_video_recording
    
    response_data = {"status": "pending"}
    response_event = asyncio.Event()
    
    def message_callback(txt_info, result_data):
        code = result_data.get("code")
        if code is not None:
            response_data["status"] = "success" if code == 0 else "error"
            response_data["code"] = code
            response_data["message"] = "Video gestartet" if code == 0 else f"Fehler (Code {code})"
            response_event.set()
    
    try:
        ws_handler = WebSocketHandler(ip)
        ws_handler.register_message_callback("video_start", message_callback)
        await ws_handler.open()
        
        if not ws_handler.is_connected():
            return {"status": "error", "message": "Verbindung fehlgeschlagen"}
        
        await start_video_recording(ws_handler)
        
        try:
            await asyncio.wait_for(response_event.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            return {"status": "no_response", "message": "Keine Antwort nach 5s"}
        
        ws_handler.unregister_message_callback("video_start")
        await ws_handler.close()
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tele/video/stop")
async def stop_video(ip: str):
    """Video-Aufnahme stoppen"""
    from ..lib.dwarfii_api import WebSocketHandler
    from ..lib.dwarfii_camera import stop_video_recording
    
    response_data = {"status": "pending"}
    response_event = asyncio.Event()
    
    def message_callback(txt_info, result_data):
        code = result_data.get("code")
        if code is not None:
            response_data["status"] = "success" if code == 0 else "error"
            response_data["code"] = code
            response_data["message"] = "Video gestoppt" if code == 0 else f"Fehler (Code {code})"
            response_event.set()
    
    try:
        ws_handler = WebSocketHandler(ip)
        ws_handler.register_message_callback("video_stop", message_callback)
        await ws_handler.open()
        
        if not ws_handler.is_connected():
            return {"status": "error", "message": "Verbindung fehlgeschlagen"}
        
        await stop_video_recording(ws_handler)
        
        try:
            await asyncio.wait_for(response_event.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            return {"status": "no_response", "message": "Keine Antwort nach 5s"}
        
        ws_handler.unregister_message_callback("video_stop")
        await ws_handler.close()
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    endpoint = "mainstream" if camera_type == "tele" else "secondstream"
    stream_url = f"{client.jpg_url}/{endpoint}"
    default_media_type = "multipart/x-mixed-replace"
    
    try:
        request = client.client.build_request("GET", stream_url)
        response = await client.client.send(request, stream=True)
    except Exception as e:
        await client.close()
        raise HTTPException(status_code=500, detail=f"Stream-Verbindung fehlgeschlagen: {e}")
    
    if response.status_code != 200:
        await response.aclose()
        await client.close()
        raise HTTPException(status_code=response.status_code, detail="Stream nicht verfügbar")
    
    media_type = response.headers.get("Content-Type", default_media_type)
    
    async def stream_generator():
        try:
            async for chunk in response.aiter_bytes():
                yield chunk
        finally:
            await response.aclose()
            await client.close()
    
    return StreamingResponse(stream_generator(), media_type=media_type)


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
