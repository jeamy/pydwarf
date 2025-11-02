"""
DWARF II HTTP-Client
Kommunikation über HTTP REST API
"""
import httpx
from typing import Optional, Dict, Any, AsyncIterator


class DwarfHTTPClient:
    """HTTP-Client für DWARF II Teleskop"""
    
    def __init__(self, ip: str, port: int = 8082, jpg_port: int = 8092):
        self.ip = ip
        self.port = port
        self.jpg_port = jpg_port
        self.base_url = f"http://{ip}:{port}"
        self.jpg_url = f"http://{ip}:{jpg_port}"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Client schließen"""
        await self.client.aclose()
    
    # ========================================================================
    # Geräte-Informationen
    # ========================================================================
    
    async def get_device_info(self) -> Dict[str, Any]:
        """Geräte-Informationen abrufen"""
        response = await self.client.post(f"{self.base_url}/deviceInfo")
        return response.json()
    
    async def set_device_name_and_password(
        self,
        mode: int,
        old_value: str,
        new_value: str
    ) -> Dict[str, Any]:
        """
        Gerätename oder Passwort ändern
        mode: 0 = Passwort, 1 = Name
        """
        data = {
            "mode": mode,
            "oldValue": old_value,
            "newValue": new_value
        }
        response = await self.client.post(
            f"{self.base_url}/setDeviceNameAndPsd",
            json=data
        )
        return response.json()
    
    async def reset_device_info(self) -> Dict[str, Any]:
        """Gerät zurücksetzen"""
        response = await self.client.post(f"{self.base_url}/resetDeviceInfo")
        return response.json()
    
    # ========================================================================
    # Firmware
    # ========================================================================
    
    async def get_firmware_version(self) -> Dict[str, Any]:
        """Firmware-Version abrufen"""
        response = await self.client.post(f"{self.base_url}/firmwareVersion")
        return response.json()
    
    async def upload_firmware(
        self,
        firmware_file: bytes,
        md5: str
    ) -> Dict[str, Any]:
        """Firmware hochladen"""
        files = {"fiwmwareFileName": firmware_file}
        data = {"md5": md5}
        response = await self.client.post(
            f"{self.base_url}/uploadFirmware",
            files=files,
            data=data
        )
        return response.json()
    
    # ========================================================================
    # Album
    # ========================================================================
    
    async def get_media_counts(self) -> Dict[str, Any]:
        """Anzahl Medien pro Typ abrufen"""
        response = await self.client.post(
            f"{self.base_url}/album/list/mediaCounts"
        )
        return response.json()
    
    async def get_media_list(
        self,
        media_type: int,
        page_index: int = 0,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Medien-Liste abrufen"""
        data = {
            "mediaType": media_type,
            "pageIndex": page_index,
            "pageSize": page_size
        }
        response = await self.client.post(
            f"{self.base_url}/album/list/mediaInfos",
            json=data
        )
        return response.json()
    
    async def delete_media(
        self,
        media_list: list[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Medien löschen"""
        data = {"datas": media_list}
        response = await self.client.post(
            f"{self.base_url}/album/delete",
            json=data
        )
        return response.json()
    
    # ========================================================================
    # Konfiguration
    # ========================================================================
    
    async def get_default_params_config(self) -> Dict[str, Any]:
        """Standard-Parameter-Konfiguration abrufen"""
        response = await self.client.get(
            f"{self.base_url}/getDefaultParamsConfig"
        )
        return response.json()
    
    # ========================================================================
    # Logs
    # ========================================================================
    
    async def get_log_info(self) -> Dict[str, Any]:
        """Log-Informationen abrufen"""
        response = await self.client.get(f"{self.base_url}/logInfo")
        return response.json()
    
    async def download_log(self) -> bytes:
        """Log-Datei herunterladen"""
        response = await self.client.get(f"{self.base_url}/downloadLog")
        return response.content
    
    # ========================================================================
    # Bild-Streams
    # ========================================================================
    
    async def get_jpg_stream(
        self,
        camera: str = "tele"
    ) -> AsyncIterator[bytes]:
        """
        JPG-Stream abrufen
        camera: 'tele' oder 'wide'
        """
        endpoint = "mainstream" if camera == "tele" else "secondstream"
        url = f"{self.jpg_url}/{endpoint}"
        
        async with self.client.stream("GET", url) as response:
            async for chunk in response.aiter_bytes():
                yield chunk
    
    # ========================================================================
    # RTSP-URLs
    # ========================================================================
    
    def get_rtsp_url(self, camera: str = "tele") -> str:
        """
        RTSP-URL für Video-Stream
        camera: 'tele' oder 'wide'
        """
        channel = "ch0" if camera == "tele" else "ch1"
        return f"rtsp://{self.ip}/{channel}/stream0"
