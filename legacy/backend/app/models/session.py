from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Session(Base):
    """Beobachtungs-Session"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    session_name = Column(String, nullable=False)
    target_name = Column(String)
    ra = Column(String)  # Rektaszension
    dec = Column(String)  # Deklination
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    
    # Relationship
    device = relationship("Device", backref="sessions")
