"""
Device API Endpoints
Geräte-Verwaltung und Informationen
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import Device
from ..services.dwarf_client import DwarfHTTPClient
from sqlalchemy import select
from datetime import datetime

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class DeviceConnect(BaseModel):
    """Verbindungs-Request"""
    ip: str
    port: int = 8082


class DeviceInfo(BaseModel):
    """Geräte-Informationen"""
    device_id: int
    device_name: str
    mac_address: str
    ip_address: str
    connection_mode: int
    is_connected: bool


class DeviceNamePassword(BaseModel):
    """Name/Passwort ändern"""
    mode: int  # 0: Passwort, 1: Name
    old_value: str
    new_value: str


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/connect")
async def connect_device(
    device: DeviceConnect,
    db: AsyncSession = Depends(get_db)
):
    """
    Gerät verbinden und in Datenbank speichern
    """
    client = DwarfHTTPClient(device.ip, device.port)
    
    try:
        # Geräte-Info abrufen
        info = await client.get_device_info()
        
        if info.get("code") != 0:
            raise HTTPException(status_code=400, detail="Gerät nicht erreichbar")
        
        data = info.get("data", {})
        
        # In Datenbank suchen/erstellen
        stmt = select(Device).where(Device.mac_address == data.get("macAddress"))
        result = await db.execute(stmt)
        db_device = result.scalar_one_or_none()
        
        if db_device:
            # Update
            db_device.ip_address = device.ip
            db_device.is_connected = True
            db_device.last_seen = datetime.utcnow()
        else:
            # Neu erstellen
            db_device = Device(
                device_id=data.get("deviceId", 1),
                device_name=data.get("deviceName", ""),
                mac_address=data.get("macAddress", ""),
                ip_address=device.ip,
                connection_mode=data.get("wifiConnectedMode", 0),
                is_connected=True,
                last_seen=datetime.utcnow()
            )
            db.add(db_device)
        
        await db.commit()
        await db.refresh(db_device)
        
        return {
            "status": "connected",
            "device": {
                "id": db_device.id,
                "device_name": db_device.device_name,
                "mac_address": db_device.mac_address,
                "ip_address": db_device.ip_address
            },
            "info": data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/info")
async def get_device_info(ip: str):
    """
    Geräte-Informationen direkt vom DWARF II abrufen
    """
    client = DwarfHTTPClient(ip)
    
    try:
        info = await client.get_device_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/firmware")
async def get_firmware_version(ip: str):
    """
    Firmware-Version abrufen
    """
    client = DwarfHTTPClient(ip)
    
    try:
        version = await client.get_firmware_version()
        return version
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/name-password")
async def set_name_password(ip: str, data: DeviceNamePassword):
    """
    Gerätename oder Passwort ändern
    mode: 0 = Passwort, 1 = Name
    """
    client = DwarfHTTPClient(ip)
    
    try:
        result = await client.set_device_name_and_password(
            mode=data.mode,
            old_value=data.old_value,
            new_value=data.new_value
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/reset")
async def reset_device(ip: str):
    """
    Gerät auf Werkseinstellungen zurücksetzen
    """
    client = DwarfHTTPClient(ip)
    
    try:
        result = await client.reset_device_info()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/list")
async def list_devices(db: AsyncSession = Depends(get_db)):
    """
    Alle gespeicherten Geräte auflisten
    """
    stmt = select(Device).order_by(Device.last_seen.desc())
    result = await db.execute(stmt)
    devices = result.scalars().all()
    
    return {
        "devices": [
            {
                "id": d.id,
                "device_name": d.device_name,
                "mac_address": d.mac_address,
                "ip_address": d.ip_address,
                "is_connected": d.is_connected,
                "last_seen": d.last_seen.isoformat() if d.last_seen else None
            }
            for d in devices
        ]
    }


@router.delete("/{device_id}")
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    """
    Gerät aus Datenbank löschen
    """
    stmt = select(Device).where(Device.id == device_id)
    result = await db.execute(stmt)
    device = result.scalar_one_or_none()
    
    if not device:
        raise HTTPException(status_code=404, detail="Gerät nicht gefunden")
    
    await db.delete(device)
    await db.commit()
    
    return {"status": "deleted", "device_id": device_id}
