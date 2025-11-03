"""
Astro API Endpoints
Astronomie-Funktionen: Kalibrierung, GOTO, Stacking
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import astro_pb2, base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class CalibrateRequest(BaseModel):
    """Kalibrierung starten"""
    pass


class GotoDSORequest(BaseModel):
    """GOTO Deep-Sky-Objekt"""
    ra: float  # Rektaszension
    dec: float  # Deklination
    target_name: str


class GotoSolarRequest(BaseModel):
    """GOTO Sonnensystem"""
    index: int  # 1-9 (Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Moon, Sun)
    lon: float  # GPS-Längengrad
    lat: float  # GPS-Breitengrad
    target_name: str


class TrackSpecialRequest(BaseModel):
    """Sonne/Mond Tracking"""
    index: int  # 0: Sonne, 1: Mond
    lon: float
    lat: float


class DarkFrameRequest(BaseModel):
    """Darkframe aufnehmen"""
    reshoot: int = 0  # 0: Nein, 1: Neu aufnehmen


class DarkFrameParamRequest(BaseModel):
    """Darkframe mit Parametern"""
    exp_index: int
    gain_index: int
    bin_index: int
    cap_size: int


class DarkFrameDeleteRequest(BaseModel):
    """Darkframe löschen"""
    exp_index: int
    gain_index: int
    bin_index: int


class EqSolvingRequest(BaseModel):
    """EQ-Verifizierung"""
    lon: float
    lat: float


# ============================================================================
# Kalibrierung
# ============================================================================

@router.post("/calibration/start")
async def start_calibration(ip: str):
    """Kalibrierung starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStartCalibration()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_CALIBRATION,
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


@router.post("/calibration/stop")
async def stop_calibration(ip: str):
    """Kalibrierung stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopCalibration()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_CALIBRATION,
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
# GOTO
# ============================================================================

@router.post("/goto/dso")
async def goto_dso(ip: str, request: GotoDSORequest):
    """GOTO Deep-Sky-Objekt"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqGotoDSO()
        req.ra = request.ra
        req.dec = request.dec
        req.target_name = request.target_name
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_GOTO_DSO,
            req.SerializeToString(),
            wait_response=True,
            timeout=10.0
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "target": request.target_name
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/goto/solar")
async def goto_solar(ip: str, request: GotoSolarRequest):
    """GOTO Sonnensystem-Objekt"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqGotoSolarSystem()
        req.index = request.index
        req.lon = request.lon
        req.lat = request.lat
        req.target_name = request.target_name
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_GOTO_SOLAR_SYSTEM,
            req.SerializeToString(),
            wait_response=True,
            timeout=10.0
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "target": request.target_name
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/goto/stop")
async def stop_goto(ip: str):
    """GOTO stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopGoto()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_GOTO,
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
# Ein-Klick GOTO
# ============================================================================

@router.post("/goto/one-click/dso")
async def one_click_goto_dso(ip: str, request: GotoDSORequest):
    """Ein-Klick GOTO Deep-Sky-Objekt (mit Auto-Fokus und Kalibrierung)"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqOneClickGotoDSO()
        req.ra = request.ra
        req.dec = request.dec
        req.target_name = request.target_name
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_ONE_CLICK_GOTO_DSO,
            req.SerializeToString(),
            wait_response=True,
            timeout=15.0
        )
        
        if response:
            res = astro_pb2.ResOneClickGoto()
            res.ParseFromString(response.data)
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "step": res.step,
                "all_end": res.all_end,
                "target": request.target_name
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/goto/one-click/solar")
async def one_click_goto_solar(ip: str, request: GotoSolarRequest):
    """Ein-Klick GOTO Sonnensystem"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqOneClickGotoSolarSystem()
        req.index = request.index
        req.lon = request.lon
        req.lat = request.lat
        req.target_name = request.target_name
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_ONE_CLICK_GOTO_SOLAR_SYSTEM,
            req.SerializeToString(),
            wait_response=True,
            timeout=15.0
        )
        
        if response:
            res = astro_pb2.ResOneClickGoto()
            res.ParseFromString(response.data)
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "step": res.step,
                "all_end": res.all_end,
                "target": request.target_name
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/goto/one-click/stop")
async def stop_one_click_goto(ip: str):
    """Ein-Klick GOTO stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopOneClickGoto()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_ONE_CLICK_GOTO,
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
# Stacking
# ============================================================================

@router.post("/stacking/start")
async def start_stacking(ip: str):
    """Live-Stacking starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqCaptureRawLiveStacking()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_CAPTURE_RAW_LIVE_STACKING,
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


