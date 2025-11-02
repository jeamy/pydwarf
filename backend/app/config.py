from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Anwendungs-Konfiguration"""
    
    # Datenbank
    database_url: str = "sqlite+aiosqlite:///./database/dwarf.db"
    
    # DWARF II Standard-Einstellungen
    dwarf_default_ip: str = "192.168.88.1"
    dwarf_http_port: int = 8082
    dwarf_jpg_port: int = 8092
    dwarf_ws_port: int = 9900
    
    # API-Einstellungen
    api_title: str = "DWARF II Control API"
    api_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"


settings = Settings()
