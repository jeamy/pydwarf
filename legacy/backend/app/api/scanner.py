"""
Network Scanner API
Sucht nach DWARF II Geräten im Netzwerk
"""
from fastapi import APIRouter
import asyncio
import socket
from typing import List

router = APIRouter()


async def check_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    """Prüft ob ein Port offen ist"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False


async def scan_ip(ip: str) -> dict:
    """Scannt eine IP nach DWARF II Ports"""
    # Prüfe DWARF II Ports parallel
    port_8082 = await check_port(ip, 8082, timeout=0.3)
    port_9900 = await check_port(ip, 9900, timeout=0.3)
    
    # Wenn beide Ports offen sind, ist es wahrscheinlich ein DWARF II
    if port_8082 and port_9900:
        port_8092 = await check_port(ip, 8092, timeout=0.3)
        return {
            "ip": ip,
            "ports": {
                "http": port_8082,
                "stream": port_8092,
                "websocket": port_9900
            },
            "is_dwarf": True
        }
    
    return None


@router.get("/scan/network")
async def scan_network(subnet: str = "192.168.88", full: bool = False):
    """
    Scannt Netzwerk nach DWARF II Geräten
    
    subnet: Netzwerk-Präfix (z.B. "192.168.88" oder "192.168.8")
    full: Wenn True, scannt alle 254 IPs, sonst auch alle (für Zuverlässigkeit)
    """
    found_devices = []
    
    # Scanne immer ALLE IPs für Zuverlässigkeit
    # (Der Scan ist schnell genug dank async)
    max_ip = 255
    
    # Scanne IP-Bereich
    tasks = []
    for i in range(1, max_ip):
        ip = f"{subnet}.{i}"
        tasks.append(scan_ip(ip))
    
    # Führe alle Scans parallel aus
    results = await asyncio.gather(*tasks)
    
    # Filtere gefundene Geräte
    found_devices = [r for r in results if r is not None]
    
    return {
        "subnet": subnet,
        "scanned_ips": max_ip - 1,
        "found_devices": len(found_devices),
        "devices": found_devices
    }


@router.get("/scan/quick")
async def quick_scan():
    """
    Schneller Scan - prüft nur gängige Subnetze
    Scannt ALLE 254 IPs für bessere Erkennung
    """
    common_subnets = [
        "192.168.88",   # DWARF II Standard
        "192.168.8",    # Häufig
        "192.168.1",    # Router Standard
        "192.168.0",    # Router Standard
        "10.0.0",       # Privat
    ]
    
    all_devices = []
    scanned_ips = 0
    
    for subnet in common_subnets:
        # Scanne ALLE IPs (1-254)
        tasks = []
        for i in range(1, 255):
            ip = f"{subnet}.{i}"
            tasks.append(scan_ip(ip))
        
        results = await asyncio.gather(*tasks)
        devices = [r for r in results if r is not None]
        all_devices.extend(devices)
        scanned_ips += 254
        
        # Wenn Gerät gefunden, breche ab
        if devices:
            break
    
    return {
        "scanned_subnets": common_subnets,
        "scanned_ips": scanned_ips,
        "found_devices": len(all_devices),
        "devices": all_devices
    }


@router.get("/scan/ip/{ip}")
async def scan_single_ip(ip: str):
    """
    Scannt eine einzelne IP
    """
    result = await scan_ip(ip)
    
    if result:
        return {
            "found": True,
            "device": result
        }
    else:
        return {
            "found": False,
            "ip": ip,
            "message": "Kein DWARF II an dieser Adresse gefunden"
        }
