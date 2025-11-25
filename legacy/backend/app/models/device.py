from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from ..database import Base


class Device(Base):
    """DWARF II Gerät"""
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)  # 1: DWARF II, 2: MAGNI
    device_name = Column(String, nullable=False)
    mac_address = Column(String, unique=True, nullable=False)
    ip_address = Column(String, nullable=False)
    connection_mode = Column(Integer, default=0)  # 0: AP, 1: STA
    is_connected = Column(Boolean, default=False)
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
