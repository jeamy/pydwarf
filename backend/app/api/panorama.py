"""
Panorama API Endpoints
Panorama-Aufnahmen
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

class StartPanoramaRequest(BaseModel):
    """Panorama starten"""
    rows: int  # Anzahl Zeilen
    cols: int  # Anzahl Spalten


# ============================================================================
# Manual Protobuf Encoding (da panorama_pb2 fehlt)
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


def _create_req_start_panorama(rows: int, cols: int) -> bytes:
    """Create ReqStartPanoramaByGrid message"""
    message = b""
    message += _encode_field(1, 0, _encode_varint(rows))
    message += _encode_field(2, 0, _encode_varint(cols))
    return message


# ============================================================================
# Panorama Endpoints
# ============================================================================

@router.post("/start")
async def start_panorama(ip: str, request: StartPanoramaRequest):
    """Panorama-Aufnahme starten"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        req_data = _create_req_start_panorama(request.rows, request.cols)
        
        response = await ws_client.send_command(
            MODULE_PANORAMA,
            CMD_PANORAMA_START_GRID,
            req_data,
            wait_response=True,
            timeout=10.0
        )
        
        if response:
            com_response = base_pb2.ComResponse()
            com_response.ParseFromString(response.data)
            
            return {
                "status": "success" if com_response.code == 0 else "error",
                "code": com_response.code,
                "grid": {"rows": request.rows, "cols": request.cols},
                "total_images": request.rows * request.cols
            }
        
        return {"status": "no_response"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await ws_client.disconnect()


@router.post("/stop")
async def stop_panorama(ip: str):
    """Panorama-Aufnahme stoppen"""
    ws_client = DwarfWebSocketClient(ip)
    
    try:
        await ws_client.connect()
        
        # Empty message
        req_data = b""
        
        response = await ws_client.send_command(
            MODULE_PANORAMA,
            CMD_PANORAMA_STOP,
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
