from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    filename: str
    original_filename: str
    source: str = "uploaded"

class TaskResponse(BaseModel):
    id: int
    filename: str
    status: str
    bbox: Optional[Dict]
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]
    metadata: Optional[Dict]
    download_url: Optional[str]  # Presigned
    created_at: datetime
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    address: Optional[str]  # Bidirectional
    radius_km: Optional[float] = 1.0
    time_interval_years: Optional[int] = 3
    source_filter: Optional[str] = "all"
    min_resolution: Optional[str] = "medium"
    min_score: Optional[float] = 0.5  # Relevancy
    search_principle: str = "radius"  # "radius", "time", "source"

class SearchHistoryResponse(BaseModel):
    id: int
    query_type: str
    params: Dict
    results_count: int
    created_at: datetime

class ExportRequest(BaseModel):
    task_ids: Optional[List[int]] = None