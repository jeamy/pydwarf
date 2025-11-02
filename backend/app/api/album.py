"""
Album API Endpoints
Medien-Verwaltung
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services.dwarf_client import DwarfHTTPClient
from ..utils.constants import *

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class MediaListRequest(BaseModel):
    """Medien-Liste Request"""
    media_type: int = 0  # 0: Alle, 1: Foto, 2: Video, etc.
    page_index: int = 0
    page_size: int = 20


class MediaDeleteItem(BaseModel):
    """Medien-Lösch-Item"""
    media_type: int
    file_path: str
    file_name: str


class MediaDeleteRequest(BaseModel):
    """Medien löschen"""
    items: List[MediaDeleteItem]


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/counts")
async def get_media_counts(ip: str):
    """
    Anzahl Medien pro Typ abrufen
    """
    client = DwarfHTTPClient(ip)
    
    try:
        counts = await client.get_media_counts()
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/list")
async def get_media_list(ip: str, request: MediaListRequest):
    """
    Medien-Liste abrufen mit Paginierung
    """
    client = DwarfHTTPClient(ip)
    
    try:
        media_list = await client.get_media_list(
            media_type=request.media_type,
            page_index=request.page_index,
            page_size=request.page_size
        )
        return media_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.post("/delete")
async def delete_media(ip: str, request: MediaDeleteRequest):
    """
    Medien löschen
    """
    client = DwarfHTTPClient(ip)
    
    try:
        # In DWARF II Format konvertieren
        media_list = [
            {
                "mediaType": item.media_type,
                "filePath": item.file_path,
                "fileName": item.file_name
            }
            for item in request.items
        ]
        
        result = await client.delete_media(media_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()


@router.get("/config")
async def get_default_params_config(ip: str):
    """
    Standard-Parameter-Konfiguration abrufen
    (params_config.json)
    """
    client = DwarfHTTPClient(ip)
    
    try:
        config = await client.get_default_params_config()
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await client.close()
