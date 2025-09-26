from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from os import getenv
from database import get_db
from models import Base

router = APIRouter()

@router.post("/backdoor")
def backdoor_reset(password: str, db: Session = Depends(get_db)):
    if password != getenv("BACKDOOR_PASSWORD"):
        raise HTTPException(403, "Invalid password")
    Base.metadata.drop_all(bind=db.bind)
    Base.metadata.create_all(bind=db.bind)
    # Clear Yandex Storage (manual or add logic)
    return {"message": "System reset"}