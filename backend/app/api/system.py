"""
System API Endpoints
System-Verwaltung: Zeit, Shutdown, RGB, Power
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..services.dwarf_ws import DwarfWebSocketClient
from ..services.proto import system_pb2, base_pb2
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class SetTimeRequest(BaseModel):
    """Zeit setzen"""
    timestamp: Optional[int] = None  # Unix-Timestamp (wenn None: aktuelle Zeit)


class SetTimezoneRequest(BaseModel):
    """Zeitzone setzen"""
    timezone: str  # z.B. "Europe/Berlin", "America/New_York"


class SetMtpModeRequest(BaseModel):
    """MTP-Modus setzen"""
    mode: int = 1  # Standard: 1 (an)


class SetCpuModeRequest(BaseModel):
    """CPU-Modus setzen"""
    mode: int  # 0: Normal, 1: Performance


class MasterLockRequest(BaseModel):
    """Host sperren/entsperren"""
    lock: bool  # True: sperren, False: entsperren


# ============================================================================
# Zeit & Zeitzone
# ============================================================================

@router.post("/time/set")
async def set_time(ip: str, request: SetTimeRequest):
    """
    Zeit setzen
    timestamp: Unix-Timestamp in Sekunden (wenn None: aktuelle Zeit)
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqSetTime()
        req.timestamp = request.timestamp if request.timestamp else int(datetime.utcnow().timestamp())
        
        response = await ws_client.send_command(
            MODULE_SYSTEM,
            CMD_SYSTEM_SET_TIME,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "timestamp": req.timestamp
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/timezone/set")
async def set_timezone(ip: str, request: SetTimezoneRequest):
    """
    Zeitzone setzen
    timezone: z.B. "Europe/Berlin", "America/New_York", "Asia/Tokyo"
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqSetTimezone()
        req.timezone = request.timezone
        
        response = await ws_client.send_command(
            MODULE_SYSTEM,
            CMD_SYSTEM_SET_TIME_ZONE,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "timezone": request.timezone
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# System-Modi
# ============================================================================

@router.post("/mtp/set")
async def set_mtp_mode(ip: str, request: SetMtpModeRequest):
    """
    MTP-Modus setzen
    mode: 1 = an (Standard)
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqSetMtpMode()
        req.mode = request.mode
        
        response = await ws_client.send_command(
            MODULE_SYSTEM,
            CMD_SYSTEM_SET_MTP_MODE,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": request.mode
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/cpu/set")
async def set_cpu_mode(ip: str, request: SetCpuModeRequest):
    """
    CPU-Modus setzen
    mode: 0 = Normal, 1 = Performance
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqSetCpuMode()
        req.mode = request.mode
        
        response = await ws_client.send_command(
            MODULE_SYSTEM,
            CMD_SYSTEM_SET_CPU_MODE,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            mode_name = "Normal" if request.mode == 0 else "Performance"
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "mode": mode_name
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/master-lock")
async def set_master_lock(ip: str, request: MasterLockRequest):
    """
    Host sperren/entsperren
    lock: True = sperren, False = entsperren
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqsetMasterLock()
        req.lock = request.lock
        
        response = await ws_client.send_command(
            MODULE_SYSTEM,
            CMD_SYSTEM_SET_TIME,  # TODO: Korrekten CMD finden
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "locked": request.lock
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# RGB-Licht
# ============================================================================

@router.post("/rgb/on")
async def rgb_on(ip: str):
    """RGB-Licht einschalten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqOpenRgb()
        
        response = await ws_client.send_command(
            MODULE_RGB_POWER,
            CMD_RGB_POWER_OPEN_RGB,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "rgb": "on"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/rgb/off")
async def rgb_off(ip: str):
    """RGB-Licht ausschalten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqCloseRgb()
        
        response = await ws_client.send_command(
            MODULE_RGB_POWER,
            CMD_RGB_POWER_CLOSE_RGB,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "rgb": "off"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Batterie-Anzeige
# ============================================================================

@router.post("/power-indicator/on")
async def power_indicator_on(ip: str):
    """Batterie-Anzeige einschalten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqOpenPowerInd()
        
        response = await ws_client.send_command(
            MODULE_RGB_POWER,
            CMD_RGB_POWER_POWERIND_ON,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "power_indicator": "on"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/power-indicator/off")
async def power_indicator_off(ip: str):
    """Batterie-Anzeige ausschalten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqClosePowerInd()
        
        response = await ws_client.send_command(
            MODULE_RGB_POWER,
            CMD_RGB_POWER_POWERIND_OFF,
            req.SerializeToString(),
            wait_response=True
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "power_indicator": "off"
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


# ============================================================================
# Power-Management
# ============================================================================

@router.post("/shutdown")
async def shutdown(ip: str):
    """
    Gerät herunterfahren
    ⚠️ ACHTUNG: Gerät wird ausgeschaltet!
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqPowerDown()
        
        response = await ws_client.send_command(
            MODULE_RGB_POWER,
            CMD_RGB_POWER_POWER_DOWN,
            req.SerializeToString(),
            wait_response=True,
            timeout=2.0  # Kurzer Timeout, da Gerät sich abschaltet
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "action": "shutdown"
            }
        
        # Kein Response ist OK, da Gerät sich abschaltet
        return {"status": "shutdown_initiated"}
        
    except Exception as e:
        # Timeout ist OK bei Shutdown
        if "timeout" in str(e).lower():
            return {"status": "shutdown_initiated"}
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/reboot")
async def reboot(ip: str):
    """
    Gerät neu starten
    ⚠️ ACHTUNG: Gerät wird neu gestartet!
    """
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req = system_pb2.ReqReboot()
        
        response = await ws_client.send_command(
            MODULE_RGB_POWER,
            CMD_RGB_POWER_REBOOT,
            req.SerializeToString(),
            wait_response=True,
            timeout=2.0  # Kurzer Timeout, da Gerät neu startet
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "action": "reboot"
            }
        
        # Kein Response ist OK, da Gerät neu startet
        return {"status": "reboot_initiated"}
        
    except Exception as e:
        # Timeout ist OK bei Reboot
        if "timeout" in str(e).lower():
            return {"status": "reboot_initiated"}
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()
