# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.api.endpoints import extract

api_router = APIRouter()
api_router.include_router(extract.router, prefix="/v1", tags=["extract"])
