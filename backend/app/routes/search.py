from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List
from database import get_db
from models import Task, SearchHistory
from schemas import SearchRequest, TaskResponse, SearchHistoryResponse
from services.geo import get_coords_from_address, calculate_distance
from services.storage import get_presigned_url
from main import get_current_user

router = APIRouter()


@router.post("/", response_model=List[TaskResponse])
async def search_images(request: SearchRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query_type = "coords" if request.latitude else "address"
    if query_type == "address" and request.address:
        request.latitude, request.longitude = get_coords_from_address(request.address)  # Bidirectional

    # Filters (backend)
    query = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "completed",
        Task.created_at >= func.now() - timedelta(years=request.time_interval_years)
    )
    if request.source_filter != "all":
        query = query.filter(Task.source == request.source_filter)
    if request.min_resolution:
        query = query.filter(Task.resolution.ilike(f"%{request.min_resolution}%"))

    tasks = query.all()
    results = []
    for task in tasks:
        task_lat, task_lon = task.location.y, task.location.x  # PostGIS
        score = 1.0  # Dummy, add Yandex Vision similarity
        dist = calculate_distance((request.latitude, request.longitude), (task_lat, task_lon))
        if request.search_principle == "radius" and dist <= request.radius_km * 1000 and score >= request.min_score:
            task.download_url = await get_presigned_url(task.storage_key)
            results.append(task)
        # Other principles: time sort, source priority

    if not results:
        raise HTTPException(404, "No results")

    results = sorted(results, key=lambda t: t.processed_at, reverse=True)[:5]  # Chrono, max 5

    # Save history
    history = SearchHistory(
        query_type=query_type,
        params=request.dict(),
        results_count=len(results),
        user_id=current_user.id
    )
    db.add(history)
    db.commit()

    return results


@router.get("/history", response_model=List[SearchHistoryResponse])
def get_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(SearchHistory).filter(SearchHistory.user_id == current_user.id).all()