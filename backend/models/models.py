from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from backend.database.database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, index=True)
    ip = Column(String)
    os = Column(String)
    os_version = Column(String)
    architecture = Column(String)
    processor = Column(String)
    cpu_percent = Column(Float)
    ram_used_mb = Column(Float)
    ram_total_mb = Column(Float)
    disk_percent = Column(Float)
    net_sent_kb = Column(Float)
    net_recv_kb = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