@router.post("/stacking/stop")
async def stop_stacking(ip: str):
    """Live-Stacking stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopCaptureRawLiveStacking()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_CAPTURE_RAW_LIVE_STACKING,
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


@router.post("/stacking/wide/start")
async def start_wide_stacking(ip: str):
    """Weitwinkel Live-Stacking starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqCaptureWideRawLiveStacking()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_WIDE_CAPTURE_LIVE_STACKING,
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


@router.post("/stacking/wide/stop")
async def stop_wide_stacking(ip: str):
    """Weitwinkel Live-Stacking stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopCaptureWideRawLiveStacking()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_WIDE_CAPTURE_LIVE_STACKING,
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
# Tracking
# ============================================================================

@router.post("/track/special/start")
async def start_special_tracking(ip: str, request: TrackSpecialRequest):
    """Sonne/Mond Tracking starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqTrackSpecialTarget()
        req.index = request.index
        req.lon = request.lon
        req.lat = request.lat
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_TRACK_SPECIAL_TARGET,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            target = "Sonne" if request.index == 0 else "Mond"
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "target": target
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/track/special/stop")
async def stop_special_tracking(ip: str):
    """Sonne/Mond Tracking stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopTrackSpecialTarget()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_TRACK_SPECIAL_TARGET,
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
# Darkframe
# ============================================================================

@router.post("/darkframe/capture")
async def capture_darkframe(ip: str, request: DarkFrameRequest):
    """Darkframe aufnehmen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqCaptureDarkFrame()
        req.reshoot = request.reshoot
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_CAPTURE_RAW_DARK,
            req.SerializeToString(),
            wait_response=True,
            timeout=30.0
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


@router.post("/darkframe/stop")
async def stop_darkframe(ip: str):
    """Darkframe-Aufnahme stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopCaptureDarkFrame()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_CAPTURE_RAW_DARK,
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


@router.get("/darkframe/check")
async def check_darkframe(ip: str):
    """Darkframe-Status prüfen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqCheckDarkFrame()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_CHECK_GOT_DARK,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            res = astro_pb2.ResCheckDarkFrame()
            res.ParseFromString(response.data)
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "progress": res.progress / 100.0  # 0-100%
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.get("/darkframe/list")
async def get_darkframe_list(ip: str):
    """Darkframe-Liste abrufen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqGetDarkFrameList()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_GET_DARK_FRAME_LIST,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            res = astro_pb2.ResGetDarkFrameInfoList()
            res.ParseFromString(response.data)
            
            frames = [
                {
                    "exp_index": frame.exp_index,
                    "gain_index": frame.gain_index,
                    "bin_index": frame.bin_index
                }
                for frame in res.results
            ]
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "frames": frames
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# EQ-Verifizierung
# ============================================================================

@router.post("/eq-solving/start")
async def start_eq_solving(ip: str, request: EqSolvingRequest):
    """EQ-Verifizierung starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStartEqSolving()
        req.lon = request.lon
        req.lat = request.lat
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_START_EQ_SOLVING,
            req.SerializeToString(),
            wait_response=True,
            timeout=30.0
        )
        
        if response:
            res = astro_pb2.ResStartEqSolving()
            res.ParseFromString(response.data)
            
            return {
                "status": "success" if res.code == 0 else "error",
                "code": res.code,
                "azi_err": res.azi_err,  # Azimut-Fehler
                "alt_err": res.alt_err   # Höhen-Fehler
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/eq-solving/stop")
async def stop_eq_solving(ip: str):
    """EQ-Verifizierung stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqStopEqSolving()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_STOP_EQ_SOLVING,
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
# GO LIVE
# ============================================================================

@router.post("/go-live")
async def go_live(ip: str):
    """GO LIVE - Zurück zum Live-View"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = astro_pb2.ReqGoLive()
        
        response = await ws_client.send_command(
            MODULE_ASTRO,
            CMD_ASTRO_GO_LIVE,
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
