import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from routes.uploads import router as uploads_router
from routes.search import router as search_router
from routes.maps import router as maps_router
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from jose import JWTError, jwt
from celery import Celery

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Building Detection API",
    description="API для распознавания зданий, геокоординат и адресов (ТЗ + Yandex Cloud интеграция)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(uploads_router, prefix="/uploads", tags=["uploads"])
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(maps_router, prefix="/maps", tags=["maps"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

celery = Celery(name, broker=os.getenv("CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user

@app.get("/")
def root():
    return {"message": "API ready. Docs: /docs"}