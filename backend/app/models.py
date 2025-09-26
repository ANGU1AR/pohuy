from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    tablename = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Task(Base):
    tablename = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    storage_key = Column(String)  # Key in Yandex Storage
    status = Column(String, default="pending")
    bbox = Column(JSON)  # Bbox dict
    location = Column(Geometry('POINT', srid=4326))  # WGS84 coords
    address = Column(String)
    metadata = Column(JSON)  # EXIF, scene from Places365
    source = Column(String)
    resolution = Column(String)  # e.g., "high"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey("users.id"))

class SearchHistory(Base):
    tablename = "search_history"
    id = Column(Integer, primary_key=True, index=True)
    query_type = Column(String)  # "coords" or "photo"
    params = Column(JSON)  # e.g., {"lat": 55.75, "lon": 37.61}
    results_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))