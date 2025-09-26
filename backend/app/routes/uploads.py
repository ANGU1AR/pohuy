from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import zipfile
import shutil
from pathlib import Path
from PIL import Image  # Any formats
from database import get_db
from models import Task
from schemas import TaskResponse
from services.detection import detect_buildings, detect_scene  # + Places365
from services.geo import get_coords_from_image, get_address_from_coords
from services.storage import upload_to_yandex_storage, get_presigned_url
from utils.exif import extract_metadata
from main import get_current_user, celery

router = APIRouter()

TEMP_DIR = Path("uploads")
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=List[TaskResponse])
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db),
                       current_user=Depends(get_current_user)):
    tasks = []
    for file in files:
        temp_path = TEMP_DIR / file.filename
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if file.filename.endswith(".zip"):
            with zipfile.ZipFile(temp_path, "r") as zip_ref:
                zip_ref.extractall(TEMP_DIR)
            for extracted in TEMP_DIR.glob("*.*"):
                if extracted.is_file():
                    task = await process_file(str(extracted), db, current_user.id)
                    if task:
                        tasks.append(task)
            temp_path.unlink()
            continue

        task = await process_file(str(temp_path), db, current_user.id)
        if task:
            tasks.append(task)
        temp_path.unlink()
    return tasks


async def process_file(file_path: str, db: Session, user_id: int):
    try:
        img = Image.open(file_path)  # Support any format
        if img.format not in ["JPEG", "PNG"]:
            converted_path = file_path + ".png"
            img.save(converted_path, "PNG")
            file_path = converted_path
    except:
        raise HTTPException(400, "Invalid image format")

    metadata = extract_metadata(file_path)
    bbox = detect_buildings(file_path)  # YOLO
    scene = detect_scene(file_path)  # Places365 for architecture/landscapes
    metadata["scene"] = scene
    lat, lon = get_coords_from_image(file_path, metadata)
    address = get_address_from_coords(lat, lon)

    storage_key = await upload_to_yandex_storage(file_path)

    db_task = Task(
        filename=Path(file_path).name,
        original_filename=Path(file_path).name,
        storage_key=storage_key,
        status="completed",
        bbox=bbox,
        location=f"POINT({lon} {lat})",  # PostGIS
        address=address,
        metadata=metadata,
        source="uploaded",
        resolution=f"{img.width}x{img.height}",
        user_id=user_id,
        processed_at=func.now()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    Path(file_path).unlink(missing_ok=True)
    return db_task