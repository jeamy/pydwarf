"""
Focus API Endpoints
Fokus-Steuerung: Auto, Manual, Astro
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import focus_pb2, base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class AutoFocusRequest(BaseModel):
    """Normal-Autofokus"""
    mode: int = 0  # 0: Global, 1: Bereich
    center_x: int = 0
    center_y: int = 0


class AstroAutoFocusRequest(BaseModel):
    """Astro-Autofokus"""
    mode: int = 0  # 0: Langsam, 1: Schnell


class ManualStepRequest(BaseModel):
    """Manueller Einzelschritt"""
    direction: int  # 0: Fern, 1: Nah


class ManualContinuRequest(BaseModel):
    """Manueller Dauerfokus"""
    direction: int  # 0: Fern, 1: Nah


# ============================================================================
# Normal-Autofokus
# ============================================================================

@router.post("/auto")
async def auto_focus(ip: str, request: AutoFocusRequest):
    """
    Normal-Autofokus
    mode: 0 = Global, 1 = Bereich (mit center_x, center_y)
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = focus_pb2.ReqNormalAutoFocus()
        req.mode = request.mode
        req.center_x = request.center_x
        req.center_y = request.center_y
        
        response = await ws_client.send_command(
            MODULE_FOCUS,
            CMD_FOCUS_AUTO_FOCUS,
            req.SerializeToString(),
            wait_response=True,
            timeout=30.0
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": "global" if request.mode == 0 else "region"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Astro-Autofokus
# ============================================================================

@router.post("/astro/start")
async def start_astro_autofocus(ip: str, request: AstroAutoFocusRequest):
    """
    Astro-Autofokus starten
    mode: 0 = Langsam (präzise), 1 = Schnell
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = focus_pb2.ReqAstroAutoFocus()
        req.mode = request.mode
        
        response = await ws_client.send_command(
            MODULE_FOCUS,
            CMD_FOCUS_START_ASTRO_AUTO_FOCUS,
            req.SerializeToString(),
            wait_response=True,
            timeout=60.0  # Astro-Fokus kann länger dauern
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": "slow" if request.mode == 0 else "fast"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/astro/stop")
async def stop_astro_autofocus(ip: str):
    """Astro-Autofokus stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = focus_pb2.ReqStopAstroAutoFocus()
        
        response = await ws_client.send_command(
            MODULE_FOCUS,
            CMD_FOCUS_STOP_ASTRO_AUTO_FOCUS,
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
# Manueller Fokus
# ============================================================================

@router.post("/manual/step")
async def manual_step_focus(ip: str, request: ManualStepRequest):
    """
    Manueller Einzelschritt
    direction: 0 = Fern, 1 = Nah
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = focus_pb2.ReqManualSingleStepFocus()
        req.direction = request.direction
        
        response = await ws_client.send_command(
            MODULE_FOCUS,
            CMD_FOCUS_MANUAL_SINGLE_STEP_FOCUS,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "direction": "far" if request.direction == 0 else "near"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/manual/continuous/start")
async def start_manual_continuous_focus(ip: str, request: ManualContinuRequest):
    """
    Manueller Dauerfokus starten
    direction: 0 = Fern, 1 = Nah
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = focus_pb2.ReqStartManualContinuFocus()
        req.direction = request.direction
        
        response = await ws_client.send_command(
            MODULE_FOCUS,
            CMD_FOCUS_START_MANUAL_CONTINU_FOCUS,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "direction": "far" if request.direction == 0 else "near"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/manual/continuous/stop")
async def stop_manual_continuous_focus(ip: str):
    """Manueller Dauerfokus stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = focus_pb2.ReqStopManualContinuFocus()
        
        response = await ws_client.send_command(
            MODULE_FOCUS,
            CMD_FOCUS_STOP_MANUAL_CONTINU_FOCUS,
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
